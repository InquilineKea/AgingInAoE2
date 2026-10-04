"""Expand command features to all available verified TaToH observations."""
import sys,json,csv,hashlib,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'deadline-sparse';sys.path.insert(0,str(ROOT/'scripts'))
import behavior_metrics as B
source=[r for r in B.csvread(ROOT/'tatoh/game_metrics.csv') if r['who']=='TaToH']
result=[r for r in B.csvread(OUT/'behavior_features.csv') if r['player']!='TaToH'];provenance=[]
for i,r in enumerate(source):
 path=next((ROOT/'tatoh/raw'/r['game']).glob('*.aoe2record'));meta,acts=B.D.decode(path)
 p=next(p for p in meta['players'] if p.get('profile_id')==197388 or (r['game'].startswith('hc4') and p['name']=='Le Loi'))
 aa=[a for a in acts if a['player']==p['number']]
 windows=[('whole available replay',meta['duration_s'])]
 if meta['duration_s']>=600:windows.insert(0,('first 10 game minutes',600))
 for window,end in windows:result.append(dict(game_id=r['game'],player='TaToH',year=r['period'][:4],context=r['period'][5:],cluster=r['cluster'],window=window,timing_comparable_to_de=True,partial_match=r['partial'],**B.calc(aa,meta['speed'],end,meta.get('dimension'))))
 provenance.append({'game_id':r['game'],'file':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'date':r['date'],'year':r['period'][:4],'context':r['period'][5:],'cluster':r['cluster'],'partial':r['partial']=='True','duration_game_seconds':meta['duration_s'],'nominal_speed':meta['speed'],'dimension':meta.get('dimension'),'slot':p['number'],'identity':p['name'],'identity_verified_by':'profile197388' if p.get('profile_id')==197388 else 'HC4 alias Le Loi','body_end':meta['body_end'],'file_bytes':path.stat().st_size})
 (OUT/'all-traits-progress.json').write_text(json.dumps({'state':'expanding_tatoh','games_processed':i+1,'games_planned':len(source),'current_game':r['game']},indent=2)+'\n')
 if (i+1)%5==0:print('TaToH',i+1,'/',len(source),flush=True)
B.csvwrite('behavior_features_all.csv',result)
(OUT/'all_tatoh_provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
(OUT/'all-traits-progress.json').write_text(json.dumps({'state':'features_complete','player_game_observations':len({(r['game_id'],r['player']) for r in result}),'windows':len(result),'tatoh_games':len(source),'short_openings_excluded':sum(p['duration_game_seconds']<600 for p in provenance)},indent=2)+'\n')
print('All features completed',len(result),'rows',flush=True)
