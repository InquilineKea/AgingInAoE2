"""Fetch the same public 2021/2026 sample if still available. No account access.

Microsoft removes older replays. Preserve local files and record HTTP failures.
Use download_historical.py for the four 2011/2012 public upload packs.
"""
import requests,zipfile,io,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
urls={
 'hc4_daut_ro8':'https://ageofnotes.com/wp-content/uploads/2021/05/10.-HC4-Ro8---Sundjata-vs-Gonzalo-Pizarro.zip',
 'hc4_viper_ro8':'https://ageofnotes.com/wp-content/uploads/2021/05/11.-HC4-Ro8---Ivaylo-vs-Edward-Longshanks.zip',
 'hc4_daut':'https://ageofnotes.com/wp-content/uploads/2021/05/4.-HC4-Ro16-Pope-Leo-vs-Gonzalo.zip',
 'hc4_viper':'https://ageofnotes.com/wp-content/uploads/2021/05/5.-HC4-Ro16-King-Bela-IV-vs-Ivaylo.zip'
}
for player,profile,ids in [('daut',198035,[508977160,508980233,508982914,508986499,508989109]),('viper',196240,[510309668,510319711,510323612,510327598,510330665])]:
 for game in ids:urls[f'{player}_{game}']=f'https://aoe.ms/replay/?gameId={game}&profileId={profile}'
results=[]
for name,url in urls.items():
 path=ROOT/'raw'/(name+'.zip')
 if path.exists():payload=path.read_bytes();status='preserved existing'
 else:
  response=requests.get(url,timeout=45);response.raise_for_status();payload=response.content
  assert payload.startswith(b'PK') and len(payload)<20_000_000
  path.write_bytes(payload);status='downloaded'
 dest=ROOT/'raw'/name;dest.mkdir(exist_ok=True)
 with zipfile.ZipFile(io.BytesIO(payload)) as archive:
  for info in archive.infolist():
   if Path(info.filename).suffix.lower()=='.aoe2record' and info.file_size<50_000_000:
    output=dest/Path(info.filename).name
    if not output.exists():output.write_bytes(archive.read(info))
 results.append(dict(name=name,source_url=url,status=status,bytes=len(payload),sha256=hashlib.sha256(payload).hexdigest()))
 print(name,status)
(ROOT/'sources'/'sample-downloads.json').write_text(json.dumps(results,indent=2))
