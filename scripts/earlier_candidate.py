"""Quarantined 2019 community-attributed FeudalVoy recording; not a verified baseline."""
import sys,json,csv,hashlib,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import behavior_metrics as B
p=ROOT/'tatoh/raw/archive_2019_feudalvoy/recording.mgz';meta,acts=B.D.decode(p)
player=next(p for p in meta['players'] if p['name']=='feudalVoy');aa=[a for a in acts if a['player']==player['number']]
rows=[]
for window,end in [('first 10 game minutes',600),('whole available replay',meta['duration_s'])]:
 rows.append(dict(recording='rec.20190928-160552',claimed_player='TaToH',verified_header_alias='feudalVoy',identity_status='Community-attributed; account identity unverified',window=window,**B.calc(aa,meta['speed'],end,meta['dimension'])))
with (ROOT/'deadline-sparse/2019_provisional_features.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
coverage={'url':'https://archive.org/details/rec.20190928-160552','replay_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'file_bytes':p.stat().st_size,'body_end':meta['body_end'],'full_body_consumed':meta['body_end']==p.stat().st_size,'duration_game_minutes':meta['duration_s']/60,'header_players':[p['name'] for p in meta['players']],'archive_title':'Tatoh píerde feudalVoy','archive_description':'Tatoh pierde con feudalVoy','date_precision':'2019-09-28 filename; uploaded 2019-10-29','identity_status':'Uploader attribution plus matching alias; not independent account verification','special_challenge':'Feudal-only series attribution; not comparable to unrestricted ranked/tournament play','unattributed_action_fraction':sum(a['player'] is None for a in acts)/len(acts),'unattributed_types':dict(collections.Counter(a['type'] for a in acts if a['player'] is None)),'included_in_main_comparison':False,'timing_comparable_to_DE':False}
(ROOT/'deadline-sparse/2019_provisional_provenance.json').write_text(json.dumps(coverage,indent=2)+'\n')
print(json.dumps(coverage,indent=2));print('provisional_opening_recorded_cpm',rows[0]['all_recorded_cpm'])
