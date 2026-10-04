"""Reproducible descriptive pilot, not a cognitive or causal aging study."""
from pathlib import Path
import sys,json,gzip,hashlib,collections,re,datetime,math
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from decode import decode
ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/'results';CACHE=RESULTS/'decoded';CACHE.mkdir(exist_ok=True)
# Restricted to types with explicit ownership in all included replay generations.
CORE={'MOVE','ORDER','BUILD','RESEARCH','DELETE','BUY','SELL','WALL'}
CLASS={'MOVE':'movement','ORDER':'order','BUILD':'construction','WALL':'construction','RESEARCH':'research','DELETE':'delete','BUY':'market','SELL':'market'}
SOURCE_HC='https://ageofnotes.com/tutorials/hidden-cup-4-download-all-recorded-games-hc4-2021/'

def entropy(values):
 if len(values)==0:return float('nan')
 n=np.array(list(collections.Counter(values).values()),dtype=float);p=n/n.sum();return float(-(p*np.log2(p)).sum())

def metrics(actions,meta,number,start=0,end=None):
 end=min(meta['duration_s'],end if end is not None else meta['duration_s']);duration=end-start
 selected=[a for a in actions if a['player']==number and a['type'] in CORE and start<=a['t']<end]
 t=np.array([a['t'] for a in selected]);g=np.diff(t);positive=g[g>0]
 types=[CLASS[a['type']] for a in selected]
 speed=meta['speed'];real_duration=duration/speed
 out=dict(n_commands=len(t),duration_game_min=duration/60,nominal_duration_min=real_duration/60,core_cpm_game=len(t)/(duration/60),core_cpm_nominal=len(t)/(real_duration/60),gap_median_game_s=float(np.median(g)) if len(g) else None,gap_median_nominal_s=float(np.median(g)/speed) if len(g) else None,gap_p95_nominal_s=float(np.percentile(g,95)/speed) if len(g) else None,positive_gap_p10_nominal_s=float(np.percentile(positive,10)/speed) if len(positive) else None,zero_gap_fraction=float(np.mean(g==0)) if len(g) else None,command_class_entropy_bits=entropy(types),switches_per_100_commands=100*sum(x!=y for x,y in zip(types,types[1:]))/max(1,len(types)-1))
 # Silent-time fraction counts only spells between observed core commands,
 # with each spell >5 nominal seconds contributing its full duration.
 gaps=np.diff(np.r_[start,t,end])/speed
 out['core_silence_over5s_fraction']=float(gaps[gaps>5].sum()/real_duration)
 # Max 10 nominal-second window, implemented with sorted event-time search.
 window=10*speed
 out['peak_10s_nominal_cpm']=float(max((np.searchsorted(t,x+window,side='left')-i for i,x in enumerate(t)),default=0)*6)
 coords=[(a['x'],a['y']) for a in selected if a['x'] is not None and a['y'] is not None and 0<=a['x']<meta['dimension'] and 0<=a['y']<meta['dimension']]
 out['coordinate_fraction']=len(coords)/max(1,len(t))
 cells=[(int(x/meta['dimension']*4),int(y/meta['dimension']*4)) for x,y in coords]
 out['spatial_entropy_4x4_bits']=entropy(cells)
 out['spatial_cell_switch_per100']=100*sum(x!=y for x,y in zip(cells,cells[1:]))/max(1,len(cells)-1)
 out['move_share']=types.count('movement')/max(1,len(types))
 out['planning_command_share']=sum(x in ['construction','research','market'] for x in types)/max(1,len(types))
 # DE-only production batching: positive queue commands, not cancel actions.
 queue=[a for a in actions if a['player']==number and a['type']=='DE_QUEUE' and start<=a['t']<end and a['amount'] is not None and a['amount']>0]
 out['queue_batch_mean']=float(np.mean([a['amount'] for a in queue])) if queue else None
 out['queue_batch_gt1_fraction']=float(np.mean([a['amount']>1 for a in queue])) if queue else None
 out['queue_commands']=len(queue)
 return out

seen_hashes={}
manifest=[];all_records=[];failures=[];command_rows=[];coverage_rows=[];phase_rows=[]
files=sorted([p for p in (ROOT/'raw').glob('*/*') if p.suffix.lower() in ['.aoe2record','.mgx','.mgz'] and p.parent.name.startswith(('hc4_','daut_','viper_','historical_'))])
for path in files:
 digest=hashlib.sha256(path.read_bytes()).hexdigest();cache=CACHE/(digest+'.json.gz')
 try:
  if cache.exists():
   with gzip.open(cache,'rt') as f:obj=json.load(f)
   meta,actions=obj['meta'],obj['actions']
  else:
   meta,actions=decode(path)
   with gzip.open(cache,'wt') as f:json.dump(dict(meta=meta,actions=actions),f)
  folder=path.parent.name
  if folder.startswith('hc4_'):year=2021;source=SOURCE_HC;date='2021-03 (HC4)';date_precision='tournament month';context='1v1 tournament';cluster=folder
  elif folder.startswith(('daut_','viper_')):year=2026;source='https://www.aoe2insights.com/match/'+folder.split('_')[1]+'/';date=meta['date_utc'];date_precision='header UTC';context='1v1 ranked';cluster=folder.split('_')[0]+'_2026_session'
  else:
   ident=int(folder.split('_')[1]);year=2011 if ident==110 else 2012;source='https://uu.getuploader.com/toric/download/'+str(ident);date={110:'2011-11 (uploaded 2011-11-29)',147:'2012-05 (uploaded 2012-05-27)',119:'2012-01-06 (filename; uploaded 2012-01-07)',159:'2012-08-24 (filename; uploaded 2012-08-26)'}[ident];date_precision='upload/filename, game date unverified';context='1v1 challenge' if len(meta['players'])==2 else 'team game';cluster=folder
  id=digest[:12];targets=[]
  for p in meta['players']:
   name=p['name'].lower()
   target='DauT' if 'daut' in name or name=='gonzalo pizarro' else ('TheViper' if 'theviper' in name or name=='ivaylo' else None)
   if target:
    if year==2026:assert p['profile_id']=={'DauT':198035,'TheViper':196240}[target]
    targets.append((target,p))
  assert len(meta['players']) in [2,4,6,8]
  duplicate_of=seen_hashes.get(digest)
  if not duplicate_of:seen_hashes[digest]=str(path.relative_to(ROOT))
  by_type=collections.defaultdict(lambda:collections.Counter())
  numbers={p['number'] for p in meta['players']}
  for a in actions:
   assert a['t']<=meta['duration_s']
   by_type[a['type']]['total']+=1
   by_type[a['type']]['attributed']+=int(a['player'] in numbers)
  local_coverage=[]
  for typ,c in by_type.items():
   local_coverage.append(dict(game_id=id,year=year,type=typ,**c))
   if typ in CORE:assert c['attributed']==c['total'],(path.name,typ,c)
  coverage_rows.extend(local_coverage)
  row=dict(game_id=id,file=str(path.relative_to(ROOT)),sha256=digest,source_url=source,year=year,date=date,date_precision=date_precision,context=context,cluster=cluster,player_names=[p['name'] for p in meta['players']],target_players=[x[0] for x in targets],duration_game_min=meta['duration_s']/60,speed=meta['speed'],save_version=meta['save_version'],decoder=meta['decoder'],sync_checks=meta['sync_checks'],body_end=meta['body_end'],file_bytes=path.stat().st_size,restore_time=meta.get('restore_time',0),map_id=meta['map_id'],map_dimension=meta['dimension'],status='parsed' if targets else 'parsed; no target player, excluded')
  assert row['restore_time']==0
  if duplicate_of:
   row['status']='duplicate; excluded'
   row['duplicate_of']=duplicate_of
  manifest.append(row)
  if duplicate_of:
   print(path.name,'DUPLICATE excluded',flush=True)
   continue
  for target,p in targets:
   base=dict(game_id=id,player=target,year=year,date=date,context=context,cluster=cluster,player_slot=p['number'],alias=p['name'],civilization_id=p['civilization_id'],map_id=meta['map_id'],map_dimension=meta['dimension'],winner=(p['number'] not in meta['resigned']) if meta['resigned'] and context!='team game' else None)
   record={**base,**metrics(actions,meta,p['number'])};all_records.append(record)
   for a in actions:
    if a['player']==p['number']:
     command_rows.append(dict(game_id=id,player=target,year=year,**{k:v for k,v in a.items() if k!='player'}))
   if meta['duration_s']>=600:
    phase_rows.append({**base,'phase':'first 10 game minutes',**metrics(actions,meta,p['number'],0,600)})
   for start in range(0,int(meta['duration_s']),300):
    end=min(start+300,meta['duration_s'])
    if end-start>=120:phase_rows.append({**base,'phase':f'{start//60}–{end//60} game minutes',**metrics(actions,meta,p['number'],start,end)})
  print(path.name,'OK',year,[x[0] for x in targets],flush=True)
 except Exception as e:
  failures.append(dict(file=str(path.relative_to(ROOT)),sha256=digest,error=type(e).__name__+': '+str(e)));print('FAILED',path.name,str(e),flush=True)
(RESULTS/'manifest.json').write_text(json.dumps(manifest,indent=2));(RESULTS/'failures.json').write_text(json.dumps(failures,indent=2))
for name,rows in [('game_metrics',all_records),('command_coverage',coverage_rows),('phase_metrics',phase_rows)]:pd.DataFrame(rows).to_csv(RESULTS/(name+'.csv'),index=False)
pd.DataFrame(command_rows).to_csv(RESULTS/'commands.csv.gz',index=False,compression='gzip')
df=pd.DataFrame(all_records)
cols=['core_cpm_game','core_cpm_nominal','gap_median_nominal_s','gap_p95_nominal_s','peak_10s_nominal_cpm','switches_per_100_commands','command_class_entropy_bits','spatial_entropy_4x4_bits','planning_command_share','queue_batch_mean','queue_batch_gt1_fraction','duration_game_min']
summary=df.groupby(['player','year','context'])[cols].median().reset_index();ns=df.groupby(['player','year','context']).agg(n_games=('game_id','size'),n_clusters=('cluster','nunique')).reset_index();summary=summary.merge(ns,on=['player','year','context']);summary.to_csv(RESULTS/'period_summary.csv',index=False)
ph=pd.DataFrame(phase_rows);ph[ph.phase=='first 10 game minutes'].groupby(['player','year','context'])[cols].median().reset_index().to_csv(RESULTS/'opening_summary.csv',index=False)
# Six paired 2012 games: same lobby, same timestamps/engine, descriptive control.
tg=df[(df.year==2012)&(df.cluster=='historical_147')]
paired=tg.pivot(index='game_id',columns='player',values=cols)
rows=[]
for gid in paired.index:
 row={'game_id':gid}
 for c in cols:row[c+'_viper_minus_daut']=paired.loc[gid,(c,'TheViper')]-paired.loc[gid,(c,'DauT')]
 rows.append(row)
pd.DataFrame(rows).to_csv(RESULTS/'paired_2012_differences.csv',index=False)
# Full site-defined tournament-Elo sequence, excluding synthetic initial/current entries.
history=[]
for player,key in [('DauT','daut'),('TheViper','viper')]:
 c=json.loads((ROOT/'sources'/('elo-'+key+'-chart.json')).read_text());footer=c['footers'][player];title=c['titles'][player];events=c['events'][player];previous=None
 for i,rating in c['series'][0]['data']:
  if i>=len(footer) or not footer[i]:continue
  event=BeautifulSoup(events.get(str(i),''),'html.parser').get_text(' ',strip=True);date=footer[i];year=int(date[-4:]);t=BeautifulSoup(title[i],'html.parser').get_text(' | ',strip=True)
  outcome='win' if 'victory' in event else ('loss' if 'defeat' in event else ('draw' if 'draw' in event else 'unknown'))
  history.append(dict(player=player,sequence=i,date_source=date,date_precision='day' if ',' in date else 'month',year=year,elo=rating,event=t,outcome=outcome,opponent_event=event))
  previous=rating
hist=pd.DataFrame(history);hist.to_csv(RESULTS/'tournament_history.csv',index=False)
yearly=hist.groupby(['player','year']).agg(series=('elo','size'),elo_median=('elo','median'),elo_last=('elo','last'),elo_min=('elo','min'),elo_max=('elo','max'),wins=('outcome',lambda x:sum(x=='win')),losses=('outcome',lambda x:sum(x=='loss')),draws=('outcome',lambda x:sum(x=='draw')),unknown=('outcome',lambda x:sum(x=='unknown'))).reset_index();yearly['series_win_fraction']=yearly.wins/yearly.series;yearly.to_csv(RESULTS/'tournament_years.csv',index=False)
print('FILES',len(manifest),'target observations',len(df),'failures',failures,flush=True)
print(summary.to_string(index=False),flush=True)
