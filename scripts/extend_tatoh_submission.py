"""Add TaToH sparse strata and replay-derived APM to the deadline submission."""
import csv,json,gzip,hashlib,statistics,zipfile,runpy,sys,html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'deadline-sparse'
sys.path.insert(0,str(ROOT/'scripts'))
import decode as D
orig=D.de_prefix
D.de_prefix=lambda data,save:orig(data,68.9 if 68<=save<68.9 else save)
runpy.run_path(str(ROOT/'scripts/deadline_sparse.py'))
def rows(p):
 with p.open() as f:return list(csv.DictReader(f))
def save(name,rs):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
me=[r for r in rows(ROOT/'tatoh/game_metrics.csv') if r['who']=='TaToH'];sel=[]
for period in ['2021 tournament','2026 tournament','2026 ranked']:
 pool=[r for r in me if r['period']==period]
 if period=='2026 ranked':pool=[r for r in pool if r['game'] in ['ranked_510330665','ranked_508914728']]
 pool.sort(key=lambda r:(r['date'],r['game']));sel+=pool[:2]
save('tatoh_selected_games.csv',sel)
summary=[]
for period in sorted({r['period'] for r in sel}):
 rs=[r for r in sel if r['period']==period]
 summary.append({'player':'TaToH','period':period,'n_games':len(rs),'n_clusters':len({r['cluster'] for r in rs}),'partial_games':sum(r['partial']=='True' for r in rs),**{k:statistics.median(float(r[k]) for r in rs) for k in ['open_cpm','whole_cpm','reclick_open','dedup_open_cpm','gap_p50_open']}})
save('tatoh_period_summary.csv',summary)
manifest={r['game_id']:r for r in json.loads((ROOT/'results/manifest.json').read_text()) if r['status']=='parsed'}
apm=[];tatohprovenance=[]
def measure(gid,player,period,slot,speed,seconds,acts,partial=False):
 aa=[a for a in acts if a.get('player')==slot]
 for window,end in [('first 10 game minutes',600),('whole available replay',seconds)]:
  selected=[a for a in aa if 0<=a['t']<end] if end==600 else aa
  duration=end/speed/60
  apm.append({'game_id':gid,'player':player,'period':period,'window':window,'recorded_player_commands':len(selected),'nominal_minutes':duration,'replay_apm':len(selected)/duration,'partial_match':partial,'definition':'All decoded ACTION records explicitly attributed to player; no unrecorded clicks/keypresses.'})
for r in rows(OUT/'selected_games.csv'):
 m=manifest[r['game_id']]
 with gzip.open(ROOT/'results/decoded'/(m['sha256']+'.json.gz'),'rt') as f:d=json.load(f)
 measure(r['game_id'],r['player'],r['year']+' '+r['context'],int(r['player_slot']),float(m['speed']),float(m['duration_game_min'])*60,d['actions'])
for r in sel:
 path=next((ROOT/'tatoh/raw'/r['game']).glob('*.aoe2record'));meta,acts=D.decode(path)
 players=[p for p in meta['players'] if p.get('profile_id')==197388 or (r['game'].startswith('hc4') and p['name']=='Le Loi')]
 assert len(players)==1
 sha=hashlib.sha256(path.read_bytes()).hexdigest()
 measure(sha[:12],'TaToH',r['period'],players[0]['number'],meta['speed'],meta['duration_s'],acts,r['partial']=='True')
 tatohprovenance.append({'game':r['game'],'file':str(path.relative_to(ROOT)),'sha256':sha,'profile_id':players[0].get('profile_id'),'verified_player_name':players[0]['name'],'partial':r['partial']=='True','available_game_minutes':meta['duration_s']/60,'body_end':meta.get('body_end'),'file_bytes':path.stat().st_size})
save('replay_apm_games.csv',apm)
asummary=[]
for player,period,window in sorted({(r['player'],r['period'],r['window']) for r in apm}):
 rs=[r for r in apm if (r['player'],r['period'],r['window'])==(player,period,window)]
 asummary.append({'player':player,'period':period,'window':window,'n_games':len(rs),'median_replay_apm':statistics.median(r['replay_apm'] for r in rs)})
save('replay_apm_summary.csv',asummary)
(OUT/'tatoh_provenance.json').write_text(json.dumps(tatohprovenance,indent=2)+'\n')
text=['# TaToH extension and basic replay APM','','TaToH adds one partial 2021 tournament replay, two 2026 tournament games and two 2026 ranked games. Earliest available tournament games were selected by date/game name; ranked games use the existing TheViper-versus-TaToH capture and one additional compatible short replay. This is convenience sampling. The two recent ranked games are from separate days. There is no verified 2011/2012 TaToH baseline.','','| Period | Games | Partial games | Opening core CPM | Whole available core CPM |','|---|---:|---:|---:|---:|']
for r in summary:text.append(f"| {r['period']} | {r['n_games']} | {r['partial_games']} | {r['open_cpm']:.1f} | {r['whole_cpm']:.1f} |")
text+=['','The 2021 archive was truncated upstream. Its first 69.5 game minutes were recovered; opening coverage is present, but its available-replay rate is not a complete-match rate. That single historical game cannot establish a temporal trend. TaToH identity is checked through profile 197388 or the documented HC4 alias Le Loi.','','## Basic APM definition','','Replay-derived APM counts all decoded ACTION records explicitly attributed to the player, including production/queue commands, divided by nominal minutes (game clock / recorded game speed). It does not count mouse clicks, camera movement, hotkeys or selections that leave no attributed ACTION record. ACTION semantics and ownership coverage differ across engine versions. Do not present this as device-input APM or directly compare it to CaptureAge/eAPM without matching definitions. Core CPM excludes non-core action types; the two measures have different denominators of actions.','','| Player | Period | Games | Opening replay APM | Whole available replay APM |','|---|---|---:|---:|---:|']
for r in asummary:
 if r['window']!='first 10 game minutes':continue
 w=next(x for x in asummary if (x['player'],x['period'],x['window'])==(r['player'],r['period'],'whole available replay'))
 text.append(f"| {r['player']} | {r['period']} | {r['n_games']} | {r['median_replay_apm']:.1f} | {w['median_replay_apm']:.1f} |")
text+=['','These rates measure recorded actions. Reaction time, working-memory capacity and compensation remain unmeasured. No age-effect test is claimed.','','Completed engine captures: one DauT match and two TheViper matches. The 14.6-minute TheViper game also includes TaToH, so one complete TaToH state stream is already available. The additional 17.6-minute TaToH match is also fully captured. All four selected match captures passed end verification with zero reported skipped simulation steps. Current binary state remains undecoded. State command summaries are included; raw state streams remain in engine-pass and are not embedded in this small ZIP.']
report='\n'.join(text)+'\n';(OUT/'TATOH_AND_APM.md').write_text(report)
p=OUT/'report.html';p.write_text(p.read_text()+'<hr><pre>'+html.escape(report)+'</pre>')
for p in (ROOT/'engine-pass').glob('full-*/command-summary.json'):
 (OUT/('engine-summary-'+p.parent.name+'.json')).write_bytes(p.read_bytes())
with zipfile.ZipFile(OUT/'submission.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.iterdir()):
  if p.is_file() and p.name!='submission.zip':z.write(p,p.name)
 for r in json.loads((OUT/'provenance.json').read_text()):z.write(ROOT/r['file'],'replays/'+r['sha256']+Path(r['file']).suffix)
 for r in tatohprovenance:z.write(ROOT/r['file'],'tatoh-replays/'+r['sha256']+'.aoe2record')
 z.write(Path(__file__),'scripts/extend_tatoh_submission.py');z.write(ROOT/'scripts/deadline_sparse.py','scripts/deadline_sparse.py')
with zipfile.ZipFile(OUT/'submission.zip') as z:assert z.testzip() is None
print(report);print('ZIP bytes',(OUT/'submission.zip').stat().st_size)
