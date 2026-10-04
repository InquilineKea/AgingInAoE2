"""Audit an unvalidated DE synchronization-counter normalization on long games.

The upstream parser explicitly describes counter meanings as guesses. This script
does not validate living-unit counts, workload, useful output or cognitive reserve.
"""
from pathlib import Path
import csv,json,hashlib,collections,math,statistics as st
from mgz import fast
from mgz.fast.header import decompress,parse_version

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'stamina'
def read(p):
    with p.open() as f:return list(csv.DictReader(f))
def write(name,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def summarize(rows,field):
    valid=[r for r in rows if r[field] is not None];counts=collections.Counter(r['cluster'] for r in valid)
    pairs=sorted((r[field],1/counts[r['cluster']]) for r in valid);half=sum(w for _,w in pairs)/2;cum=0
    for i,(v,w) in enumerate(pairs):
        cum+=w
        if cum>=half-1e-12:
            if math.isclose(cum,half,abs_tol=1e-12) and i+1<len(pairs):v=(v+pairs[i+1][0])/2
            break
    return {'weighted_median':v,'game_median':st.median(r[field] for r in valid),'min':min(r[field] for r in valid),'max':max(r[field] for r in valid),'n':len(valid),'clusters':len(counts)} if valid else {'weighted_median':None,'n':0,'clusters':0}

cohort=[r for r in read(OUT/'cohort_inventory.csv') if r['qualifies_45plus']=='True' and int(r['year'])>=2021]
main={(r['game_id'],r['player']):r for r in read(ROOT/'results/game_metrics.csv')}
tat={r['game_id']:r for r in json.loads((ROOT/'deadline-sparse/all_tatoh_provenance.json').read_text())}
manifest={r['game_id']:r for r in json.loads((ROOT/'results/manifest.json').read_text()) if r['status']=='parsed'}
windows=read(OUT/'window_metrics.csv');snapshots=[];measures=[];paired=[];checks=[]
for i,g in enumerate(cohort):
    if g['player']=='TaToH':m=tat[g['game_id']];slot=m['slot'];path=ROOT/m['file']
    else:m=manifest[g['game_id']];slot=int(main[g['game_id'],g['player']]['player_slot']);path=ROOT/m['file']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==g['sha256']
    samples=[];ts=0;checked=0;missing=0
    with path.open('rb') as f:
        head=decompress(f);parse_version(head,f);fast.meta(f)
        while f.tell()<path.stat().st_size:
            op,payload=fast.operation(f)
            if op is fast.Operation.SYNC:
                ts+=payload[0];stats=payload[2]
                if stats:
                    assert abs(stats['current_time']-ts)<=1000
                    checked+=1
                    if slot in stats:
                        data=stats[slot];samples.append({'t':ts/1000,**data})
                        snapshots.append({'game_id':g['game_id'],'player':g['player'],'year':g['year'],'t_game_s':ts/1000,'slot':slot,**data})
                    else:missing+=1
        assert f.tell()==path.stat().st_size
    rows={}
    for w in windows:
        if (w['game_id'],w['player'])!=(g['game_id'],g['player']) or w['window'] not in ['0-10','10-20','20-30','30-40','40-45','40+']:continue
        start=float(w['start_game_s']);end=float(w['end_game_s']);integral=0;covered=0;segments=0
        for a,b in zip(samples,samples[1:]+[{'t':ts/1000}]):
            lo=max(start,a['t']);hi=min(end,b['t'])
            # Do not carry counters over a long missing-snapshot interval.
            if hi>lo and b['t']-a['t']<=30:
                integral+=a['obj_count']*(hi-lo);covered+=hi-lo;segments+=1
        coverage=covered/(end-start);mean=integral/covered if covered else None
        rate=float(w['core_cpm']);intensity=100*rate/mean if mean and coverage>=.95 else None
        r={k:g[k] for k in ['game_id','player','year','context','cluster','partial','sha256']}
        r.update(window=w['window'],sync_segments=segments,counter_time_coverage=coverage,time_weighted_obj_count_field=mean,core_cpm=rate,core_cpm_per100_obj_count_field=intensity,counter_semantics_validated=False,independent_workload_measured=False,useful_output_measured=False)
        rows[w['window']]=r;measures.append(r)
    first=rows['0-10'];late=rows['40-45']
    paired.append({k:g[k] for k in ['game_id','player','year','context','cluster','partial']})
    r=paired[-1];r.update(opening_obj_count_field=first['time_weighted_obj_count_field'],late_obj_count_field=late['time_weighted_obj_count_field'],obj_counter_late_over_open=late['time_weighted_obj_count_field']/first['time_weighted_obj_count_field'] if first['time_weighted_obj_count_field'] else None,core_cpm_late_over_open=late['core_cpm']/first['core_cpm'],counter_normalized_core_late_over_open=late['core_cpm_per100_obj_count_field']/first['core_cpm_per100_obj_count_field'] if first['core_cpm_per100_obj_count_field'] else None,minimum_counter_time_coverage=min(first['counter_time_coverage'],late['counter_time_coverage']))
    checks.append({'game_id':g['game_id'],'player':g['player'],'source_hash_verified':True,'sync_clock_verified':True,'sync_checks':checked,'missing_player_payloads':missing,'first_player_snapshot_game_s':samples[0]['t'] if samples else None,'body_end_verified':True,'counter_semantics_validated':False})
    print('Audited synchronization counters',i+1,'/',len(cohort),flush=True)
write('sync_counter_snapshots.csv',snapshots);write('sync_counter_window_audit.csv',measures);write('sync_counter_paired_audit.csv',paired)
summary=[]
for player,year,context in sorted({(r['player'],r['year'],r['context']) for r in paired}):
    rs=[r for r in paired if(r['player'],r['year'],r['context'])==(player,year,context)]
    for field in ['obj_counter_late_over_open','core_cpm_late_over_open','counter_normalized_core_late_over_open']:
        summary.append({'player':player,'year':year,'context':context,'metric':field,**summarize(rs,field)})
write('sync_counter_period_audit.csv',summary)
(OUT/'sync_counter_validation.json').write_text(json.dumps({'observations':len(cohort),'snapshot_rows':len(snapshots),'source_checks':checks,'upstream_source':'https://github.com/happyleavesaoc/aoc-mgz/pull/123','parser_version':'mgz 1.8.51','upstream_semantics_explicitly_guessed':True,'living_units_not_validated':True,'independent_workload_not_validated':True,'zero_resource_player_payloads_can_be_omitted_by_upstream_parser':True,'minimum_coverage_for_intensity':.95,'max_snapshot_carry_seconds':30,'results_exploratory_only':True},indent=2)+'\n')
print('Synchronization proxy audit complete',len(cohort),'observations')
