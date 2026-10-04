"""Independent source and metric invariants for the Memb extension."""
from pathlib import Path
import collections,csv,gzip,hashlib,json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'memb'
CORE={'MOVE','ORDER','BUILD','RESEARCH','DELETE','BUY','SELL','WALL'}
def read(path):return list(csv.DictReader(path.open()))
def main():
    downloads=json.loads((OUT/'downloads.json').read_text());available=[r for r in downloads if 'file' in r]
    for r in available:assert hashlib.sha256((ROOT/r['file']).read_bytes()).hexdigest()==r['sha256']
    inv=read(OUT/'game_inventory.csv');meta={r['game_id']:r for r in inv};assert len(meta)==len(inv)
    excluded=json.loads((OUT/'excluded_recordings.json').read_text())
    assert len(inv)+len(excluded)==len(available)
    assert all(r['duration_game_seconds']<60 for r in excluded)
    actions=collections.defaultdict(list)
    with gzip.open(OUT/'owned_commands.jsonl.gz','rt') as f:
        for line in f:
            a=json.loads(line);actions[a['game_id']].append(a)
    assert set(actions)==set(meta)
    for gid,aa in actions.items():
        assert all(a['player']==int(meta[gid]['slot']) for a in aa)
        assert all(x['t']<=y['t'] for x,y in zip(aa,aa[1:]))
    windows=read(OUT/'window_metrics.csv')
    for r in windows:
        aa=actions[r['game_id']];speed=float(meta[r['game_id']]['nominal_speed'])
        label=r['window']
        if ' request ' in label:
            age=label.split()[0];tech={'Feudal':101,'Castle':102,'Imperial':103}[age]
            request=next(a['t'] for a in aa if a['type']=='RESEARCH' and a.get('technology_id')==tech)
            offset=int(label.split('+')[1].split('-')[0])*60;start=request+offset;end=start+300
        else:start,end=[int(s)*60 for s in label.split('-')]
        times=[(a['t']-start)/speed for a in aa if a['type'] in CORE and start<=a['t']<end]
        gaps=np.diff(times);duration=(end-start)/speed
        assert len(times)==int(r['n_core_commands'])
        assert len(gaps)==int(r['adjacent_core_gaps'])
        assert int(sum(gaps>5))==int(r['long_gap_count_gt5s'])
        assert math.isclose(len(times)/duration*60,float(r['core_cpm']),abs_tol=1e-8)
        assert len(gaps) and math.isclose(float(np.mean(gaps>5)),float(r['p_core_gap_gt5s']),abs_tol=1e-12)
        n=int((duration+1e-9)//10);counts=[sum(k*10<=t<(k+1)*10 for t in times)*6 for k in range(n)]
        assert n==int(r['complete_10s_bins'])
        assert math.isclose(float(np.percentile(counts,95)),float(r['burst_p95_10s_core_cpm']),abs_tol=1e-8)
    original=read(ROOT/'deadline-sparse/all_trait_comparisons.csv');combined=read(OUT/'all_players_trait_comparisons.csv')
    assert combined[:len(original)]==original,'Original comparison rows changed'
    assert all(not r['early_weighted_median'] and not r['difference'] and r['direction']=='unavailable' for r in combined[len(original):])
    longids={r['game_id'] for r in read(OUT/'long_game_paired_changes.csv')}
    for gid in longids:assert float(meta[gid]['duration_game_minutes'])>=45
    report={'source_replay_hashes_verified':len(available),'eligible_observations':len(inv),'short_abort_exclusions':len(excluded),
        'owned_actor_slot_and_monotonic_clock_verified':True,'independently_recomputed_phase_windows':len(windows),
        'gap_denominators_strict_threshold_and_p95_bursts_verified':True,'original_comparison_rows_preserved':len(original),
        'historical_memb_contrasts_withheld':True,'qualifying_long_game_cohort':len(longids)}
    (OUT/'independent_verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
