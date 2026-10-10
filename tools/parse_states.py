import re, json, glob, os, sys
root = sys.argv[1]
def cells(line): return [c.strip() for c in line.strip().strip('|').split('|')]
def strip_md(s): return re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s).replace('**','').replace('★','').strip()
states=[]; settlements=[]; provinces=[]
files=sorted(glob.glob(root+'/states/*/*.md'))+[root+'/states/99_Ничьи_земли.md']
for fp in files:
    txt=open(fp).read(); lines=txt.split('\n')
    title=lines[0].lstrip('# ').strip()
    sid=os.path.basename(fp)[:-3]
    card={}; cur_prov=None; mode=None; prov_info={}
    for i,l in enumerate(lines):
        if l.startswith('## '):
            mode=l[3:].strip(); cur_prov=None
            if fp.endswith('99_Ничьи_земли.md') and mode.startswith('В'):
                cur_prov = None if mode=='Вне областей' else re.sub(r'.*«(.+)».*', r'\1', mode)
            continue
        if l.startswith('### ') and mode=='Провинции':
            cur_prov=l[4:].strip(); prov_info={'name':cur_prov,'state':sid}; provinces.append(prov_info); continue
        if not l.startswith('|') or set(l.replace('|','').strip())<=set('-: '): continue
        c=cells(l)
        if mode=='Карточка государства' and len(c)==2 and c[0]!='Поле': card[c[0]]=re.sub(r'\s*·\s*\[[^\]]*\]\([^)]*\)','',c[1]).strip()
        elif mode=='Провинции' and cur_prov and len(c)==2 and c[0]!='Поле':
            if c[0].startswith('Центр'):
                x,y=[int(v) for v in re.findall(r'\d+',c[1])[:2]]; prov_info['cx']=x; prov_info['cy']=y
            elif c[0].startswith('Площадь'): prov_info['area']=c[1]
            elif c[0].startswith('Где'): prov_info['where']=c[1]
            elif c[0]=='Тип провинции': prov_info['ptype']=strip_md(c[1])
            elif c[0]=='Владелец': prov_info['owner']=strip_md(c[1])
            elif c[0]=='Наместник': prov_info['governor']=strip_md(c[1])
            elif c[0]=='Название в атласе': prov_info['atlas']=strip_md(c[1])
        elif len(c)==7 and c[0]!='Поселение':
            xy=re.findall(r'\d+',c[5])
            if len(xy)<2: continue
            settlements.append(dict(name=strip_md(c[0]),capital='★' in c[0],type=c[1],ruler=c[2],status=c[3],roads=c[4],
                x=int(xy[0]),y=int(xy[1]),note=c[6],state=sid,province=cur_prov or ''))
    m=re.search(r'## Хроника\n(.*?)\n## ',txt,re.S)
    chron=[strip_md(x[2:]) for x in m.group(1).split('\n') if x.startswith('- ')] if m else []
    arms=re.search(r'поле `(#[0-9a-f]{6})`, фигура «(\w+)»',card.get('Герб',''))
    states.append(dict(id=sid,title=title,full=card.get('Полное название',title),bloc=card.get('Блок',''),ruler=card.get('Правитель',''),
        capital=card.get('Столица',''),area=card.get('Площадь, тыс. км²',''),color=card.get('Цвет на карте','').strip('`'),
        neighbors=strip_md(card.get('Соседи','')),note=card.get('Заметки',''),
        arms={'field':arms.group(1),'charge':arms.group(2)} if arms else None,chronicle=chron,
        file=os.path.relpath(fp,root)))
idx=open(root+'/states/index.md').read()
roads=[]
for m in re.finditer(r'- \*\*(.+?)\*\*, ≈(\d+) км: (.+)',idx):
    roads.append(dict(name=m.group(1),km=int(m.group(2)),via=[s.strip() for s in m.group(3).split('→')]))
json.dump(dict(states=states,provinces=provinces,settlements=settlements,roads=roads),open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
print(len(states),len(provinces),len(settlements),len(roads))
names={s['name'] for s in settlements}
print([v for r in roads for v in r['via'] if v not in names])
print([p['name'] for p in provinces if 'cx' not in p])
