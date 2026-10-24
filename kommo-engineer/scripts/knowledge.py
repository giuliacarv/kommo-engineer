"""Compact, accent-insensitive retrieval and package coverage checks."""
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s.casefold()) if not unicodedata.combining(c))

def find(query):
    words = set(re.findall(r'[\w-]+', norm(query))) - {'de','do','da','o','a','qual','configurar','escolher'}
    cat = json.loads((ROOT/'references/knowledge/catalog.json').read_text(encoding='utf-8'))
    results=[]
    for item in cat['procedures']:
        title=norm(item['title']+' '+item['id'])
        extra=norm(json.dumps({k:item.get(k,[]) for k in ('keywords','aliases','prerequisites','screenshots','related')},ensure_ascii=False))
        score=sum((4 if w in title else 1 if w in extra else 0) for w in words)
        if words=={'salesbot'} and item['id']=='PROC-KOMMO-005':score+=10
        if score:
            results.append({k:item[k] for k in ('id','title','path','status')} | dict(score=score,screenshots=item.get('screenshots',[]),gaps=item.get('gaps',[]),related=item.get('related',[])))
    return sorted(results,key=lambda x:(-x['score'],x['id']))[:8]

def validate():
    errors=[];duplicates=[]
    visual=json.loads((ROOT/'references/knowledge/visual/catalog.json').read_text(encoding='utf-8'))
    seen={};covered=set()
    for entry in visual['images']:
        p=ROOT/entry['path']; covered.add(p.resolve())
        for key in ('path','canonical_path','documentation'):
            if key not in entry or not (ROOT/entry[key]).is_file():errors.append(f"Missing {key}: {entry.get('id')}")
        if p.is_file():
            h=hashlib.sha256(p.read_bytes()).hexdigest()
            if h!=entry['sha256']:errors.append(f"Image hash mismatch: {entry['path']}")
            if h in seen:duplicates.append([seen[h],entry['path']])
            seen[h]=entry['path']
            canonical=ROOT/entry.get('canonical_path','MISSING')
            if canonical.is_file() and hashlib.sha256(canonical.read_bytes()).hexdigest()!=h:errors.append('Canonical image differs')
    for p in ROOT.glob('recursos do kommo/**/*'):
        if p.suffix.lower() in ('.png','.jpg','.jpeg','.webp') and p.resolve() not in covered:errors.append(f'Undocumented image: {p.name}')
    cat=json.loads((ROOT/'references/knowledge/catalog.json').read_text(encoding='utf-8')); ids=set()
    for item in cat['procedures']:
        if item['id'] in ids:errors.append('Duplicate identifier '+item['id'])
        ids.add(item['id'])
        if not (ROOT/item['path']).is_file():errors.append('Missing procedure '+item['path'])
    for p in ROOT.rglob('*.md'):
        # Templates contain project-relative examples; validate package references only.
        if 'templates' in p.parts:continue
        text=p.read_text(encoding='utf-8')
        for raw in re.findall(r'!?\[[^\]]*\]\(([^\n]+?)\)',text):
            raw=raw.strip('<>'); target=unquote(raw.split('#',1)[0])
            if not target or re.match(r'\w+://|mailto:|[A-Za-z]:|<',target):continue
            if not (p.parent/target).exists():errors.append(f'{p.relative_to(ROOT)}: missing {target}')
    return dict(valid=not errors,errors=errors,images=len(covered),canonical_images=len(seen),deduplicated_original_pairs=duplicates,procedures=len(ids))
