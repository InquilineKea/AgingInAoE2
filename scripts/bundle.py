"""Package public recordings and final analysis, excluding environment and fixtures."""
from pathlib import Path
import zipfile,json,hashlib,csv,collections
root=Path(__file__).resolve().parents[1];dest=root.parent/'aoe2-aging-samples-and-analysis.zip'
files=[root/p for p in ['REPORT.md','README.md','report.html','requirements.txt']]
files+=list((root/'raw').rglob('*'))
files+=[p for p in (root/'results').glob('*') if p.is_file() and p.name!='bundle-verification.json']
files+=list((root/'scripts').glob('*.py'))+list((root/'sources').glob('*.json'))
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
 for p in files:
  if p.is_file():archive.write(p,Path('aoe2-aging')/p.relative_to(root))
with zipfile.ZipFile(dest) as archive:
 assert archive.testzip() is None
 recordings=[p for p in archive.namelist() if p.endswith(('.mgx','.aoe2record','.mgz'))]
 assert len(recordings)==46
rows=list(csv.DictReader(open(root/'results/game_metrics.csv')))
assert len(rows)==44 and len({r['game_id'] for r in rows})==37
assert not any(n>1 for n in collections.Counter((r['game_id'],r['player']) for r in rows).values())
summary=dict(bundle=str(dest),bytes=dest.stat().st_size,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),downloaded_replay_files=46,duplicate_files_excluded=5,validation_failures_excluded=3,unrelated_game_excluded=1,analyzed_target_games=37,player_game_observations=44,zip_integrity='passed')
(root/'results/bundle-verification.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
