"""Actor-group behavior from captured engine commands, not decoded world state."""
import json,gzip,csv,statistics as st,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'deadline-sparse'
slots={}
with (ROOT/'results/game_metrics.csv').open() as f:
 for r in csv.DictReader(f):slots[(r['game_id'],r['player'])]=int(r['player_slot'])
slots[('3598af4f05ca','TaToH')]=2;slots[('61c225f6fcca','TaToH')]=2
folders=['full-c7d3588daf74-attempt-2','full-a467a9f1780f','full-3598af4f05ca','full-67f43712e111','full-61c225f6fcca-attempt-2'];rows=[]
for folder in folders:
 p=ROOT/'engine-pass'/folder;status=json.loads((p/'status.json').read_text());source=json.loads((p/'source.json').read_text());gid=source['game_id']
 with gzip.open(p/'commands.jsonl.gz','rt') as f:commands=[json.loads(l) for l in f]
 for (game,player),slot in slots.items():
  if game!=gid:continue
  for window,end in [('first 10 game minutes',600000),('whole available replay',status['last_time_ms']+1)]:
   aa=[a for a in commands if a['game_time_ms']<end and a['payload'].get('commPlayerId')==slot and a['payload'].get('humanOrder') is True]
   unit=[a for a in aa if 'unitIds' in a['payload']];u=[a for a in unit if a['payload']['unitIds']]
   groups=[frozenset(a['payload']['unitIds']) for a in u];pairs=list(zip(groups,groups[1:]));overlap=[len(a&b)/len(a|b) for a,b in pairs]
   history={};revisits=[];interposed=[]
   for i,(a,g) in enumerate(zip(u,groups)):
    if g in history:
     j,t=history[g];revisits.append((a['game_time_ms']-t)/1000);interposed.append(i-j-1)
    history[g]=(i,a['game_time_ms'])
   sizes=sorted(len(g) for g in groups)
   def med(a):return st.median(a) if a else None
   def frac(n,d):return n/d if d else None
   rows.append(dict(game_id=gid,player=player,window=window,complete_match=status['complete_match_verified'],available_game_seconds=status['last_time_ms']/1000,attributed_human_order_commands=len(aa),commands_with_unit_list=len(unit),nonempty_unit_list_coverage=frac(len(u),len(unit)),distinct_actor_groups=len(set(groups)),distinct_actor_ids=len(set().union(*groups)) if groups else 0,actor_group_size_median=med(sizes),actor_group_size_p90=sizes[int((len(sizes)-1)*.9)] if sizes else None,actor_group_ge10_fraction=frac(sum(len(g)>=10 for g in groups),len(groups)),adjacent_group_change_fraction=frac(sum(a!=b for a,b in pairs),len(pairs)),adjacent_nonoverlapping_group_fraction=frac(sum(not(a&b) for a,b in pairs),len(pairs)),adjacent_group_jaccard_median=med(overlap),exact_group_revisit_game_s_median=med(revisits),exact_group_revisit_game_s_p90=sorted(revisits)[int((len(revisits)-1)*.9)] if revisits else None,interposed_commands_before_exact_group_return_median=med(interposed),exact_group_repeat_under1_game_s_fraction=frac(sum(t<1 for t in revisits),len(revisits)),control_held_flag_fraction=frac(sum(a['payload'].get('controlHeld') is True for a in u),len(u)),instant_false_flag_fraction=frac(sum(a['payload'].get('instant') is not True for a in u),len(u))))
with (OUT/'engine_actor_features.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(OUT/'engine_actor_scope.json').write_text(json.dumps({'player_game_observations':len(rows)//2,'state_decoded':False,'scope':'Known command payloads with explicit commPlayerId and humanOrder=true. Group means exact set of commanded IDs, not a semantic task or army. Game seconds are not human reaction time. Flag fields reported literally; not validated cognitive constructs. Partial captures labeled.'},indent=2)+'\n')
print('engine actor rows',len(rows))
