"""Bounded, public-source MembTV replay cohort; no credentials or chat export.

Freeze six newest all-mode match pages and the newest ranked page. Download
the newest 60 all-mode games plus three latest ranked availability probes.
The outcome-independent newest-first rule is fixed before command analysis.
"""
from pathlib import Path
import hashlib, io, json, subprocess, time, zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'memb'
SOURCES = OUT / 'sources'
RAW = OUT / 'raw'
PROFILE = 196407

def fetch(url, dest):
    result = subprocess.run(['/usr/bin/curl', '--silent', '--show-error', '--location',
        '--proto', '=https', '--max-time', '45', '--output', str(dest),
        '--write-out', '%{http_code}', url], capture_output=True, text=True)
    return result.stdout.strip(), result.returncode

def main():
    SOURCES.mkdir(parents=True, exist_ok=True); RAW.mkdir(exist_ok=True)
    matches = []
    for page in range(1, 7):
        path = SOURCES / f'matches-page-{page}.json'
        if not path.exists():
            status, code = fetch(f'https://data.aoe2companion.com/api/matches?profile_ids={PROFILE}&page={page}', path)
            assert status == '200' and code == 0, (status, code)
        matches += json.loads(path.read_text())['matches']
        time.sleep(.25)
    assert len({m['matchId'] for m in matches}) == len(matches)
    (OUT / 'match-log.json').write_text(json.dumps(matches, indent=2)+'\n')
    ranked = json.loads((SOURCES / 'ranked-page-1.json').read_text())['matches']
    jobs = [(m, 'recent all-mode newest 60') for m in matches[:60]]
    jobs += [(m, 'latest ranked availability probe') for m in ranked[:3] if m['matchId'] not in {m['matchId'] for m in matches[:60]}]
    rows=[]
    for match, selection in jobs:
        mid=match['matchId']; url=f'https://aoe.ms/replay/?gameId={mid}&profileId={PROFILE}'
        file=RAW/f'{mid}.aoe2record'
        row={'match_id':mid,'url':url,'selection':selection,'started':match['started'],
             'finished':match.get('finished'),'leaderboard':match['leaderboard'],
             'players':sum(len(t['players']) for t in match['teams'])}
        archive=SOURCES/'temporary-replay.zip'
        if file.exists(): row['http']='200';row['cached']=True
        else:
            status,code=fetch(url,archive);row['http']=status;row['curl_exit']=code
            if status=='200' and code==0:
                data=archive.read_bytes();assert len(data)<100_000_000
                row['archive_sha256']=hashlib.sha256(data).hexdigest()
                with zipfile.ZipFile(io.BytesIO(data)) as z:
                    infos=[i for i in z.infolist() if i.filename.lower().endswith('.aoe2record')]
                    assert len(infos)==1 and infos[0].file_size<60_000_000
                    file.write_bytes(z.read(infos[0]))
            if archive.exists():archive.unlink()
        if file.exists():
            row.update(file=str(file.relative_to(ROOT)),sha256=hashlib.sha256(file.read_bytes()).hexdigest(),bytes=file.stat().st_size)
        rows.append(row)
        (OUT/'downloads.json').write_text(json.dumps(rows,indent=2)+'\n')
        print(mid,row['http'],row.get('bytes'),flush=True)
        time.sleep(.25)

if __name__=='__main__':main()
