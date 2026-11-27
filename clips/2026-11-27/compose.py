import json,subprocess
def cut(out,segs,crop,w,y):
    inp=[];f="";cat=""
    for i,(src,a,b) in enumerate(segs):
        inp+=["-ss",str(a),"-t",str(round(b-a,3)),"-i",src+".mp4"]
        f+=f"[{i}:v]fps=30,split[x{i}][y{i}];[x{i}]crop=ih*9/16:ih,scale=1080:1920,gblur=sigma=40,eq=brightness=-0.25[bg{i}];[y{i}]crop={crop},scale={w}:-2[fg{i}];[bg{i}][fg{i}]overlay=(W-w)/2:{y},setsar=1[v{i}];[{i}:a]aresample=48000,afade=t=in:d=0.03,afade=t=out:st={b-a-0.04}:d=0.04[a{i}];"
        cat+=f"[v{i}][a{i}]"
    f+=cat+f"concat=n={len(segs)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg","-v","error","-y",*inp,"-filter_complex",f,"-map","[v]","-map","[a]","-c:v","libx264","-preset","veryfast","-crf","18","-c:a","aac",out],check=True)
def tl(segs,src,t):
    off=0
    for s,a,b in segs:
        if s==src and a-0.35<=t<=b+0.35: return round(off+min(max(t,a),b)-a,2)
        off+=b-a
    raise ValueError((src,t))
def make(tag,segs,caps,crop,w,y,meta,zooms,es):
    cut(f"c_{tag}.mp4",segs,crop,w,y)
    c=[[tl(segs,s,a),tl(segs,s,b),t] for s,a,b,t in caps]
    z=[[tl(segs,s,a),tl(segs,s,b)] for s,a,b in zooms]
    end=round(sum(b-a for _,a,b in segs),2)
    spec=dict(src=f"/home/claude/w/c_{tag}.mp4",start=0,end=end,captions=c,zooms=z,end_secs=es,**meta)
    json.dump(spec,open(tag+".json","w"),ensure_ascii=False,indent=1); print(tag,end+es)
J="jdg";K="jdg2"
make("tellr_jdg_alertes",[(J,0,5.6),(K,0,35.6),(K,38.8,51.0),(K,53.0,60.0)],[
(J,0,1.5,"Comment on désactive ça ?"),(J,1.8,2.6,"Je comprends *rien*,"),(J,2.6,5.4,"c'est pas moi qui le fais d'habitude."),
(K,0,2.5,"Comment on désactive ces trucs *pourris* ?"),(K,3.0,5.9,"Oh là là, comment on fait ?"),(K,6.2,8.0,"Comment ça marche ?"),(K,8.3,10.6,"Arrêtez, c'est *nul* !"),
(K,13.0,14.8,"Comment on fait ?"),(K,14.9,16.8,"Comment on désactive ces *trucs-là* ?"),(K,21.4,23.2,"Oh là là, vas-y."),
(K,29.5,31.0,"Oui mais *où* ?"),(K,31.2,32.8,"Attends."),(K,39.5,40.6,"Mais non, c'est pas ça."),(K,40.7,43.2,"En fait, ça doit être un truc à désactiver"),(K,43.2,44.2,"dans *Streamlabs*."),(K,45.0,46.5,"*Streamlabs*,"),(K,46.6,49.9,"ils ont dû le ranger dans une sous-catégorie *obscure*."),
(K,53.8,55.4,"Parce qu'évidemment, tu te dis :"),(K,55.4,56.5,"ça va être dans *Fenêtre d'alerte*,"),(K,56.5,58.0,"mais bien sûr que *non*."),(K,58.0,59.9,"Ça serait *trop simple* !")],
"900:900:430:0",1080,430,dict(guest="Joueur du Grenier",category="Drôle",hook="Arrêtez, c'est nul !",context="Joueur du Grenier cherche comment désactiver une alerte en plein live.",source="Joueur du Grenier · Twitch",takeaway="En live, le réglage le plus simple est parfois le mieux caché."),[(K,8.3,10.6),(K,56.5,59.9)],4.0)
A="arcom1";B="arcom2"
make("tellr_massiet_arcom",[(A,26.7,34.0),(A,37.0,48.2),(A,52.4,55.2),(B,0,13.1),(B,14.0,21.7),(B,22.4,26.6),(B,29.4,42.2),(B,43.4,51.5)],[
(A,26.8,28.0,"Là, j'ai commencé à avoir"),(A,28.0,30.9,"des textos de *journalistes*"),(A,31.0,33.0,"qui me demandent une *réaction*."),(A,33.1,34.0,"Réaction à *quoi* ?"),
(A,37.2,39.4,"Je mets GTA sur *pause*,"),(A,40.5,42.0,"je vais me clarifier l'esprit"),(A,42.1,44.4,"parce qu'il doit se passer un truc."),(A,44.7,45.9,"Je regarde mon téléphone"),(A,46.1,48.2,"et je vois les annonces de l'*Arcom*."),(A,52.5,55.2,"Je me lève de mon canapé : attends, *quoi* ?"),
(B,0,2.0,"On est dans une situation"),(B,2.0,4.8,"dans laquelle je ne vais pas respecter des règles de l'*Arcom*,"),(B,4.9,7.0,"qu'elles me soient applicables ou pas."),(B,7.0,8.3,"Je ne les *respecterai pas*."),
(B,8.8,10.8,"J'invite tous les *créateurs* de contenu"),(B,10.8,13.1,"concernés à ne pas respecter cette règle."),(B,14.1,16.4,"Vous êtes libres d'interviewer"),(B,16.4,18.2,"tous les candidats à la *présidentielle*"),(B,18.2,19.9,"pendant le temps que vous voulez"),(B,19.9,21.7,"et de leur poser les questions que vous voulez."),
(B,22.5,24.4,"Les candidats sont libres de créer leur *chaîne YouTube*"),(B,24.5,26.6,"s'ils trouvent qu'ils n'ont pas assez de temps de parole."),
(B,29.5,32.5,"Et si jamais un créateur de contenu"),(B,32.5,35.7,"se retrouve traîné en *justice* pour ne pas avoir interviewé […],"),(B,37.2,40.2,"je paierai ses frais de justice *personnellement*,"),(B,41.1,42.1,"s'il le souhaite."),
(B,43.5,46.0,"C'est dans ces moments-là qu'il faut être *solidaires*,"),(B,46.1,48.4,"parce que c'est un peu facile de s'en prendre"),(B,48.4,51.3,"à des créateurs très *isolés* les uns des autres.")],
"890:960:670:0",1080,430,dict(guest="Jean Massiet",category="Actu",hook="Je ne les respecterai pas",context="Jean Massiet réagit en live aux règles de l'Arcom pour la présidentielle 2027.",source="Jean Massiet · Twitch",takeaway="Les règles de l'Arcom pour 2027 sont contestées par des créateurs."),[(B,7.0,8.3),(B,37.2,40.2)],4.5)
C="clem";T="tun"
make("tellr_clem_animateur",[(C,0,17.75),(C,32.3,54.0),(T,0,14.95),(T,15.7,29.5)],[
(C,0,2.4,"Et avoir PA qui nous *carry* comme ça !"),(C,2.5,4.5,"Tu te rends compte de la différence de *niveau*"),(C,4.6,7.1,"et de capacité à tenir un *stream* ?"),(C,7.7,11.2,"Dès qu'il dit ses premières phrases,"),(C,11.4,14.4,"qu'il anime et qu'il donne à sa gauche,"),(C,14.5,17.7,"il *rebondit*, c'est trop agréable."),
(C,32.4,33.9,"Quand il est arrivé au domaine,"),(C,33.9,35.4,"j'ai vu un *autre PA*."),(C,35.7,38.0,"Un PA en mission *professionnelle*."),(C,39.4,41.6,"Il avait l'air stressé, mais il le cache mieux que nous."),(C,42.1,44.2,"Il avait juste l'air *concentré*."),(C,44.3,47.2,"Et il a juste *carry de fou* le live."),(C,47.4,50.5,"Caster *25 heures* un événement sur un sport où tu n'es pas pro,"),(C,50.6,53.9,"un événement que tu ne maîtrises pas…"),
(T,0,2.4,"Imagine, je lance un truc *nul*"),(T,2.4,4.9,"pendant le live, un sujet"),(T,4.9,7.0,"qui est un *cul-de-sac*,"),(T,7.0,9.9,"qu'il faut pas commencer parce qu'en live ça rend pas bien."),(T,10.3,13.3,"Direct, tu le sors, t'es là : ouais, OK…"),(T,13.4,14.95,"« J'ai vu une question dans le chat. »"),
(T,15.8,17.7,"Il est trop *fort*, il carry de ouf !"),(T,19.0,20.2,"C'est ce qui me *rassurait*."),(T,23.6,25.3,"Il carry de ouf,"),(T,25.4,27.7,"en vrai, t'as juste à t'*asseoir*"),(T,27.7,29.4,"et il fait le live.")],
"1180:810:280:150",1080,540,dict(guest="ClemQuiCourt",category="Coulisses",hook="Il a juste carry de fou le live",context="Débrief de leurs 25 heures en direct : ce que l'animateur PA leur a apporté.",source="ClemQuiCourt · Twitch",takeaway="Un bon animateur rend le live plus simple pour tous."),[(C,44.3,47.2),(T,25.4,29.4)],4.5)
