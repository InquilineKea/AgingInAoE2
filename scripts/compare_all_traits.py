"""Compare every measured trait with explicit coverage and comparability flags."""
import csv,json,gzip,math,statistics as st,collections,re,html,zipfile,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'deadline-sparse'
def read(p):
 with p.open() as f:return list(csv.DictReader(f))
def write(name,rows):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def num(x):
 try:v=float(x);return v if math.isfinite(v) else None
 except (TypeError,ValueError):return None
base=read(OUT/'behavior_features_all.csv');traits=list(base[0])[8:]
for r in base:
 for t in traits:r[t]=num(r[t])
bykey={(r['game_id'],r['player'],r['window']):r for r in base}
# Existing raw-command detail features; keep nonduplicate measures and coverage.
v2=read(ROOT/'reanalysis-v2/game_features.csv');exclude={'core_cpm_nominal','destination_coordinate_coverage','destination_jump_diagonal_median','destination_jump_ge_quarter_diagonal_fraction'}
extras=[k for k in v2[0] if k not in {'game_id','player','year','context','cluster','player_slot','window','window_game_seconds'}|exclude]
for r in v2:
 key=(r['game_id'],r['player'],'whole available replay' if r['window']=='whole game' else r['window']);dst=bykey[key]
 for t in extras:dst[t]=num(r[t])
traits+=extras
for r in read(OUT/'tatoh_detail_features_all.csv'):
 dst=bykey[(r['game_id'],r['player'],r['window'])]
 for t in extras:dst[t]=num(r[t])
# Legacy whole-replay traits: distinct definitions are explicitly prefixed.
legacy=read(ROOT/'results/game_metrics.csv');lf=['command_class_entropy_bits','switches_per_100_commands','core_silence_over5s_fraction','peak_10s_nominal_cpm','move_share','planning_command_share','queue_batch_mean','queue_batch_gt1_fraction','duration_game_min']
for r in legacy:
 dst=bykey[(r['game_id'],r['player'],'whole available replay')]
 for t in lf:dst['legacy_'+t]=num(r[t])
traits+=['legacy_'+t for t in lf]
# Exact legacy equivalents for TaToH where the stored definitions suffice.
tatoh_prov={r['game_id']:r for r in json.loads((OUT/'all_tatoh_provenance.json').read_text())}
for r in base:
 if r['player']=='TaToH' and r['window']=='whole available replay':
  r['legacy_command_class_entropy_bits']=r['core_category_entropy_bits']
  r['legacy_switches_per_100_commands']=100*r['core_category_switch_fraction']
  rates=[r.get(t) for t in ['build_commands_nominal_min','wall_commands_nominal_min','research_commands_nominal_min','market_commands_nominal_min']]
  r['legacy_planning_command_share']=sum(rates)/r['core_cpm'] if all(x is not None for x in rates) and r['core_cpm'] else None
  r['legacy_queue_batch_mean']=r.get('positive_queue_amount_mean')
  r['legacy_duration_game_min']=tatoh_prov[r['game_id']]['duration_game_seconds']/60
# TaToH's previously computed phase-specific and repetition definitions.
tatoh=[r for r in read(ROOT/'tatoh/game_metrics.csv') if r['who']=='TaToH'];tf=['cpm_0_5','cpm_5_10','cpm_10_15','cpm_15_20','cpm_10_20','reclick_open','dedup_open_cpm','reclick_whole','dedup_whole_cpm','gap_p50_open','gap_p90_open','gap_p99_open','gap_p99_10_20']
for r in tatoh:
 dst=bykey[(r['game'],'TaToH','whole available replay')]
 for t in tf:dst['tatoh_'+t]=num(r[t])
traits+=['tatoh_'+t for t in tf]
# Age-up requests from explicitly attributed RESEARCH commands, game clock.
ages={'feudal_request_game_s':101,'castle_request_game_s':102,'imperial_request_game_s':103}
main_manifest={r['game_id']:r for r in json.loads((ROOT/'results/manifest.json').read_text()) if r['status']=='parsed'}
for r in legacy:
 m=main_manifest[r['game_id']]
 with gzip.open(ROOT/'results/decoded'/(m['sha256']+'.json.gz'),'rt') as f:actions=json.load(f)['actions']
 for window in ['first 10 game minutes','whole available replay']:
  dst=bykey[(r['game_id'],r['player'],window)]
  for t,tech in ages.items():dst[t]=next((a['t'] for a in actions if a['player']==int(r['player_slot']) and a['type']=='RESEARCH' and a.get('technology_id')==tech and (window!='first 10 game minutes' or a['t']<600)),None)
for r in tatoh:
 for window in ['first 10 game minutes','whole available replay']:
  dst=bykey.get((r['game'],'TaToH',window))
  if dst is not None:
   for t,original in [('feudal_request_game_s','feudal_s'),('castle_request_game_s','castle_s'),('imperial_request_game_s','imperial_s')]:
    value=num(r[original]);dst[t]=value if window!='first 10 game minutes' or value is not None and value<600 else None
traits+=list(ages)
comparisons=[('DauT earliest period','DauT',2011,'1v1 challenge',2026,'1v1 ranked','classic versus DE; challenge versus ranked; age cannot be isolated'),('TheViper earliest period','TheViper',2012,'team game',2026,'1v1 ranked','classic versus DE; team versus ranked; age cannot be isolated'),('DauT DE control','DauT',2021,'1v1 tournament',2026,'1v1 ranked','same engine family; patch/map/opponent/tournament versus ranked confounds'),('TheViper DE control','TheViper',2021,'1v1 tournament',2026,'1v1 ranked','same engine family; patch/map/opponent/tournament versus ranked confounds'),('TaToH tournament control','TaToH',2021,'tournament',2026,'tournament','one partial historical game; settings/maps/opponents differ'),('TaToH earliest verified to ranked','TaToH',2021,'tournament',2026,'ranked','one partial historical game; tournament versus ranked and map/opponent confounds')]
# The 2019 community attribution is never pooled into the verified baseline.
provisional=read(OUT/'2019_provisional_features.csv')
for r in provisional:
 base.append({'game_id':'rec.20190928-160552','player':'TaToH','year':'2019','context':'provisional Feudal-only','cluster':'2019 uploader', 'window':r['window'], 'partial_match':False,**{t:num(r.get(t)) for t in traits}})
comparisons.append(('TaToH provisional 2019','TaToH',2019,'provisional Feudal-only',2026,'ranked','unverified account identity; special challenge; classic command attribution gap; excluded from verified inference'))
def subset(player,year,context,window):return [r for r in base if r['player']==player and int(r['year'])==year and r['context']==context and r['window']==window]
def stats(rs,t):
 valid=[r for r in rs if num(r.get(t)) is not None]
 if not valid:return None
 cl=collections.Counter(r['cluster'] for r in valid);pairs=sorted((num(r[t]),1/cl[r['cluster']]) for r in valid);total=sum(w for v,w in pairs);cum=0
 for i,(value,weight) in enumerate(pairs):
  cum+=weight
  if cum>=total/2-1e-12:
   if math.isclose(cum,total/2,abs_tol=1e-12) and i+1<len(pairs):value=(value+pairs[i+1][0])/2
   break
 vals=[v for v,w in pairs]
 return {'weighted_median':value,'game_median':st.median(vals),'min':min(vals),'max':max(vals),'n':len(valid),'clusters':len(cl)}
def restriction(t,ey):
 if ('actor' in t or t in ['explicit_actor_coverage','actor_pair_count','same_actor_pair_count']):return 'Raw actor-list coverage/reuse differs: numeric contrast is not a reliable group-control trend.'
 if ey<2020 and any(x in t for x in ['gap','burst','silence','peak','first_core','count_5s','empty_5s']):return 'Cross-engine timing resolution/encoding differs; do not infer latency or slowing.'
 if ey<2020 and any(x in t for x in ['all_recorded','noncore','queue','research']):return 'Classic commands can lack ownership or differ in encoding; rates may undercount actions.'
 if 'request_game_s' in t or t.startswith('tatoh_') and t.endswith('_s'):return 'Age-up request timing depends strongly on start-age and tournament settings.'
 return 'Descriptive behavior; no cognitive or causal age interpretation.'
rows=[]
for label,player,ey,ec,ly,lc,limits in comparisons:
 for window in ['first 10 game minutes','whole available replay']:
  early=subset(player,ey,ec,window);late=subset(player,ly,lc,window)
  for t in traits:
   a,b=stats(early,t),stats(late,t)
   d=b['weighted_median']-a['weighted_median'] if a and b else None
   rows.append({'comparison':label,'player':player,'early_year':ey,'early_context':ec,'late_year':ly,'late_context':lc,'window':window,'trait':t,'early_n':a['n'] if a else 0,'late_n':b['n'] if b else 0,'early_clusters':a['clusters'] if a else 0,'late_clusters':b['clusters'] if b else 0,'early_weighted_median':a['weighted_median'] if a else None,'late_weighted_median':b['weighted_median'] if b else None,'early_game_median':a['game_median'] if a else None,'late_game_median':b['game_median'] if b else None,'early_min':a['min'] if a else None,'early_max':a['max'] if a else None,'late_min':b['min'] if b else None,'late_max':b['max'] if b else None,'difference':d,'difference_percentage_points':d*100 if d is not None and any(x in t for x in ['fraction','coverage','share']) else None,'relative_change_percent':d/a['weighted_median']*100 if a and b and a['weighted_median']!=0 else None,'direction':'unavailable' if d is None else 'increase' if d>1e-10 else 'decrease' if d< -1e-10 else 'unchanged','metric_limit':restriction(t,ey),'comparison_limit':limits})
write('all_trait_comparisons.csv',rows)
# Literal file endpoints are descriptive examples with date/tie limitations.
manifest={r['game_id']:r for r in json.loads((ROOT/'results/manifest.json').read_text()) if r['status']=='parsed'}
for r in json.loads((OUT/'all_tatoh_provenance.json').read_text()):manifest[r['game_id']]=r
single=[];endpoints=[]
for player in ['DauT','TheViper','TaToH']:
 games=[r for r in base if r['player']==player and r['context']!='provisional Feudal-only' and r['window']=='whole available replay']
 def order(r):
  m=manifest[r['game_id']];name=m.get('file',r['game_id']);match=re.search(r'(?:_|\b)[gG](\d+)',name)
  return str(m.get('date','')),int(match.group(1)) if match else 99,name
 games.sort(key=order);a,b=games[0],games[-1]
 endpoints.append({'player':player,'early_game_id':a['game_id'],'early_date':manifest[a['game_id']].get('date'),'early_context':a['context'],'late_game_id':b['game_id'],'late_date':manifest[b['game_id']].get('date'),'late_context':b['context'],'warning':'Earliest dated available archive recording, not first career game. Month/upload dates do not establish exact within-period chronology. One-game contrast is highly variable.'})
 for window in ['first 10 game minutes','whole available replay']:
  aa=bykey.get((a['game_id'],player,window));bb=bykey.get((b['game_id'],player,window))
  for t in traits:
   x,y=num(aa.get(t)) if aa else None,num(bb.get(t)) if bb else None
   single.append({'player':player,'window':window,'trait':t,'early_game_id':a['game_id'],'late_game_id':b['game_id'],'early_value':x,'late_value':y,'difference':y-x if x is not None and y is not None else None,'limit':restriction(t,int(a['year']))})
write('single_game_endpoint_comparisons.csv',single);(OUT/'comparison_endpoints.json').write_text(json.dumps(endpoints,indent=2)+'\n')
# Readable tables include every trait; unavailable cells remain visible.
report=['# Earliest-to-latest analysis of all measured replay traits','','All available measurements are compared below. The 255-entry catalog includes candidates and controls; many require world state or visibility that has not been decoded. Those candidates are not silently treated as completed traits.','','The expanded command dataset has 98 verified player-game observations: 44 DauT/TheViper observations and 54 TaToH observations. One 6.2-minute TaToH replay is excluded from the ten-minute opening window. The community-attributed 2019 replay is analyzed separately.','','Each session/series receives equal weight inside a period; games share that cluster weight. Weighted medians are used for the headline comparison, with game medians and full observed ranges retained in CSV. This is descriptive analysis. The very small number of independent early clusters precludes reliable aging-effect inference.','','## Endpoint files','']
for r in endpoints:report.append(f"- {r['player']}: {r['early_game_id']} ({r['early_date']}, {r['early_context']}) → {r['late_game_id']} ({r['late_date']}, {r['late_context']}).")
report+=['','These are the earliest and latest dated files available here, not first/last career games. Exact month-level ordering can be uncertain. The single-game CSV provides the literal contrast; period tables provide a less brittle comparison.','','## Main interpretation','','DauT and TheViper issue more attributed commands in recent DE recordings than in the earliest classic files, but missing classic command ownership and different settings prevent interpreting the increase as improved cognition. Within DE, both show lower core-command rates in the opening but higher whole-game core rates. APM, deduplication, phase and command types change the result. TaToH has only one partial 2021 baseline; tournament and ranked comparisons must stay separate.','','No measured trait establishes reaction-time change, working-memory change, compensation or causal aging. Repetition, gaps, diversity and spatial switching are behavior measures. Actor-group comparisons from raw files have coverage artifacts; recent engine captures resolve actor lists but have no historical engine baseline.','','## Key measures','']
key=['all_recorded_cpm','core_cpm','dedup_core_cpm','core_gap_p50_s','core_gap_p99_s','command_silence_ge5s_time_fraction','core_gap_burstiness','core_category_entropy_bits','destination_jump_ge_quarter_fraction','rapid_destination_repeat_fraction']
for label,player,ey,ec,ly,lc,limits in comparisons:
 report+=['### '+label,'',f'{ey} {ec} → {ly} {lc}. Limits: {limits}.','','| Trait | Window | Early weighted median | Late weighted median | Direction |','|---|---|---:|---:|---|']
 for t in key:
  for window in ['first 10 game minutes','whole available replay']:
   r=next(r for r in rows if (r['comparison'],r['trait'],r['window'])==(label,t,window))
   def fmt(x):return 'unavailable' if x is None else f'{x:.4g}'
   report.append(f"| {t} | {window} | {fmt(r['early_weighted_median'])} | {fmt(r['late_weighted_median'])} | {r['direction']} |")
 report.append('')
report+=['## Every measured trait, with coverage','','These tables retain absent baselines as unavailable. Actor-selection numeric changes are reported for completeness but not interpreted as historical group-control changes.','']
for label,*_ in comparisons:
 report+=['### '+label,'','| Trait | Window | Early | Late | Δ | Games early/late |','|---|---|---:|---:|---:|---:|']
 for r in rows:
  if r['comparison']!=label:continue
  fmt=lambda x:'—' if x is None else f'{x:.4g}'
  report.append(f"| {r['trait']} | {r['window']} | {fmt(r['early_weighted_median'])} | {fmt(r['late_weighted_median'])} | {fmt(r['difference'])} | {r['early_n']}/{r['late_n']} |")
 report.append('')
report+=['## Unavailable or limited families','','- Economy, production uptime, combat efficiency, projectile dodges, visibility-conditioned response and multiple-front interference: world-state/visibility decoding is not completed.','- Recent actor-group measurements: available for six player-game observations, but no historical state-command baseline exists.','- Working-memory capacity, perceptual reaction time and compensation: not directly measured by any included table.','- Rating/peer trends: existing snapshot data are separate competitive outcomes, not earliest-game cognitive traits.','','## Reproduction','','Run expand_all_tatoh_features.py, expand_tatoh_details.py, then compare_all_traits.py. Inputs include raw replay files, the existing validated detail tables, and the quarantined 2019 candidate. Tables record weighting, sample counts, ranges, definitions and restrictions; no significance tests are claimed.']
md='\n'.join(report)+'\n';(OUT/'ALL_TRAITS_ANALYSIS.md').write_text(md)
# A searchable HTML table provides practical access to the complete analysis.
header=['comparison','player','trait','window','early_weighted_median','late_weighted_median','relative_change_percent','early_n','late_n','metric_limit','comparison_limit']
body=['<!doctype html><meta charset="utf-8"><title>All measured replay traits</title><style>body{font:15px system-ui;margin:30px;background:#111827;color:#e5e7eb}input{padding:12px;width:70%;font:inherit}table{border-collapse:collapse;width:100%;margin-top:20px}th,td{padding:8px;border-bottom:1px solid #374151;text-align:left}th{position:sticky;top:0;background:#1f2937}details{margin:20px 0}pre{white-space:pre-wrap;line-height:1.5}</style><h1>Earliest-to-latest: all measured traits</h1><p>Descriptive behavior; no causal aging claim. Blank baselines mean unavailable.</p><input id="filter" placeholder="Filter: player, metric, year comparison, or limitation" aria-label="Filter measured traits"><table><thead><tr>']
body+=['<th>'+html.escape(k)+'</th>' for k in header];body+=['</tr></thead><tbody>']
for r in rows:
 body.append('<tr>'+''.join('<td>'+html.escape('' if r[k] is None else f'{r[k]:.4g}' if isinstance(r[k],float) else str(r[k]))+'</td>' for k in header)+'</tr>')
body+=['</tbody></table><details><summary>Full interpretation and tables</summary><pre>'+html.escape(md)+'</pre></details><script>document.getElementById("filter").addEventListener("input",e=>{let q=e.target.value.toLowerCase();document.querySelectorAll("tbody tr").forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q))})</script>']
(OUT/'all_traits.html').write_text(''.join(body))
validation={'measured_trait_definitions':len(traits),'comparison_sets':len(comparisons),'windowed_comparison_rows':len(rows),'rows_with_both_periods':sum(r['direction']!='unavailable' for r in rows),'verified_player_game_observations':len({(r['game_id'],r['player']) for r in base if r['context']!='provisional Feudal-only'}),'provisional_2019_separate':True,'short_game_excluded_from_10_min_opening':True,'weighting':'equal series/session clusters; games share cluster weight; weighted median; midpoint when cumulative weight equals one half','state_traits_unavailable':True,'age_effect_identified':False}
(OUT/'all_traits_validation.json').write_text(json.dumps(validation,indent=2)+'\n');print(json.dumps(validation,indent=2))
