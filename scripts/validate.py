"""Numerical integrity and independent parser cross-checks for the pilot."""
from pathlib import Path
import sys,json,gzip,collections,hashlib
import numpy as np,pandas as pd
from mgz.model import parse_match
ROOT=Path(__file__).resolve().parents[1];RESULTS=ROOT/'results'
manifest=json.loads((RESULTS/'manifest.json').read_text());df=pd.read_csv(RESULTS/'game_metrics.csv');checks=[]
for key in ['hc4_daut','hc4_viper']:
 row=next(x for x in manifest if '/'+key+'/' in x['file'])
 with (ROOT/row['file']).open('rb') as f:m=parse_match(f)
 with gzip.open(RESULTS/'decoded'/(row['sha256']+'.json.gz'),'rt') as f:decoded=json.load(f)
 raw=decoded['actions'];expected=[(a.timestamp.total_seconds(),a.type.name,a.player.number if a.player else None) for a in m.actions];actual=[(a['t'],a['type'],a['player']) for a in raw]
 assert len(expected)==len(actual) and expected==actual
 assert abs(m.duration.total_seconds()-decoded['meta']['duration_s'])<0.001
 checks.append(dict(check='independent mgz.model vs local body decoder',file=row['file'],action_count=len(raw),exact_timestamp_type_owner_agreement=True))
for row in manifest:
 if row['year']==2021:
  from mgz.fast.header import parse
  with (ROOT/row['file']).open('rb') as f:full=parse(f)
  assert full['map']['restore_time']==0
 assert row['file_bytes']==(ROOT/row['file']).stat().st_size
 assert hashlib.sha256((ROOT/row['file']).read_bytes()).hexdigest()==row['sha256']
 assert row['body_end']==row['file_bytes']
 assert row['restore_time']==0
for _,r in df.iterrows():
 assert abs(r.core_cpm_nominal-r.n_commands/r.nominal_duration_min)<1e-8
 assert abs(r.core_cpm_game-r.n_commands/r.duration_game_min)<1e-8
 assert 0<=r.switches_per_100_commands<=100
 assert 0<=r.core_silence_over5s_fraction<=1.00001
 assert 0<=r.spatial_entropy_4x4_bits<=4.00001
assert len(df[df.year==2026])==10
assert not df.duplicated(['game_id','player']).any()
assert df.game_id.nunique()==37
assert not df.game_id.eq('abfca9f523fb').any()
assert not df[(df.player=='TheViper')&(df.year<2012)].shape[0]
checks.extend([dict(check='hashes/full body consumed/non-restored',files=len(manifest)),dict(check='2026 independent sync clock checkpoints',n=sum(r['sync_checks'] for r in manifest if r['year']==2026)),dict(check='per-game rate/time/entropy/fraction invariants',observations=len(df))])
(RESULTS/'validation.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
