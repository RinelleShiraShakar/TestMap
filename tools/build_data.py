import json, re, sys
from PIL import Image
S=sys.argv[1]; OUT=sys.argv[2]
d=json.load(open(S+'/states.json')); houses=json.load(open(S+'/houses.json'))
mask=Image.open(S+'/zip/regions.png'); W,H=mask.size; px=mask.load()
def rid(x,y):
    x//=4; y//=4
    if 0<=x<W and 0<=y<H: return px[x,y]
    return 0
provs=[p for p in d['provinces'] if 'cx' in p]
for p in provs: p['rid']=rid(p['cx'],p['cy'])
ids=[p['rid'] for p in provs]; print('prov rids',sorted(ids), len(set(ids)))
byrid={p['rid']:p for p in provs if p['rid']}
for s in d['settlements']:
    r=rid(s['x'],s['y']); s['rid']=r
    if s['province'] in ('Поселения в чужих провинциях','') and r in byrid: s['province']=byrid[r]['name']
    if s['province']=='Поселения в чужих провинциях': s['province']=''
# Решения Nerissa в треде сборки, поверх каталога государств
# 2026-10-10: «Допустим жива.» — Лагерта Тебриксдоттер жива; правит Сигвартами (вывод сборки)
for st in d['states']:
    if st['id']=='Сигварты':
        st['ruler']='Лагерта Тебриксдоттер'
        st['chronicle']=[c for c in st['chronicle'] if 'Лагерта' not in c]
for x in d['settlements']:
    if x['name']=='Сигварты':
        x['ruler']='Лагерта Тебриксдоттер'
        if 'Лагерта' in x['note']: x['note']='—'
# houses per state
HS={'Империя':['Дом Неретцес'],'Этерналия':['Дом Калифакт'],'Аммалингия':['Племя Сардов'],'Хеортания':['Племя Сардов'],
 'Церковь_Геи':['Церковники'],'Пиррет':['Дом Астрарий'],'Маринари':['Дом Маринари','Род Лонгов'],'Южные_земли':['Дом Эль Бранте'],
 'Бергамо_и_Аэномосберг':['Дом Висконти'],'Северные_Владыки':['Род Васильевых'],'Хиндъяльф':['Род Саксов'],
 'Северное_королевство':['Род Рагнаров из Категада','Род Рихтеров'],'Нью-Борк_и_Нестегард':['Рагнары из Нью-Борка'],
 'Калева':['Род Калева'],'Конфедерация_Тервингов':['Род Тервингов','Род Герулов','Род Алеманнов','Род Лукне','Род Вэш','Род Хеортанов'],
 'Гетское_королевство':['Род Аммалингов из Архмайера','Аммалы из Готесбурга','Аммалинги из Амалабурга','Род Эйзингеров'],
 'Королевство_Торвигов':['Род Торвигов','Род Рейнов','Род Крагмаров'],'Кархевальд':['Род Хеортанов','Род Кархевальда','Аммалы из Хеортума','Род Дунабхельма'],
 'Туран':['Род Сарг-Улгура'],'Данники_Турана':['Аммалы из Арирхайла'],'Сигварты':['Род Барбариенсов']}
def hfind(prefix): 
    for i,h in enumerate(houses):
        if h['name'].startswith(prefix): return i
    raise SystemExit('no house '+prefix)
for st in d['states']: st['houses']=[hfind(p) for p in HS.get(st['id'],[])]
SET={'Торсвик':'Род Кертов','Остия':'Род Лонгов','Категат':'Род Рагнаров из Категада','Архмайер':'Род Аммалингов из Архмайера',
 'Готесбург':'Аммалы из Готесбурга','Амалабург':'Аммалинги из Амалабурга','Эйзингеры':'Род Эйзингеров','Хеортум':'Аммалы из Хеортума',
 'Рейн':'Род Рейнов','Крагма':'Род Крагмаров','Торвиги':'Род Торвигов','Алеманны':'Род Алеманнов','Герулы':'Род Герулов','Лукне':'Род Лукне',
 'Вэш':'Род Вэш','Тервинги':'Род Тервингов','Аэномосберг':'Дом Маринари','Сарды':'Племя Сардов','Арирхайл':'Аммалы из Арирхайла','Равнскол':'Род Кертов'}
stmap={s['id']:s for s in d['states']}
for s in d['settlements']:
    h=None
    if s['name'] in SET: h=hfind(SET[s['name']])
    else:
        for i,hh in enumerate(houses):
            for m in hh['members']:
                parts=m['name'].split()
                if len(parts)>=2 and re.search(r'(?<!\w)'+re.escape(parts[-2])+r'(?!\w)',s['ruler']) and re.search(r'(?<!\w)'+re.escape(parts[-1][:5]),s['ruler']) and h is None: h=i
        if h is None and stmap[s['state']]['houses']: h=stmap[s['state']]['houses'][0]
    s['house']=h
# roads polylines
pos={s['name']:(s['x'],s['y']) for s in d['settlements']}
for r in d['roads']: r['pts']=[pos[v] for v in r['via']]
# culture (only where the notes say it plainly)
CUL={'imp':{'name':'Имперская культура','faith':'Церковь Матери Геи'},'west':{'name':'Западные Кровные (степняки)','faith':'Сотни духов'}}
for st in d['states']:
    if st['bloc']=='Империя': st['culture']='imp'
    elif st['id']=='Туран': st['culture']='west'
    else: st['culture']=None
    if st['id']=='Северные_Владыки': st['faith']='Каллерой (единственный имперский дом этой веры)'
CULTXT={'imp':'Империя считает себя основательницей цивилизации и существующей с первого дня Кары. Ценит дисциплину и порядок. Фактически это теократия под видом империализма: слово Понтифика может переломить расстановку домов. Власть основана на божественном праве и крови.',
 'west':'Степняки, самый свободолюбивый народ. Небо им потолок, стен не признают, боевой конь — друг. Нет слуг и рабов, только «помощники». Уважение к вождю держится на харизме.'}
for k in CUL: CUL[k]['text']=CULTXT[k]
data=dict(map={'w':2035,'h':4096,'maskScale':4},states=d['states'],provinces=provs,settlements=d['settlements'],roads=d['roads'],houses=houses,cultures=CUL)
open(OUT,'w').write('window.OIK='+json.dumps(data,ensure_ascii=False)+';')
print('no house:',[s['name'] for s in d['settlements'] if s['house'] is None])
print('no prov:',[s['name'] for s in d['settlements'] if not s['province']])
print([(s['name'],houses[s['house']]['name']) for s in d['settlements'] if s['house'] is not None][:80])
