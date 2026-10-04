"""Fetch the TaToH replay sample. Public sources only; extract only replay files.

- 2019: one community-uploaded UserPatch recording on archive.org.
- 2021: Hidden Cup 4 Ro16 pack, Le Loi (TaToH) vs John the Fearless (Hera).
- 2026: every 1v1 still retained by Microsoft's replay endpoint (about 6-8 weeks):
  ranked RM 1v1 games and 2-player tournament-qualifier lobbies, from the
  aoe2companion match list saved in tatoh/.
Team games are not downloaded.
"""
import requests, zipfile, io, json, hashlib, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; T=ROOT/'tatoh'; RAW=T/'raw'; RAW.mkdir(parents=True,exist_ok=True)
PROFILE=197388
jobs=[dict(name='archive_2019_feudalvoy',kind='file',url='https://archive.org/download/rec.20190928-160552/rec.20190928-160552.mgz',ext='.mgz',period='2019 community upload'),
      dict(name='hc4_tatoh_vs_hera',kind='zip',url='https://ageofnotes.com/wp-content/uploads/2021/05/7.-HC4-Ro16-Le-Loi-vs-John-the-Fearless.zip',period='2021 HC4 Ro16')]
matches=json.loads((T/'aoe2companion_matches_2026-08-10_to_2026-10-04.json').read_text())
for lb,ms in matches.items():
    for m in ms:
        players=[p for t in m['teams'] for p in t['players']]
        if len(players)!=2: continue
        jobs.append(dict(name=f"{'ranked' if lb=='rm_1v1' else 'lobby'}_{m['matchId']}",kind='zip',
            url=f"https://aoe.ms/replay/?gameId={m['matchId']}&profileId={PROFILE}",
            period='2026 ranked' if lb=='rm_1v1' else '2026 lobby 1v1',match=m['matchId'],started=m['started'],
            lobby=m['name'],map=m.get('mapName'),players=[(p['name'],p['profileId'],p.get('won')) for p in players]))
log=[]
for j in jobs:
    row=dict(j);files=[]
    try:
        r=requests.get(j['url'],timeout=60,headers={'User-Agent':'Mozilla/5.0'})
        row['http']=r.status_code
        if r.status_code==200:
            b=r.content; row.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
            if j['kind']=='zip':
                assert b.startswith(b'PK') and len(b)<100_000_000
                with zipfile.ZipFile(io.BytesIO(b)) as z:
                    for info in z.infolist():
                        if Path(info.filename).suffix.lower() in ('.aoe2record','.mgz','.mgx') and info.file_size<60_000_000:
                            d=RAW/j['name'];d.mkdir(exist_ok=True);out=d/Path(info.filename).name
                            out.write_bytes(z.read(info));files.append(str(out.relative_to(ROOT)))
            else:
                d=RAW/j['name'];d.mkdir(exist_ok=True);out=d/('recording'+j['ext']);out.write_bytes(b);files.append(str(out.relative_to(ROOT)))
    except Exception as e:
        row['error']=repr(e)
    row['files']=files;log.append(row)
    print(j['name'],row.get('http'),row.get('bytes'),len(files),flush=True)
    time.sleep(0.7)
(T/'downloads.json').write_text(json.dumps(log,indent=1))
