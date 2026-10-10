import re, json, sys
txt=open(sys.argv[1]).read()
blocks=[]; cur=None
for l in txt.split('\n'):
    m=re.match(r'^## (.+)',l)
    b=re.match(r'^\*\*(.+?)\.\*\*\s*(.*)',l)
    if m and not m.group(1).startswith(('Гербы','Противоречия','Источники')):
        h=re.sub(r'\s*\[А\d\]','',m.group(1)); cur=dict(name=h,desc='',members=[]); blocks.append(cur); continue
    if m: cur=None; continue
    if l.startswith('# '): cur=None; continue
    if b:
        cur=dict(name=b.group(1),desc=b.group(2),members=[]); blocks.append(cur); continue
    if cur is None: continue
    if l.startswith('- **'):
        mm=re.match(r'- \*\*(.+?)\*\*(.*)',l); rest=mm.group(2).strip().lstrip(',').strip()
        cur['members'].append(dict(name=mm.group(1).rstrip('.'),text=rest))
    elif l.strip() and not l.startswith(('- _','---')) and not cur['members']:
        cur['desc']=(cur['desc']+' '+l.strip()).strip()
blocks=[b for b in blocks if b['members'] or b['desc']]
json.dump(blocks,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
for b in blocks: print(b['name'],'|',len(b['members']),'|',b['desc'][:60])
