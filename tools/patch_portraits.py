import sys
from PIL import Image, ImageDraw
S=sys.argv[1]
g=Image.open('/mnt/project-files/oikumena/images/sards/gerb-sardov.png').convert('RGBA'); w,h=g.size
m=Image.new('L',(w,h),0); ImageDraw.Draw(m).ellipse((int(w*.035),int(h*.035),int(w*.965),int(h*.965)),fill=255)
g.putalpha(m); g.resize((240,240),Image.LANCZOS).save(S+'/pub/img/arms-sardy.png',optimize=True)
p=S+'/pub/index.html'; s=open(p).read()
def rep(a,b):
    global s
    assert a in s, a[:60]
    s=s.replace(a,b,1)
rep(".face.more{",".face img{width:100%;height:100%;object-fit:cover;display:block}\n.face.pic{padding:0;overflow:hidden;border-color:var(--gold)}\n.phead img.arms,.rlabel img.arms{flex:none;border-radius:50%;box-shadow:0 0 0 3px var(--gold),0 3px 8px rgba(0,0,0,.6)}\n.house li{display:flex;gap:10px;align-items:flex-start}\n.house li .face{flex:none;width:44px;height:44px}\n.face.more{")
rep("/* ---------- Герб ---------- */","""/* ---------- Портреты и гербы-картинки (из сводки персонажей) ---------- */
const PORTRAITS=[[/Олаф Сард/,'img/p-olaf-sard.jpg'],[/Юсти(на|ана).*Калифакт/,'img/p-yustiana-kalifakt.jpg'],[/Амала Сард/,'img/p-amala-sard.jpg'],[/Тересия Сард/,'img/p-teresiya-sard.jpg']];
const portrait=n=>{const p=PORTRAITS.find(([r])=>r.test(n));return p?p[1]:null};
const ARMS_IMG={'Хеортания':'img/arms-sardy.png','Аммалингия':'img/arms-sardy.png'}; // герб дома Сардов
/* ---------- Герб ---------- */""")
rep("function arms(st,size){\n","function arms(st,size){\n  if(st&&ARMS_IMG[st.id]){const z=size||64;return `<img class=\"arms\" src=\"${ARMS_IMG[st.id]}\" width=\"${z}\" height=\"${z}\" alt=\"Герб: ${esc(st.title)}\">`}\n")
rep("const shown=list.slice(0,max).map(m=>`<div class=\"face\" title=\"${esc(m.name)}\">${esc(initials(m.name))}</div>`).join('');",
 "list=[...list].sort((a,b)=>(portrait(b.name)?1:0)-(portrait(a.name)?1:0));\n  const shown=list.slice(0,max).map(face).join('');")
rep("function faces(list,max){","function face(m){const p=portrait(m.name);return p?`<div class=\"face pic\" title=\"${esc(m.name)}\"><img src=\"${p}\" alt=\"${esc(m.name)}\" loading=\"lazy\"></div>`:`<div class=\"face\" title=\"${esc(m.name)}\">${esc(initials(m.name))}</div>`}\nfunction faces(list,max){")
rep("<ul>${H.members.map(m=>`<li><b>","<ul>${H.members.map(m=>`<li>${portrait(m.name)?face(m):''}<div><b>")
rep("''))}</span>`:''}</li>`","''))}</span>`:''}</div></li>`")
open(p,'w').write(s)
print('ok')
