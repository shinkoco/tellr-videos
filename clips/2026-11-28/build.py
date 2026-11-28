import json,subprocess
def cut(out,src,segs,vf):
    inp=[];f="";cat=""
    for i,(a,b) in enumerate(segs):
        inp+=["-ss",str(a),"-t",str(round(b-a,3)),"-i",src]
        f+=f"[{i}:v]fps=30,{vf.replace('#',str(i))},setsar=1[v{i}];[{i}:a]aresample=48000,afade=t=in:d=0.03,afade=t=out:st={b-a-0.04:.3f}:d=0.04[a{i}];"
        cat+=f"[v{i}][a{i}]"
    f+=cat+f"concat=n={len(segs)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg","-v","error","-y",*inp,"-filter_complex",f,"-map","[v]","-map","[a]","-c:v","libx264","-preset","veryfast","-crf","18","-c:a","aac",out],check=True)
def make(tag,src,segs,vf,caps,zooms,es,meta,crop=None):
    cut(f"c_{tag}.mp4",src,segs,vf)
    def tl(t):
        off=0
        for a,b in segs:
            if a-0.4<=t<=b+0.4: return round(off+min(max(t,a),b)-a,2)
            off+=b-a
        raise ValueError(t)
    end=round(sum(b-a for a,b in segs),2)
    spec=dict(src=f"c_{tag}.mp4",start=0,end=end,captions=[[tl(a),tl(b),t] for a,b,t in caps],zooms=[[tl(a),tl(b)] for a,b in zooms],end_secs=es,**meta)
    if crop: spec["crop"]=crop
    json.dump(spec,open(tag+".json","w"),ensure_ascii=False,indent=1); print(tag,end+es)
make("tellr_lefrenchie_dafoe","daf.mp4",[(4.55,31.9),(40.6,45.4),(56.1,61.3),(63.5,69.8),(77.15,83.05),(91.1,100.9)],"null",[
(4.6,6.7,"Et tu perds énormément de *confort*"),(6.7,9.4,"par rapport à un appartement, à une maison,"),(9.4,11.0,"parce que t'as pas les ressources *illimitées*."),(11.0,12.5,"Donc là, où en moyenne un Français…"),
(14.75,15.8,"C'est *Willem Dafoe* !"),(16.0,16.8,"Je ne déconne pas,"),(16.9,18.5,"c'est l'acteur du *Bouffon Vert* dans Spider-Man."),(19.4,20.3,"Je ne déconne pas."),(21.55,23.1,"J'ai vu sa tête de *face*, c'est lui."),(24.6,25.8,"Avec la veste en *cuir*, ouais."),(26.0,27.2,"Je ne déconne pas, c'était lui."),(27.25,29.0,"Alors attends, je vais pas aller le *chasser*"),(30.25,31.7,"mais je vous *promets* que c'est lui."),
(40.7,41.6,"Attends, on le voit plus."),(43.2,45.2,"On l'a *perdu* de vue."),
(56.2,57.7,"Au milieu du passage *piéton* !"),(59.1,61.2,"Là-bas, il est en train de *traverser*."),
(63.6,65.7,"Ah non, c'est même pas de *dos*, les amis."),(65.8,67.4,"J'ai vu sa tête de *face*."),(67.9,69.0,"J'ai vu sa tête de face."),(69.3,69.75,"C'est *lui*."),
(77.2,79.1,"C'est lui, je *confirme*, je l'ai reconnu aussi."),(79.9,81.5,"J'ai pas le temps de tourner la *caméra*"),(81.5,83.0,"assez rapidement pour que vous voyiez."),
(91.2,92.7,"En vrai, on n'en croise pas tant que ça,"),(92.8,93.7,"mais tu vas en *croiser*."),(93.75,95.7,"Si tu viens ici, tu vas forcément croiser quelqu'un,"),(95.75,96.8,"toutes les deux semaines, un mois."),(96.9,98.4,"La dernière fois, on avait croisé […],"),(98.5,100.7,"là, on a croisé *Willem Dafoe*.")],
[(14.75,16.0),(67.9,69.8),(98.5,100.8)],4.0,
dict(guest="LeFrenchie",category="Drôle",hook="J'ai vu sa tête de face, c'est lui.",context="En live à New York, LeFrenchie assure reconnaître Willem Dafoe.",source="LeFrenchie · Twitch",takeaway="En live, la rue peut couper la parole à tout moment."),crop=[540,0,405,720])
make("tellr_littlebigwhale_chats","lbw.mp4",[(0,37.1),(39.8,60.0)],"null",[
(0.0,1.2,"Sur l'application, récemment,"),(1.6,2.6,"c'est un *banger*."),(4.2,6.6,"Il y a des *vlogs*, ils font des vlogs."),(9.6,11.3,"Je trouve ça *énorme*."),(11.7,13.0,"Du coup, ça fait des vlogs avec…"),
(15.55,16.9,"Regardez, ça, c'est *Mickey*."),(17.4,20.0,"Ça, c'est *Mouchou* qui vient manger."),(20.6,23.9,"Ça fait des petits montages comme ça,"),(24.4,26.6,"des chats qui apparaissent devant la *cam*."),(28.0,29.0,"Non mais n'importe quoi !"),
(29.4,31.9,"Et c'est une gamelle où tu peux lui *parler*."),(32.4,34.0,"Si un chat arrive, et c'est pas *ton* chat,"),(34.0,36.1,"il vient manger les *croquettes* de ton chat,"),(36.1,36.95,"tu peux faire « *wow* » !"),
(40.0,42.2,"Et ça me fait des *avant-après*."),(43.6,45.0,"Regardez, là, c'était à"),(45.0,47.4,"*6 h 09* et 52 secondes du matin."),(49.9,52.0,"Là, on voit l'animal en fond,"),(52.4,54.7,"on voit l'auteur du *crime*"),(54.75,56.4,"et les petites croquettes dans la gamelle,"),(56.5,57.7,"juste devant la *gamelle*."),(58.8,60.0,"Et là, c'était à *6 h 09*…")],
[(52.4,54.7),(36.1,37.0)],4.5,
dict(guest="LittleBigWhale",category="Insolite",hook="On voit l'auteur du crime",context="LittleBigWhale montre les vidéos de la gamelle de ses chats.",source="LittleBigWhale · Twitch",takeaway="Une caméra sur la gamelle, et les croquettes n'ont plus de secrets."),crop=[790,0,608,1080])
make("tellr_debrief_psg_dembele","dem.mp4",[(0,54.97)],"split[x#][y#];[x#]crop=ih*9/16:ih,scale=1080:1920,gblur=sigma=40,eq=brightness=-0.25[bg#];[y#]scale=1080:-2[fg#];[bg#][fg#]overlay=0:650",[
(0.5,2.2,"Même si bien sûr il y a ces grands *absents*,"),(2.2,5.8,"on avait quand même envie de voir une *animation*."),(5.8,7.9,"Je trouve que *Mayulu* s'en est sorti le mieux."),(8.7,10.55,"[…] la période actuelle n'est pas évidente,"),(10.6,11.4,"même s'il a marqué à Nice."),(11.4,13.2,"Par contre, assez déçu du match d'*Akliouche*,"),(13.2,15.6,"qui était un joueur qui montait en *puissance*."),(15.6,17.3,"Alors peut-être que c'est un accident"),(17.3,20.0,"et son premier vrai *raté*, il va rebondir."),
(20.0,21.5,"Par contre, j'ai vraiment senti la *différence*"),(21.5,22.5,"quand *Dembélé* est rentré."),(23.6,26.3,"La maîtrise technique, le supplément d'*âme*."),(26.35,29.35,"J'ai vu le *leader* offensif du PSG, c'était lui."),(29.45,31.6,"S'il n'y a pas Dembélé qui est à *100 %*"),(31.6,32.4,"toute la saison,"),(32.4,34.6,"ça va être très compliqué de viser ce *triplé*."),
(34.65,36.0,"Il y a la question d'aller chercher"),(36.0,37.65,"une *recrue* supplémentaire."),(37.8,40.5,"On avait focus cette animation offensive."),(40.75,42.1,"Des joueurs ont beaucoup apporté."),(42.15,44.4,"*Hakimi* a été très généreux dans son couloir,"),(44.45,46.8,"sur sa heatmap, il doit être un *ailier*."),
(47.05,49.2,"C'est vrai qu'on s'attendait à une Roma"),(49.2,50.15,"peut-être *fébrile*,"),(50.15,51.9,"vu la compo de départ de *Gasperini*,"),(51.9,53.5,"mais les joueurs voulaient se montrer"),(53.5,54.6,"et ont été bons au *pressing*.")],
[],6.2,
dict(guest="Débrief PSG-Roma",category="Sport",hook="J'ai vu le leader offensif du PSG, c'était lui.",context="Après le 2-2 contre la Roma, débrief en direct chez BruceGrannec.",source="BruceGrannec · Twitch",takeaway="D'après ce débrief, le PSG a besoin d'un Dembélé en pleine forme."))
