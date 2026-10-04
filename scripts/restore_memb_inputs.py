"""Restore only manifest-listed Memb replay inputs, with no silent overwrites."""
import argparse,hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('archive',type=Path);args=parser.parse_args()
    asset=next(r for r in json.loads((ROOT/'RELEASE_ASSETS.json').read_text()) if r['name']=='memb-analysis.zip')
    digest=hashlib.sha256()
    with args.archive.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):digest.update(chunk)
    assert digest.hexdigest()==asset['sha256'],'Archive hash mismatch'
    rows=[r for r in json.loads((ROOT/'memb/downloads.json').read_text()) if 'file' in r]
    with zipfile.ZipFile(args.archive) as z:
        for r in rows:
            target=(ROOT/r['file']).resolve()
            assert target.is_relative_to(ROOT/'memb/raw'),'Manifest path escapes replay directory'
            data=z.read(r['file']);assert hashlib.sha256(data).hexdigest()==r['sha256']
            target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists():assert hashlib.sha256(target.read_bytes()).hexdigest()==r['sha256'],'Refusing to replace mismatched input'
            else:
                with target.open('xb') as f:f.write(data)
    print(json.dumps({'replays':len(rows),'archive_and_source_hashes_verified':True},indent=2))

if __name__=='__main__':main()
