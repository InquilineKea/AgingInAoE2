"""Use the existing detail-feature definitions for every usable TaToH replay."""
import sys,json,gzip,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'deadline-sparse';sys.path.insert(0,str(ROOT/'scripts'))
import replay_detail_features as R
from mgz import fast
from mgz.fast.header import decompress,parse_version
rows=[];checks=[]
for i,m in enumerate(json.loads((OUT/'all_tatoh_provenance.json').read_text())):
 path=ROOT/m['file'];acts=[];ts=0
 with path.open('rb') as f:
  head=decompress(f);parse_version(head,f);fast.meta(f)
  while f.tell()<path.stat().st_size:
   op,p=fast.operation(f)
   if op is fast.Operation.SYNC:ts+=p[0]
   elif op is fast.Operation.ACTION:
    typ,payload=p;acts.append(dict(t=ts/1000,type=typ.name,player=payload.get('player_id'),**{k:payload[k] for k in R.FIELDS if k in payload}))
  assert f.tell()==m['body_end']==path.stat().st_size
 assert ts/1000==m['duration_game_seconds']
 meta={'speed':m['nominal_speed'],'dimension':m['dimension'],'save_version':20.06 if m['year']=='2021' else 68.9}
 windows=[('whole available replay',m['duration_game_seconds'])]
 if m['duration_game_seconds']>=600:windows.insert(0,('first 10 game minutes',600))
 for window,end in windows:rows.append(dict(game_id=m['game_id'],player='TaToH',year=m['year'],context=m['context'],cluster=m['cluster'],window=window,**R.features(acts,meta,m['slot'],end)))
 checks.append({'game_id':m['game_id'],'body_end_verified':True,'clock_verified':True,'partial_match':m['partial']})
 (OUT/'all-traits-detail-progress.json').write_text(json.dumps({'processed':i+1,'planned':54,'state':'running'},indent=2)+'\n')
 if (i+1)%10==0:print('Detailed TaToH',i+1,'/54',flush=True)
with (OUT/'tatoh_detail_features_all.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(OUT/'tatoh_detail_validation.json').write_text(json.dumps(checks,indent=2)+'\n')
(OUT/'all-traits-detail-progress.json').write_text(json.dumps({'processed':54,'planned':54,'state':'complete'},indent=2)+'\n')
print('Detailed features complete',len(rows),flush=True)
