"""Additional descriptive command features; includes early classic samples."""
import csv,json,gzip,math,statistics as st,collections,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'deadline-sparse'
sys.path.insert(0,str(ROOT/'scripts'));import decode as D
orig=D.de_prefix;D.de_prefix=lambda data,save:orig(data,68.9 if 68<=save<68.9 else save)
CORE={'MOVE','ORDER','BUILD','RESEARCH','DELETE','BUY','SELL','WALL'}
def csvread(p):
 with p.open() as f:return list(csv.DictReader(f))
def csvwrite(name,rs):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
def quant(x,p):
 if not x:return None
 a=sorted(x);i=(len(a)-1)*p;k=int(i);return a[k]+(a[min(k+1,len(a)-1)]-a[k])*(i-k)
def entropy(xs):
 c=collections.Counter(xs);n=sum(c.values());return -sum(v/n*math.log2(v/n) for v in c.values()) if n else None
def category(t):
 return 'movement' if t=='MOVE' else 'interaction' if t=='ORDER' else 'construction' if t in {'BUILD','WALL'} else 'technology' if t=='RESEARCH' else 'market' if t in {'BUY','SELL'} else 'production' if 'QUEUE' in t else 'other'
def calc(acts,speed,end,dim):
 aa=sorted([a for a in acts if 0<=a['t']<end],key=lambda a:a['t']);cc=[a for a in aa if a['type'] in CORE];ts=[a['t']/speed for a in cc];total=end/speed
 gaps=[b-a for a,b in zip(ts,ts[1:])];positive=[x for x in gaps if x>0];edgegaps=[b-a for a,b in zip([0]+ts,ts+[total])]
 mean=st.mean(gaps) if gaps else None;sd=st.pstdev(gaps) if gaps else None
 bins=[0]*max(1,math.ceil(total/5))
 for t in ts:bins[min(int(t/5),len(bins)-1)]+=1
 nb=[5 if i<len(bins)-1 else total-5*i for i in range(len(bins))];binrates=[n/d*60 for n,d in zip(bins,nb) if d>0]
 types=[a['type'] for a in cc];cats=[category(a['type']) for a in cc]
 mo=[a for a in cc if a['type'] in {'MOVE','ORDER'}];xy=[a for a in mo if isinstance(a.get('x'),(int,float)) and isinstance(a.get('y'),(int,float)) and 0<=a['x']<dim and 0<=a['y']<dim] if dim else []
 jumps=[math.hypot(b['x']-a['x'],b['y']-a['y'])/(dim*math.sqrt(2)) for a,b in zip(xy,xy[1:])]
 cells=[(min(3,int(a['x']/dim*4)),min(3,int(a['y']/dim*4))) for a in xy]
 repeat=0
 for a,b in zip(xy,xy[1:]):
  target=a.get('target_id');same=target not in (None,-1) and target==b.get('target_id')
  repeat+=((b['t']-a['t'])/speed<=.5 and (math.hypot(b['x']-a['x'],b['y']-a['y'])<=2 or same))
 transitions=collections.Counter(zip(types,types[1:]));prev=collections.Counter(types[:-1]);nt=sum(transitions.values())
 cond=-sum(v/nt*math.log2(v/prev[a]) for (a,b),v in transitions.items()) if nt else None
 def fraction(num,den):return num/den if den else None
 return dict(all_recorded_cpm=len(aa)/total*60,core_cpm=len(cc)/total*60,noncore_action_fraction=fraction(len(aa)-len(cc),len(aa)),first_core_command_nominal_s=ts[0] if ts else None,core_gap_p10_s=quant(positive,.1),core_gap_p50_s=quant(positive,.5),core_gap_p90_s=quant(positive,.9),core_gap_p99_s=quant(positive,.99),core_gap_max_s=max(positive) if positive else None,simultaneous_core_gap_fraction=fraction(sum(x==0 for x in gaps),len(gaps)),core_gap_cv=sd/mean if mean else None,core_gap_burstiness=(sd-mean)/(sd+mean) if mean and sd+mean else None,command_silence_ge5s_time_fraction=sum(x for x in edgegaps if x>=5)/total,command_silence_ge10s_time_fraction=sum(x for x in edgegaps if x>=10)/total,core_count_5s_cv=st.pstdev(bins)/st.mean(bins) if st.mean(bins) else None,peak_5s_nominal_cpm=max(binrates),empty_5s_bin_fraction=sum(x==0 for x in bins)/len(bins),core_type_entropy_bits=entropy(types),core_category_entropy_bits=entropy(cats),core_type_transition_entropy_bits=cond,core_type_switch_fraction=fraction(sum(a!=b for a,b in zip(types,types[1:])),len(types)-1),core_category_switch_fraction=fraction(sum(a!=b for a,b in zip(cats,cats[1:])),len(cats)-1),core_same_type_triplet_fraction=fraction(sum(a==b==c for a,b,c in zip(types,types[1:],types[2:])),len(types)-2),coordinate_coverage=fraction(len(xy),len(mo)),destination_jump_diagonal_p50=quant(jumps,.5),destination_jump_diagonal_p90=quant(jumps,.9),destination_jump_ge_quarter_fraction=fraction(sum(x>=.25 for x in jumps),len(jumps)),destination_entropy_4x4_bits=entropy(cells),destination_cell_switch_fraction=fraction(sum(a!=b for a,b in zip(cells,cells[1:])),len(cells)-1),rapid_destination_repeat_fraction=fraction(repeat,len(xy)-1),dedup_core_cpm=(len(cc)-repeat)/total*60)
if __name__ == '__main__':
 metrics=csvread(ROOT/'results/game_metrics.csv');manifest={r['game_id']:r for r in json.loads((ROOT/'results/manifest.json').read_text()) if r['status']=='parsed'}
 actions=collections.defaultdict(list)
 with gzip.open(ROOT/'reanalysis-v2/detailed_actions.jsonl.gz','rt') as f:
  for line in f:
   a=json.loads(line);actions[(a['game_id'],a['target_player'])].append(a)
 result=[]
 for r in metrics:
  m=manifest[r['game_id']];acts=actions[(r['game_id'],r['player'])]
  for window,end in [('first 10 game minutes',600),('whole available replay',float(m['duration_game_min'])*60)]:
   result.append(dict(game_id=r['game_id'],player=r['player'],year=r['year'],context=r['context'],cluster=r['cluster'],window=window,timing_comparable_to_de=int(r['year'])>=2021,partial_match=False,**calc(acts,float(m['speed']),end,float(r['map_dimension']))))
 for r in csvread(OUT/'tatoh_selected_games.csv'):
  path=next((ROOT/'tatoh/raw'/r['game']).glob('*.aoe2record'));meta,acts=D.decode(path);p=next(p for p in meta['players'] if p.get('profile_id')==197388 or p['name']=='Le Loi');aa=[a for a in acts if a['player']==p['number']]
  for window,end in [('first 10 game minutes',600),('whole available replay',meta['duration_s'])]:
   result.append(dict(game_id=r['game'],player='TaToH',year=r['period'][:4],context=r['period'][5:],cluster=r['cluster'],window=window,timing_comparable_to_de=True,partial_match=r['partial'],**calc(aa,meta['speed'],end,meta.get('dimension'))))
 csvwrite('behavior_features.csv',result)
 summary=[]
 features=list(result[0])[8:]
 for player,year,context,window in sorted({(r['player'],r['year'],r['context'],r['window']) for r in result}):
  rs=[r for r in result if (r['player'],r['year'],r['context'],r['window'])==(player,year,context,window)]
  vals={}
  for k in features:
   v=[r[k] for r in rs if r[k] is not None];vals[k]=st.median(v) if v else None
  summary.append(dict(player=player,year=year,context=context,window=window,n_games=len(rs),n_clusters=len({r['cluster'] for r in rs}),**vals))
 csvwrite('behavior_period_summary.csv',summary)
 (OUT/'behavior_validation.json').write_text(json.dumps({'player_game_observations':len(result)//2,'windows':len(result),'numeric_features':len(features),'classic_timing_not_comparable':True,'command_destinations_not_unit_motion':True,'state_schema_decoded':False,'no_age_effect_tests':True},indent=2)+'\n')
 print('Computed',len(features),'features for',len(result)//2,'player-game observations; first ten minutes and whole available replay.')
