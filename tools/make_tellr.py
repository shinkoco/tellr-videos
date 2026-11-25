#!/usr/bin/env python3
"""TELLR — montage d'un clip au format 3 temps (accroche, clip plein cadre, à retenir).

Usage : python3 tools/make_tellr.py spec.json out.mp4

spec.json :
{
  "src": "src.mp4",               # vidéo source (déjà téléchargée)
  "start": 12.0, "end": 78.0,     # extrait en secondes dans la source (60-90 s conseillé)
  "crop": [x, y, w, h],           # optionnel : zone à garder (sinon recadrage centré 9:16)
  "guest": "Yomi Denzel",         # nom de l'invité (bandeau)
  "hook": "La phrase choc du clip", # VRAIE phrase prononcée, mot pour mot (guillemets ajoutés)
  "context": "Une ligne de contexte écrite par TELLR",
  "source": "Yomi Denzel · YouTube",
  "captions": [[0.0, 1.4, "et là j'ai *compris*"], ...],  # temps relatifs à start ; *mot* = mot-clé coloré
  "zooms": [[10.2, 13.0]],        # optionnel : intervalles de zoom (punch-in 1,12x)
  "takeaway": "La leçon du clip, reformulée par TELLR",
  "hook_secs": 3.0, "end_secs": 3.5,
  "category": "business",        # optionnel, affiché dans la bulle d'accroche
  "end_style": "E" ou "F"        # optionnel, sinon alterné automatiquement
}
Charte provisoire : couleur ACCENT, police Inter Display. À remplacer par la charte TELLR.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
ACCENT = (239, 74, 35)
INK = (26, 26, 26)
CREAM = (255, 246, 236)
FONT_DIRS = ["/usr/share/fonts/opentype/inter", os.path.join(os.path.dirname(__file__), "fonts")]


def font(weight, size):
    for d in FONT_DIRS:
        p = os.path.join(d, f"InterDisplay-{weight}.otf")
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.truetype("DejaVuSans-Bold.ttf", size)


def wrap(d, text, fnt, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t.replace("*", ""), font=fnt) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


BRAND = json.load(open(os.path.join(os.path.dirname(__file__), "brand", "tellr_brand.json")))
OR, CR, INKH = BRAND["colors"]["orange"], BRAND["colors"]["cream"], BRAND["colors"]["ink"]
# Zones de sécurité TikTok EN LIGNE (vérifiées sur capture 25/11 : barre « Rechercher » jusqu'à y≈250, recadrage latéral ~52 px) : haut 300 px, bas 420 px, côtés 120 px, colonne de boutons à droite (x > 940) sous y = 900.
SAFE_L, SAFE_R, SAFE_T = 120, 960, 300


def _svg_png(svg, w, h):
    import cairosvg, io
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=w, output_height=h))).convert("RGBA")


def bubble_img(w, h, fill):
    vb = " ".join(map(str, BRAND["bubble"]["viewbox"]))
    return _svg_png(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" preserveAspectRatio="none"><path fill="{fill}" d="{BRAND["bubble"]["outer"]}"/></svg>', w, h)


def wordmark_img(width, fill):
    x, y, w, h = BRAND["wordmark"]["bbox"]
    paths = "".join(f'<path d="{d}"/>' for d in BRAND["wordmark"]["paths"])
    hh = int(width * h / w)
    return _svg_png(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}"><g fill="{fill}">{paths}</g></svg>', width, hh)


def badge_img(size, slogan=False):
    """Bulle orange avec TellR (et le slogan) en crème."""
    bub = bubble_img(size, int(size * 430 / 400), OR)
    wm = wordmark_img(int(size * 0.68), CR)
    bub.alpha_composite(wm, (int(size * 0.13), int(size * (0.22 if slogan else 0.3))))
    if slogan:
        d = ImageDraw.Draw(bub)
        fs = font("Bold", max(12, int(size * 0.075)))
        d.text((size // 2, int(size * 0.62)), BRAND["slogan"], font=fs, fill=CR, anchor="mm")
    return bub


def hook_png(spec, path):
    """Accroche : la phrase choc dans une grande bulle orange, dans la zone de sécurité."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    bx, bw = SAFE_L, SAFE_R - SAFE_L
    pad = 70
    quote = "« " + spec["hook"] + " »"
    for size in (84, 76, 68, 60, 54):
        fq = font("Black", size)
        lines = wrap(d, quote, fq, bw - 2 * pad - 40)
        if len(lines) <= 4:
            break
    lh = int(size * 1.12)
    body_h = 64 + 58 + len(lines) * lh + 56
    bh = int(body_h / 0.76)          # la pointe occupe le bas de la bulle
    img.alpha_composite(bubble_img(bw, bh, OR), (bx, SAFE_T))
    y = SAFE_T + 64
    fn = font("Bold", 36)
    name = spec["guest"].upper()
    d.text((bx + pad, y), name, font=fn, fill=CR)
    cat = spec.get("category", "")
    if cat:
        x = bx + pad + d.textlength(name + "  ·  ", font=fn)
        d.text((bx + pad + d.textlength(name, font=fn), y), "  ·  ", font=fn, fill=CR)
        d.text((x, y), cat.upper(), font=fn, fill=INK)
    y += 58
    for l in lines:
        d.text((bx + pad, y), l, font=fq, fill=CR)
        y += lh
    img.save(path)


def caption_png(text, path):
    """Sous-titres dans une pastille crème, mot-clé en orange."""
    img = Image.new("RGBA", (W, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fc = font("Black", 70)
    lines = wrap(d, text, fc, W - 300)[:2]
    for i, line in enumerate(lines):
        words = line.split()
        total = sum(d.textlength(w.replace("*", "") + " ", font=fc) for w in words) - d.textlength(" ", font=fc)
        x, y = (W - total) / 2, 20 + i * 108
        d.rounded_rectangle([x - 30, y - 10, x + total + 30, y + 92], 26, fill=CR)
        for w in words:
            hl = w.startswith("*") or w.endswith("*")
            w2 = w.replace("*", "")
            d.text((x, y), w2, font=fc, fill=ACCENT if hl else INK)
            x += d.textlength(w2 + " ", font=fc)
    img.save(path)


def tag_png(spec, path):
    """Pendant le clip : badge TellR en haut à droite + crédit du streamer en haut à gauche."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    img.alpha_composite(badge_img(140), (SAFE_R - 140, SAFE_T))
    d = ImageDraw.Draw(img)
    src = spec.get("source", spec["guest"])
    f = font("Bold", 32)
    tw = d.textlength(src, font=f)
    d.rounded_rectangle([SAFE_L, SAFE_T + 10, SAFE_L + tw + 44, SAFE_T + 66], 28, fill=(0, 0, 0, 140))
    d.text((SAFE_L + 22, SAFE_T + 18), src, font=f, fill=(255, 255, 255))
    img.save(path)


def end_png(spec, path):
    """Écran de fin : alterne E (fond orange) et F (fond crème, leçon dans la bulle)."""
    style = spec.get("end_style") or "E"   # E = fond orange (validé) ; F (crème) abandonné le 24/11/2026
    if style == "E":
        img = Image.new("RGBA", (W, H), ACCENT + (255,))
        d = ImageDraw.Draw(img)
        d.text((130, 420), "À RETENIR", font=font("Bold", 44), fill=INK)
        for size in (88, 78, 68):
            ft = font("Black", size)
            lines = wrap(d, spec["takeaway"], ft, 800)
            if len(lines) <= 5:
                break
        for i, l in enumerate(lines):
            d.text((130, 490 + i * int(size * 1.18)), l, font=ft, fill=CREAM)
        # badge crème sur fond orange : on inverse les couleurs
        bub = bubble_img(420, int(420 * 430 / 400), CR)
        bub.alpha_composite(wordmark_img(int(420 * 0.68), OR), (int(420 * 0.13), int(420 * 0.22)))
        ImageDraw.Draw(bub).text((210, int(420 * 0.62)), BRAND["slogan"], font=font("Bold", 32), fill=OR, anchor="mm")
        img.alpha_composite(bub, (330, 1000))
        d.text((W // 2, 1560), "Abonne-toi pour la suite", font=font("Bold", 50), fill=CREAM, anchor="mm")
    else:
        img = Image.new("RGBA", (W, H), CREAM + (255,))
        d = ImageDraw.Draw(img)
        for size in (80, 72, 64, 58):
            ft = font("Black", size)
            lines = wrap(d, spec["takeaway"], ft, 760)
            if len(lines) <= 5:
                break
        lh = int(size * 1.15)
        bh = int((140 + len(lines) * lh + 60) / 0.76)
        img.alpha_composite(bubble_img(900, bh, OR), (90, 260))
        d.text((160, 320), "À RETENIR", font=font("Bold", 40), fill=INK)
        for i, l in enumerate(lines):
            d.text((160, 380 + i * lh), l, font=ft, fill=CREAM)
        y = 260 + bh + 70
        wm = wordmark_img(520, INKH)
        img.alpha_composite(bubble_img(150, 161, OR), (180, y))
        img.alpha_composite(wm, (360, y + 4))
        d.text((362, y + wm.size[1] + 30), BRAND["slogan"], font=font("Bold", 40), fill=INK)
        by = y + wm.size[1] + 110
        d.rounded_rectangle([140, by, 940, by + 100], 50, fill=ACCENT)
        d.text((W // 2, by + 50), "Abonne-toi pour la suite", font=font("Bold", 48), fill=CREAM, anchor="mm")
    img.convert("RGB").save(path)


def run(cmd):
    subprocess.run(cmd, check=True)


def main(spec_path, out):
    spec = json.load(open(spec_path))
    tmp = tempfile.mkdtemp(prefix="tellr_")
    dur = spec["end"] - spec["start"]
    hook_s = spec.get("hook_secs", 3.0)
    end_s = spec.get("end_secs", 3.5)

    # 1) base plein cadre 9:16 + zooms
    if "crop" in spec:
        x, y, w, h = spec["crop"]
        cropf = f"crop={w}:{h}:{x}:{y},"
    else:
        cropf = "crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',"
    z = "+".join(f"0.12*between(t,{a},{b})" for a, b in spec.get("zooms", [])) or "0"
    base = os.path.join(tmp, "base.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-ss", str(spec["start"]), "-t", str(dur), "-i", spec["src"],
         "-vf", f"{cropf}scale={W}:{H},scale=w='{W}*(1+{z})':h='{H}*(1+{z})':eval=frame,crop={W}:{H},setsar=1,fps=30",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-ar", "48000", "-ac", "2", base])

    # 2) calques
    hook_png(spec, os.path.join(tmp, "hook.png"))
    tag_png(spec, os.path.join(tmp, "tag.png"))
    inputs, filt, last = ["-i", base, "-i", os.path.join(tmp, "hook.png"), "-i", os.path.join(tmp, "tag.png")], [], "0:v"
    slide = f"if(lt(t,{hook_s}),0,-(t-{hook_s})*2600)"
    filt.append(f"[{last}][1:v]overlay=0:'{slide}':enable='lt(t,{hook_s + 0.5})'[v1]"); last = "v1"
    filt.append(f"[{last}][2:v]overlay=0:0:enable='gte(t,{hook_s})'[v2]"); last = "v2"
    caps = sorted(spec.get("captions", []), key=lambda c: c[0])
    caps = [[a, min(b, caps[i + 1][0] - 0.02) if i + 1 < len(caps) else b, t] for i, (a, b, t) in enumerate(caps)]
    for i, (a, b, text) in enumerate(caps):
        p = os.path.join(tmp, f"c{i}.png")
        caption_png(text, p)
        inputs += ["-i", p]
        idx = 3 + i
        filt.append(f"[{last}][{idx}:v]overlay=0:1300:enable='between(t,{a},{b})'[c{i}]"); last = f"c{i}"
    clip = os.path.join(tmp, "clip.mp4")
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", f"[{last}]", "-map", "0:a",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "copy", clip])

    # 3) carte « à retenir »
    end_png(spec, os.path.join(tmp, "end.png"))
    endv = os.path.join(tmp, "end.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", str(end_s), "-i", os.path.join(tmp, "end.png"),
         "-f", "lavfi", "-t", str(end_s), "-i", "anullsrc=r=48000:cl=stereo",
         "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-c:a", "aac", "-shortest", endv])

    # 4) assemblage
    run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-i", endv, "-filter_complex",
         "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", out])
    print("OK", out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
