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
  "hook_secs": 3.0, "end_secs": 3.5
}
Charte provisoire : couleur ACCENT, police Inter Display. À remplacer par la charte TELLR.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
ACCENT = (255, 106, 26)
INK = (20, 18, 16)
CREAM = (246, 241, 233)
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


def hook_png(spec, path):
    img = Image.new("RGBA", (W, 640), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fq = font("Black", 88)
    lines = wrap(d, "« " + spec["hook"] + " »", fq, W - 140)[:3]
    h = 190 + len(lines) * 104 + 110
    d.rectangle([0, 0, W, h], fill=ACCENT + (255,))
    d.text((70, 100), spec["guest"].upper(), font=font("Bold", 38), fill=(255, 255, 255))
    for i, l in enumerate(lines):
        d.text((70, 160 + i * 104), l, font=fq, fill=INK)
    ctx = spec.get("context", "")
    if ctx:
        fc = font("SemiBold", 34)
        tw = d.textlength(ctx, font=fc)
        y = 160 + len(lines) * 104 + 20
        d.rounded_rectangle([70, y, 70 + tw + 60, y + 60], 30, fill=INK)
        d.text((100, y + 8), ctx, font=fc, fill=(255, 255, 255))
    img.save(path)


def caption_png(text, path):
    img = Image.new("RGBA", (W, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    fc = font("Black", 76)
    lines = wrap(d, text, fc, W - 160)[:2]
    for i, line in enumerate(lines):
        words = line.split()
        total = sum(d.textlength(w.replace("*", "") + " ", font=fc) for w in words)
        x, y = (W - total) / 2, 20 + i * 96
        for w in words:
            hl = w.startswith("*") or w.endswith("*")
            w2 = w.replace("*", "")
            d.text((x + 4, y + 5), w2, font=fc, fill=(0, 0, 0, 200))
            d.text((x, y), w2, font=fc, fill=ACCENT if hl else (255, 255, 255))
            x += d.textlength(w2 + " ", font=fc)
    img.save(path)


def tag_png(spec, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([W - 230, 70, W - 60, 130], 10, fill=(255, 255, 255))
    d.text((W - 210, 76), "TELLR", font=font("Black", 40), fill=INK)
    d.text((70, 1760), "Source : " + spec.get("source", spec["guest"]), font=font("SemiBold", 34), fill=(235, 235, 235))
    img.save(path)


def end_png(spec, path):
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 16], fill=ACCENT)
    d.rounded_rectangle([70, 520, 420, 590], 35, fill=ACCENT)
    d.text((105, 530), "À RETENIR", font=font("Black", 44), fill=INK)
    ft = font("Black", 88)
    lines = wrap(d, spec["takeaway"], ft, W - 140)[:4]
    for i, l in enumerate(lines):
        d.text((70, 640 + i * 106), l, font=ft, fill=INK)
    d.text((70, 660 + len(lines) * 106), "Extrait : " + spec.get("source", spec["guest"]), font=font("SemiBold", 36), fill=(110, 100, 90))
    d.rounded_rectangle([70, 1500, 1010, 1640], 24, fill=INK)
    d.text((140, 1530), "Abonne-toi pour la suite", font=font("Black", 64), fill=(255, 255, 255))
    d.text((70, 1720), "TELLR", font=font("Black", 72), fill=INK)
    img.save(path)


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
    for i, (a, b, text) in enumerate(spec.get("captions", [])):
        p = os.path.join(tmp, f"c{i}.png")
        caption_png(text, p)
        inputs += ["-i", p]
        idx = 3 + i
        filt.append(f"[{last}][{idx}:v]overlay=0:1280:enable='between(t,{a},{b})'[c{i}]"); last = f"c{i}"
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
