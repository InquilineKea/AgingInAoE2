"""Build a reproducible, descriptive sparse-period submission from verified tables."""
import csv, json, hashlib, statistics, html, zipfile
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'deadline-sparse'; OUT.mkdir(exist_ok=True)
def read(p):
 with p.open() as f: return list(csv.DictReader(f))
def write(name, rows):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
features=read(ROOT/'reanalysis-v2/game_features.csv'); metrics=read(ROOT/'results/game_metrics.csv')
manifest=json.loads((ROOT/'results/manifest.json').read_text()); sources={r['game_id']:r for r in manifest if r['status']=='parsed'}
selected=[]
for player in ('DauT','TheViper'):
 for year in sorted({r['year'] for r in metrics if r['player']==player}):
  pool=[r for r in metrics if r['player']==player and r['year']==year]
  if year=='2026' and player=='TheViper': pool.sort(key=lambda r:(float(r['duration_game_min']),r['game_id']))
  else: pool.sort(key=lambda r:(r['date'],r['game_id']))
  selected.extend(pool[:2])
keys={(r['game_id'],r['player']) for r in selected}
chosen=[r for r in features if (r['game_id'],r['player']) in keys]
write('selected_games.csv',selected); write('game_features.csv',chosen)
cols=['core_cpm_nominal','destination_jump_ge_quarter_diagonal_fraction','build_commands_nominal_min','wall_commands_nominal_min','research_commands_nominal_min','explicit_actor_coverage']
def med(rows,col):
 vals=[float(r[col]) for r in rows if r.get(col)!='' and r.get(col) is not None]
 return statistics.median(vals) if vals else None
summary=[]
for player,year in sorted({(r['player'],r['year']) for r in chosen}):
 for window in ('first 10 game minutes','whole game'):
  rs=[r for r in chosen if (r['player'],r['year'],r['window'])==(player,year,window)]
  summary.append(dict(player=player,year=year,window=window,n_games=len(rs),n_clusters=len({r['cluster'] for r in rs}),contexts='; '.join(sorted({r['context'] for r in rs})),**{c:med(rs,c) for c in cols}))
write('period_summary.csv',summary)
checks=[]
for gid in sorted({r['game_id'] for r in selected}):
 s=sources[gid]; raw=ROOT/s['file']; digest=hashlib.sha256(raw.read_bytes()).hexdigest()
 if digest!=s['sha256']: raise ValueError('Source hash mismatch '+gid)
 checks.append({'game_id':gid,'file':s['file'],'sha256':digest,'source_url':s.get('source_url'),'year':s['year'],'date':s['date'],'date_precision':s.get('date_precision'),'players_in_replay':s['player_names'],'hash_verified':True})
(OUT/'provenance.json').write_text(json.dumps(checks,indent=2)+'\n')
validation={'created_utc':datetime.now(timezone.utc).isoformat(),'player_game_observations':len(selected),'distinct_replays':len(checks),'period_rows':len(summary),'source_hashes_verified':True,'two_games_per_player_period':all(r['n_games']==2 for r in summary),'engine_state_schema_decoded':False,'onager_dodges_classified':0,'full_dataset_sensitivity':'../reanalysis-v2/period_summary.csv','selection_rule':'Earliest dated two games per player/year with game_id tie-break; 2026 TheViper uses the two shortest available games for deadline-compatible state validation. Selection uses no command-feature outcome. Convenience sampling and duration selection introduce bias.'}
(OUT/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
lines=['# Sparse replay pilot: DauT and TheViper across career periods','','A reproducible hackathon pilot measuring command behavior in younger and later career recordings. This is a descriptive feasibility study; it does not measure cognitive aging.','','## Sampling and provenance','',validation['selection_rule'],'','Two games per available player/year: DauT 2011, 2012, 2021, 2026; TheViper 2012, 2021, 2026. All selected raw replay SHA-256 hashes were checked. Every sampled game has whole-game commands and a standardized first-ten-game-minute window. Historical dates can be upload/filename dates; see provenance.json.','',f'{len(selected)} player-game observations from {len(checks)} distinct replay files. Shared team games can contribute observations to both players and are not independent.','','## Measured results','','Opening and whole-game command rates are per nominal real minute: game-clock duration divided by replay-recorded nominal speed. They are not directly measured human input rates.','','| Player | Year | Games / clusters | Opening commands/min | Whole-game commands/min | Opening large destination jumps |','|---|---:|---:|---:|---:|---:|']
for r in summary:
 if r['window']!='first 10 game minutes': continue
 w=next(x for x in summary if (x['player'],x['year'],x['window'])==(r['player'],r['year'],'whole game'))
 lines.append(f"| {r['player']} | {r['year']} | {r['n_games']} / {r['n_clusters']} | {r['core_cpm_nominal']:.1f} | {w['core_cpm_nominal']:.1f} | {100*r['destination_jump_ge_quarter_diagonal_fraction']:.1f}% |")
lines+=['','A large destination jump is a distance of at least one-quarter map diagonal between consecutive valid move/order destinations. It measures spatial command dispersion; it does not measure gaze, attention switching or memory.','']
for player in ('DauT','TheViper'):
 a=next(r for r in summary if (r['player'],r['year'],r['window'])==(player,'2021','first 10 game minutes'))
 b=next(r for r in summary if (r['player'],r['year'],r['window'])==(player,'2026','first 10 game minutes'))
 pct=100*(b['core_cpm_nominal']/a['core_cpm_nominal']-1)
 lines.append(f"{player}: the sparse opening median changes from {a['core_cpm_nominal']:.1f} in 2021 to {b['core_cpm_nominal']:.1f} in 2026 ({pct:+.1f}%). This is a sample difference, not an identified age effect.")
lines+=['','Full-data sensitivity check: the previously validated 2021/2026 opening medians are DauT 95.82 → 84.84 and TheViper 122.19 → 102.75. Whole-game medians rise in that larger sample (DauT 74.72 → 86.12; TheViper 94.73 → 103.32). A general slowing claim is therefore unsupported. See full_period_summary.csv.','','## What the features can establish','','- Command frequency and destination dispersion: observed replay command behavior.','- Build/wall/research rates: issued commands, not completed actions or strategic success.','- Reaction time: unavailable without a visible threat onset and a linked response. Command gaps are not reaction time.','- Working memory: not measured. No validated memory task or capacity estimate is present.','- Compensation: hypothesis only. More planning or repeated commands cannot by itself establish compensation.','- Onager dodging: zero classified episodes; projectile/state decoding and threat visibility remain unvalidated.','','## State capture status','','Recent game-state streams are optional technical validation, separate from the longitudinal command comparison. The running sparse queue targets one complete DauT game and the two shortest recent TheViper games. A second DauT capture preserves more than ten game minutes but is an incomplete match. Historical 2021 state simulation needs an older DE engine; 2011/2012 needs a compatible classic engine. These historical state frames have not been collected. The current API22 binary state schema is not decoded. See state_capture_status.json for the build-time snapshot and ../engine-pass/status.json for live progress.','','## Limits and next experiment','','Classic and DE files have different command encoding and timestamp granularity; cross-engine rates are exploratory. The 2012 recordings include team games; player-slot ownership and research coverage vary by version. 2021 is tournament play and 2026 is a small ranked session. Maps, opponents, civilizations, patches and game lengths differ. Two games per stratum provide no reliable population uncertainty or age attribution; no significance tests are presented. Explicit actor selection covers only part of raw commands, so group switching is excluded from longitudinal conclusions.','','The next falsifiable experiment would sample matched maps, civilizations, opponents and game phases, identify visible projectile threats, measure threat-to-command latency in game-clock time with timestamp-resolution checks, and score dodge outcomes. Repeated sessions and independent tournaments are required before an age interpretation.','','## Reproduce','','Run `python artifacts/aoe2-aging/scripts/deadline_sparse.py` from the repository root. Inputs are the existing verified replay-command tables and original raw files. The ZIP includes sampled replays, provenance, selected rows, period summaries, full-data sensitivity, validation and the script. No credentials or player chat are included.']
(OUT/'REPORT.md').write_text('\n'.join(lines)+'\n')
(OUT/'full_period_summary.csv').write_bytes((ROOT/'reanalysis-v2/period_summary.csv').read_bytes())
state=json.loads((ROOT/'engine-pass/status.json').read_text())
state['historical_games_pending']=sum(r['year']!=2026 for r in json.loads((ROOT/'engine-pass/queue.json').read_text()))
state['recent_games_deferred']=7
state['capture_folders']=[{'folder':p.parent.name,**json.loads(p.read_text())} for p in (ROOT/'engine-pass').glob('full-*/status.json')]
(OUT/'state_capture_status.json').write_text(json.dumps(state,indent=2)+'\n')
rows=[r for r in summary if r['window']=='first 10 game minutes']
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="490" viewBox="0 0 900 490"><rect width="900" height="490" fill="#101827"/><text x="35" y="40" fill="white" font-size="24">Sparse pilot: opening command rates</text><text x="35" y="65" fill="#aebbd0" font-size="15">Two games per player / period • nominal commands per minute • descriptive only</text>']
for i,r in enumerate(rows):
 y=100+i*47; val=r['core_cpm_nominal']; color='#5ac8b8' if r['player']=='DauT' else '#b59afa'
 svg.append(f'<text x="35" y="{y+20}" fill="white" font-size="16">{r["player"]} {r["year"]}</text><rect x="190" y="{y}" width="{val*4:.1f}" height="28" rx="4" fill="{color}"/><text x="{200+val*4:.1f}" y="{y+20}" fill="white" font-size="16">{val:.1f}</text>')
svg.append('<text x="35" y="465" fill="#aebbd0" font-size="14">Era, engine, map and tournament/ranked context differ. These are not reaction-time measurements.</text></svg>')
(OUT/'opening_rates.svg').write_text(''.join(svg))
(OUT/'report.html').write_text('<!doctype html><meta charset="utf-8"><title>Sparse replay pilot</title><style>body{max-width:1000px;margin:40px auto;padding:20px;font:17px system-ui;background:#101827;color:#edf2fa}pre{white-space:pre-wrap;line-height:1.55}img{width:100%}</style><h1>DauT and TheViper: sparse longitudinal replay pilot</h1><img src="opening_rates.svg" alt="Opening command rates"><pre>'+html.escape('\n'.join(lines))+'</pre>')
zip_path=OUT/'submission.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.iterdir()):
  if p.is_file() and p!=zip_path: z.write(p,p.name)
 z.write(Path(__file__),'scripts/deadline_sparse.py')
 for r in checks: z.write(ROOT/r['file'],'replays/'+r['sha256']+Path(r['file']).suffix)
print(json.dumps(validation,indent=2)); print('bundle_bytes',zip_path.stat().st_size)
