"""Package all measured comparisons and source replay files; preserve pilot ZIP."""
import csv,json,zipfile,hashlib,html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'deadline-sparse'
def read(p):
 with p.open() as f:return list(csv.DictReader(f))
comparisons=read(OUT/'all_trait_comparisons.csv');traits=sorted({r['trait'] for r in comparisons})
inventory=[]
for t in traits:
 units='game-clock seconds' if 'request_game_s' in t else 'fraction' if any(x in t for x in ['fraction','coverage','share']) else 'bits' if 'entropy' in t else 'nominal seconds' if t.endswith('_s') or '_s_' in t else 'commands per nominal minute' if 'cpm' in t or 'commands_nominal_min' in t else 'count or dimensionless; see source'
 source='decode.py / compare_all_traits.py' if 'request_game_s' in t else 'behavior_metrics.py' if t in list(read(OUT/'behavior_features_all.csv')[0])[8:] else 'replay_detail_features.py' if not t.startswith(('legacy_','tatoh_')) else 'analyze.py' if t.startswith('legacy_') else 'tatoh_analyze.py'
 definition='See source implementation; all-recorded actions are not all device inputs.'
 if t.startswith('core_gap_p') or t=='core_gap_max_s':definition='Positive inter-core-command gaps only, divided by recorded nominal speed.'
 elif t in ['core_gap_cv','core_gap_burstiness']:definition='Computed over all inter-core-command gaps, including zero gaps. CV=sd/mean; burstiness=(sd-mean)/(sd+mean).'
 elif t.startswith('command_silence_'):definition='Full duration of gaps at/above threshold divided by nominal window duration; includes window edges.'
 elif t=='peak_5s_nominal_cpm':definition='Maximum aligned five-nominal-second bin rate; final partial bin is duration-normalized. Not the sliding legacy ten-second measure.'
 elif t=='rapid_destination_repeat_fraction':definition='Share of consecutive valid movement/order destinations within 0.5 nominal seconds and two tiles, or same valid target when target IDs are retained. Actor identity and outcomes are not required.'
 elif t=='dedup_core_cpm':definition='Core commands minus approximate rapid destination repeats, divided by nominal minutes. Repeat rule/target coverage can differ from the separately stored TaToH legacy definition.'
 elif t=='legacy_core_silence_over5s_fraction':definition='Legacy time fraction in core-command gaps strictly greater than five seconds; edge gaps included.'
 elif 'request_game_s' in t:definition='First attributed RESEARCH request for technology 101/102/103; game-clock seconds. Not completed age-up. Starting-age, map settings and classic ownership affect comparison.'
 elif t.startswith('tatoh_'):definition='Previously computed TaToH phase or gap/re-click/age-up request definition. Phase fields retain their own named interval although stored on whole-replay rows.'
 eligible=[r for r in comparisons if r['trait']==t and r['direction']!='unavailable'];inventory.append({'trait':t,'units':units,'implementation':source,'definition':definition,'available_windowed_comparisons':len(eligible),'cognitive_construct':'Not directly measured','coverage_limit':'Raw actors: selection reuse affects coverage. Timing: classic/DE resolution differs. State/visibility absent.'})
with (OUT/'trait_dictionary.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(inventory[0]));w.writeheader();w.writerows(inventory)
status=[]
implemented={'Replay-derived APM':'all_recorded_cpm','Core command rate':'core_cpm','Command-type entropy':'core_type_entropy_bits','Command-category entropy':'core_category_entropy_bits','Type transition entropy':'core_type_transition_entropy_bits','Type switch rate':'core_type_switch_fraction','Category switch rate':'core_category_switch_fraction','Same-type triplet share':'core_same_type_triplet_fraction','Gap coefficient of variation':'core_gap_cv','Gap burstiness':'core_gap_burstiness','Median positive command gap':'core_gap_p50_s','p90 command gap':'core_gap_p90_s','p99 command gap':'core_gap_p99_s','Maximum command gap':'core_gap_max_s','Zero-gap command share':'simultaneous_core_gap_fraction','Five-second action-count variation':'core_count_5s_cv','Peak five-second action rate':'peak_5s_nominal_cpm','Empty five-second bin share':'empty_5s_bin_fraction','Command-silence time above five seconds':'command_silence_ge5s_time_fraction','Command-silence time above ten seconds':'command_silence_ge10s_time_fraction','First-command delay':'first_core_command_nominal_s','Approximate deduplicated command rate':'dedup_core_cpm','Median destination jump':'destination_jump_diagonal_p50','p90 destination jump':'destination_jump_diagonal_p90','Large destination-jump share':'destination_jump_ge_quarter_fraction','Destination entropy across map cells':'destination_entropy_4x4_bits','Destination-cell switch rate':'destination_cell_switch_fraction','Repeated nearby destination share':'rapid_destination_repeat_fraction','Build-command rate':'build_commands_nominal_min','Wall-command rate':'wall_commands_nominal_min','Research-command rate':'research_commands_nominal_min','Market-command rate':'market_commands_nominal_min','Requested queue batch size':'positive_queue_amount_mean','Production-building command revisits':'production_command_revisit_nominal_median_s','Technology-choice diversity':'distinct_research_type_ids','Unit-production diversity':'requested_queue_unit_type_ids','Target diversity':'distinct_order_target_ids','Commanded target diversity':'distinct_order_target_ids','First Feudal research request':'feudal_request_game_s','First Castle research request':'castle_request_game_s','First Imperial research request':'imperial_request_game_s','Explicit actor-group size':'actor_group_size_median','Explicit actor-group size p90':'actor_group_size_p90','Large explicit-group share':'actor_group_ge10_fraction','Explicit-group overlap':'actor_overlap_jaccard_median','Explicit-group change rate':'actor_group_change_fraction','Explicit production-building revisit interval':'production_command_revisit_nominal_median_s','Number of distinct commanded actor IDs':'commanded_actor_ids','Actor-list coverage':'explicit_actor_coverage','Coordinate coverage':'coordinate_coverage','Explicit actor coverage':'explicit_actor_coverage','Time in command gaps':'command_silence_ge5s_time_fraction'}
for r in read(OUT/'metric_catalog.csv'):
 metric=r['metric'];t=implemented.get(metric);cat=r['category'];state='Measured; see comparisons and restrictions' if t else 'Current engine-command measurements only; no historical engine baseline' if cat=='Command organization' and any(x in metric.lower() for x in ['group','actor']) else 'Competitive outcome/context available in separate snapshot tables' if cat=='Outcomes and relative performance' else 'Control/provenance; not an aging trait' if cat=='Coverage and controls' else 'Not implemented or not validated for earliest/latest comparison'
 status.append({'catalog_id':r['id'],'category':cat,'metric':metric,'status':state,'comparison_field':t or '', 'requirement':r['requirements']})
with (OUT/'catalog_comparison_status.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(status[0]));w.writeheader();w.writerows(status)
start='''# Start here: full earliest-to-latest replay analysis

- PLAYER_FINDINGS.md: the individual behavioral findings and limits.
- all_traits.html: searchable table of all comparisons.
- ALL_TRAITS_ANALYSIS.md: full period tables and definitions of scope.
- all_trait_comparisons.csv: 82 defined measurements/coverage fields across seven comparisons, with missing values retained.
- single_game_endpoint_comparisons.csv and comparison_endpoints.json: literal earliest/latest file contrasts.
- trait_dictionary.csv: source implementation, units and definition cautions.
- catalog_comparison_status.csv: status of each of the 255 candidate measurements/controls.
- behavior_features_all.csv and tatoh_detail_features_all.csv: expanded raw feature rows.
- engine_actor_features.csv: six recent player-game observations; no historical engine baseline.
- sample_outcome_summary.csv and competitive_rating_*.csv: separate match outcomes and previously collected rating snapshots.

The verified command dataset contains 98 player-game observations, with 195 phase/window rows. One short TaToH recording has no ten-minute opening row. The 2019 community-attributed FeudalVoy recording remains provisional and is not pooled into the verified baseline. Missing state/visibility metrics, reaction time, working-memory capacity and compensation are not invented.

Series/session days receive equal weight; games share each cluster's weight. Observed ranges are not confidence intervals. No causal aging effect or population significance test is claimed.

All source replay files used for these observations are included by SHA-256. Different recordings of the same match can have different hashes/viewpoint data, so file count is not match count. Full compressed engine-state streams remain in engine-pass outside this ZIP; command summaries and capture validation are included.

Use the existing repository environment to reproduce: expand_all_tatoh_features.py, expand_tatoh_details.py, compare_all_traits.py, compare_outcomes_snapshot.py, then bundle_all_traits.py. The ZIP contains input replay files and source feature tables but preserves repository-relative reproduction paths in provenance.
'''
(OUT/'START_HERE.md').write_text(start)
p=OUT/'all_traits.html';s=p.read_text();s=s.replace('<h1>Earliest-to-latest: all measured traits</h1>','<h1>Earliest-to-latest: all measured traits</h1><details open><summary>Individual player findings</summary><pre>'+html.escape((OUT/'PLAYER_FINDINGS.md').read_text())+'</pre></details>');p.write_text(s)
ids={r['game_id'] for r in read(ROOT/'results/game_metrics.csv')};main=[r for r in json.loads((ROOT/'results/manifest.json').read_text()) if r['game_id'] in ids]
provenance=main+json.loads((OUT/'all_tatoh_provenance.json').read_text());sources={r['sha256']:r for r in provenance}
(OUT/'all_source_replays.json').write_text(json.dumps(provenance,indent=2)+'\n')
zip_path=OUT/'submission-all-traits.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.iterdir()):
  if p.is_file() and p.suffix!='.zip' and p.name!='all_traits_bundle_validation.json':z.write(p,p.name)
 for sha,r in sources.items():
  p=ROOT/r['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==sha;z.write(p,'replays/'+sha+p.suffix)
 p=ROOT/'tatoh/raw/archive_2019_feudalvoy/recording.mgz';z.write(p,'provisional-2019/recording.mgz')
 for p in (ROOT/'scripts').glob('*.py'):z.write(p,'scripts/'+p.name)
 for p in [ROOT/'reanalysis-v2/game_features.csv',ROOT/'results/game_metrics.csv',ROOT/'results/manifest.json',ROOT/'tatoh/game_metrics.csv',ROOT/'tatoh/tournament_elo_peers.csv',ROOT/'requirements.txt']:
  z.write(p,'input-tables/'+str(p.relative_to(ROOT)))
 for p in (ROOT/'earlier-probes').glob('*.json'):z.write(p,'earlier-probes/'+p.name)
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None
 result={'zip_bytes':zip_path.stat().st_size,'zip_integrity_verified':True,'source_replay_files':len(sources),'provisional_extra_replay_files':1,'source_hashes_verified':True,'verified_player_game_observations':98,'state_frames_embedded':False}
(OUT/'all_traits_bundle_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
