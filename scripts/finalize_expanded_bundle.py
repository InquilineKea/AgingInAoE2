"""Update report, validate feature agreement, and package the expanded pilot."""
import json,csv,math,zipfile,html,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'deadline-sparse'
def read(p):
 with p.open() as f:return list(csv.DictReader(f))
v2={(r['game_id'],r['player'],r['window']):r for r in read(ROOT/'reanalysis-v2/game_features.csv')}
checked=0
for r in read(OUT/'behavior_features.csv'):
 window='whole game' if r['window']=='whole available replay' else r['window']
 original=v2.get((r['game_id'],r['player'],window))
 if original:
  assert math.isclose(float(r['core_cpm']),float(original['core_cpm_nominal']),rel_tol=1e-8,abs_tol=1e-8),(r['game_id'],window,r['core_cpm'],original['core_cpm_nominal'])
  checked+=1
captures=[]
for p in (ROOT/'engine-pass').glob('full-*/status.json'):
 s=json.loads(p.read_text())
 if s.get('complete_match_verified'):
  assert s['time_steps_skipped']==0
  assert abs(s['last_time_ms']-s['expected_duration_ms'])<=3000
  captures.append({'folder':p.parent.name,'frames':s['frames'],'commands':s['commands'],'last_game_time_ms':s['last_time_ms'],'compressed_bytes':(p.parent/'frames.pb.gz').stat().st_size,'zero_reported_skips':True})
v={'catalog_entries':len(read(OUT/'metric_catalog.csv')),'command_feature_observations':len(read(OUT/'behavior_features.csv'))//2,'command_features_per_window':31,'command_windows_compared_with_prior_verified_core_rate':checked,'core_rate_agreement':True,'engine_actor_observations':len(read(OUT/'engine_actor_features.csv'))//2,'complete_match_captures':captures,'complete_match_frames':sum(x['frames'] for x in captures),'state_schema_decoded':False,'2019_candidate_quarantined':True,'no_cognitive_constructs_measured':True}
(OUT/'expanded_validation.json').write_text(json.dumps(v,indent=2)+'\n')
text=['# Expanded metric analysis and earlier-game check','','The registry contains 255 candidate measurements and control variables. These are not 255 completed features. Thirty-one command-based numeric features were calculated for 49 player-game observations in opening and whole-available-replay windows. All 88 overlapping DauT/TheViper window command rates agree with the previously validated analysis. Actor-group metrics were additionally calculated for six recent player-game observations, with incomplete match coverage labeled.','','## Earlier-game coverage','','DauT: four 2011 recordings and seven 2012 team games are included in the expanded command analysis. TheViper: nine 2012 observations are included. Their classic-engine timestamp and ownership differences preclude direct high-resolution timing comparisons with DE. There is no newly verified sample before these earliest periods.','','TaToH: the 2019 archive contains a fully consumed 32.983-minute replay with +Zaid versus feudalVoy. Its uploader title and description explicitly attribute it to TaToH. This supports community attribution, not independent account identity. The replay appears to concern the Feudal-only challenge, so it is quarantined from the main unrestricted-play comparison. Its attributed opening replay command rate is 108.66 per nominal minute, but 20.9% of all replay actions have no player ownership and are omitted from player-specific rates. Do not interpret it as a verified basic-input APM baseline. See 2019_provisional_features.csv and 2019_provisional_provenance.json.','','The 2021 TaToH pack was retried with a cache refresh and byte-range request. It still returned exactly 524,288 bytes, and the range beyond that returned HTTP 416 with total size 524,288. Aocrecs failed TLS verification; certificate verification was retained. Archive search found the 2019 candidate but no additional verified earlier TaToH replay. Logs are included.','','## Completed state capture','','Four full matches are complete, containing '+str(v['complete_match_frames'])+' frames in total and zero reported skipped simulation steps. TheViper versus TaToH supplies data for both players. State-command summaries and actor-group features are included; raw state frames remain in engine-pass. Binary world state, projectile paths and player visibility have not been decoded, so this is not an onager-dodge analysis.','','## New features and interpretation','','Command volume, positive gap percentiles, longest gap, simultaneous command fraction, gap variation, burstiness, five-second activity variation, empty bins, time in long command silences, command-type/category entropy, transition entropy, category switches, repeated triplets, spatial destination entropy and jumps, and approximate deduplicated command rate are in behavior_features.csv. Whole-game and phase-specific values have different exposure and survivor composition. Classic timing fields are flagged as incomparable with DE.','','Engine actor features use explicit unit sets in humanOrder=true commands with an explicit player ID. Exact group size, overlap and revisit behavior describe command organization; they do not identify semantic tasks, attention or memory capacity. Flag fields are reported literally.','','For an aging study, prioritize opportunity-normalized visible-threat response, dodge success/damage avoidance, economy idle time during matched battle, and performance loss with simultaneous fronts. These need validated world state, player visibility and comparable repeated sessions. APM alone cannot isolate age effects.','','## Reproduce','','Use the repository environment and run deadline_sparse.py, extend_tatoh_submission.py, behavior_metrics.py, metric_catalog.py, earlier_candidate.py, engine_actor_features.py, then finalize_expanded_bundle.py. Raw data paths and source hashes are retained. No significance test or causal aging claim is presented.']
report='\n'.join(text)+'\n';(OUT/'EXPANDED_ANALYSIS.md').write_text(report)
p=OUT/'report.html';body=p.read_text();marker='<hr><pre># Expanded metric analysis';body=body.split(marker)[0];p.write_text(body+'<hr><pre>'+html.escape(report)+'</pre>')
with zipfile.ZipFile(OUT/'submission.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.iterdir()):
  if p.is_file() and p.name!='submission.zip':z.write(p,p.name)
 seen=set()
 for r in json.loads((OUT/'provenance.json').read_text())+json.loads((OUT/'tatoh_provenance.json').read_text()):
  if r['sha256'] in seen:continue
  seen.add(r['sha256']);p=ROOT/r['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'];z.write(p,'replays/'+r['sha256']+p.suffix)
 candidate=ROOT/'tatoh/raw/archive_2019_feudalvoy/recording.mgz';z.write(candidate,'provisional-2019/recording.mgz')
 for name in ['deadline_sparse.py','extend_tatoh_submission.py','behavior_metrics.py','metric_catalog.py','earlier_candidate.py','engine_actor_features.py','finalize_expanded_bundle.py']:
  z.write(ROOT/'scripts'/name,'scripts/'+name)
 for p in (ROOT/'earlier-probes').glob('*.json'):z.write(p,'earlier-probes/'+p.name)
with zipfile.ZipFile(OUT/'submission.zip') as z:assert z.testzip() is None
print(json.dumps(v,indent=2));print('ZIP bytes',(OUT/'submission.zip').stat().st_size)
