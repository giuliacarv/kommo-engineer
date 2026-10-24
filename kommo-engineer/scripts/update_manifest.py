"""Rebuild package inventory, excluding this manifest and Python caches."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=ROOT/'manifest.json';obj=json.loads(p.read_text(encoding='utf-8'))
    obj.update(version='0.5.0-rc.1',notes='Release candidate: testes offline, API experimental sem homologação de conta, escrita desligada por padrão.')
    obj['files']={f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(ROOT.rglob('*')) if f.is_file() and f.name!='manifest.json' and '__pycache__' not in f.parts and f.suffix!='.pyc'}
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(dict(version=obj['version'],files=len(obj['files']))))
if __name__=='__main__':main()
