"""Restore original replay paths from the release archive and verify hashes."""
import argparse, hashlib, json, shutil, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def restore(archive, member, relative, digest=None):
    target = (ROOT / relative).resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError('Input path escapes repository')
    if target.exists():
        if digest and hashlib.sha256(target.read_bytes()).hexdigest() == digest:
            return
        if digest:
            raise ValueError(f'Refusing to replace mismatched file: {relative}')
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    with archive.open(member) as source, target.open('xb') as output:
        shutil.copyfileobj(source, output)
    if digest and hashlib.sha256(target.read_bytes()).hexdigest() != digest:
        raise ValueError(f'Hash mismatch: {relative}')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    args = parser.parse_args()
    asset = next(x for x in json.loads((ROOT / 'RELEASE_ASSETS.json').read_text()) if x['name'] == 'submission-all-traits.zip')
    digest = hashlib.sha256()
    with args.archive.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''): digest.update(chunk)
    if digest.hexdigest() != asset['sha256']:
        raise ValueError('Release archive SHA-256 mismatch')
    provenance = json.loads((ROOT / 'deadline-sparse/all_source_replays.json').read_text())
    unique = {}
    with zipfile.ZipFile(args.archive) as archive:
        for entry in provenance:
            suffix = Path(entry['file']).suffix
            restore(archive, 'replays/' + entry['sha256'] + suffix, entry['file'], entry['sha256'])
            unique[entry['sha256']] = entry['file']
        provisional = json.loads((ROOT / 'deadline-sparse/2019_provisional_provenance.json').read_text())
        restore(archive, 'provisional-2019/recording.mgz', 'tatoh/raw/archive_2019_feudalvoy/recording.mgz', provisional['replay_sha256'])
    print(json.dumps({'unique_verified_replay_files': len(unique), 'provisional_files': 1, 'archive_sha256_verified': True, 'source_hashes_verified': True}, indent=2))

if __name__ == '__main__': main()
