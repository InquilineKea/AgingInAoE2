"""Phase-matched command trajectories and observed-session fatigue proxies.

These measurements do not identify cognitive reserve or normalize game-state demand.
Run with the existing replay-parser environment. Inputs retain original provenance.
"""
from pathlib import Path
import collections, csv, datetime as dt, gzip, hashlib, json, math, statistics as st
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'stamina'
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / 'scripts'))
from mgz import fast
from mgz.fast.header import decompress, parse_version
import behavior_metrics as B

CORE = B.CORE
FIELDS = ('x', 'y', 'object_ids', 'target_id', 'building_id', 'technology_id', 'unit_id', 'amount')

def read(path):
    with path.open() as stream: return list(csv.DictReader(stream))

def write(name, rows):
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with (OUT / name).open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)

def quant(values, p): return B.quant(values, p)

def metrics(actions, speed, start, end, dimension):
    assert end > start
    aa = [a for a in actions if start <= a['t'] < end]
    core = [a for a in aa if a['type'] in CORE]
    times = [(a['t'] - start) / speed for a in core]
    duration = (end - start) / speed
    gaps = [b-a for a,b in zip(times,times[1:])]
    # Equal-duration complete 10-nominal-second bins; omit terminal partial bins.
    nbins = int((duration + 1e-9) // 10)
    bins = [0] * nbins
    for t in times:
        k = int(t // 10)
        if k < nbins: bins[k] += 1
    rates = [n*6 for n in bins]
    edge_gaps = [b-a for a,b in zip([0]+times,times+[duration])]
    movement = [a for a in core if a['type'] in {'MOVE','ORDER'}]
    valid = [a for a in movement if isinstance(a.get('x'), (int,float)) and isinstance(a.get('y'), (int,float)) and 0 <= a['x'] < dimension and 0 <= a['y'] < dimension]
    repeats = 0
    for a,b in zip(valid,valid[1:]):
        same_target = a.get('target_id') not in (None,-1,0,4294967295) and a.get('target_id') == b.get('target_id')
        repeats += (b['t']-a['t'])/speed <= .5 and (math.hypot(a['x']-b['x'],a['y']-b['y']) <= 2 or same_target)
    production = [a for a in aa if 'QUEUE' in a['type'] and (a.get('amount') or 0) > 0]
    actors = [a for a in movement if a.get('object_ids')]
    return {
        'window_game_seconds': end-start, 'window_nominal_seconds': duration,
        'n_recorded_actions': len(aa), 'n_core_commands': len(core),
        'all_recorded_cpm': len(aa)/duration*60, 'core_cpm': len(core)/duration*60,
        'burst_p95_10s_core_cpm': quant(rates,.95), 'peak_10s_core_cpm': max(rates) if rates else None,
        'complete_10s_bins': nbins, 'adjacent_core_gaps': len(gaps),
        'long_gap_count_gt5s': sum(g>5 for g in gaps),
        'p_core_gap_gt5s': sum(g>5 for g in gaps)/len(gaps) if gaps else None,
        'core_gap_p50_s': quant([g for g in gaps if g>0],.5),
        'core_gap_p99_s': quant([g for g in gaps if g>0],.99),
        'silence_time_gt5s_fraction': sum(g for g in edge_gaps if g>5)/duration,
        'approx_repeat_pairs': repeats,
        'approx_repeat_pairs_per_core_command': repeats/len(core) if core else None,
        'approx_dedup_core_cpm': (len(core)-repeats)/duration*60,
        'explicit_actor_coverage': len(actors)/len(movement) if movement else None,
        'distinct_explicit_actor_ids': len({i for a in actors for i in a['object_ids']}),
        'distinct_commanded_production_ids': len({i for a in production for i in a.get('object_ids',[])}),
        'positive_queue_request_cpm': len(production)/duration*60,
        'core_category_entropy_bits': B.entropy([B.category(a['type']) for a in core]),
    }

def ratio(a,b): return a/b if a is not None and b not in (None,0) else None
def difference(a,b): return a-b if a is not None and b is not None else None

def weighted_summary(rows, field):
    valid = [r for r in rows if r.get(field) is not None and math.isfinite(r[field])]
    if not valid: return {'weighted_median':None,'game_median':None,'min':None,'max':None,'n':0,'clusters':0}
    counts = collections.Counter(r['cluster'] for r in valid)
    pairs = sorted((r[field],1/counts[r['cluster']]) for r in valid)
    half = sum(w for _,w in pairs)/2; total = 0
    for i,(value,weight) in enumerate(pairs):
        total += weight
        if total >= half-1e-12:
            if math.isclose(total,half,abs_tol=1e-12) and i+1<len(pairs): value=(value+pairs[i+1][0])/2
            break
    values = [v for v,_ in pairs]
    return {'weighted_median':value,'game_median':st.median(values),'min':min(values),'max':max(values),'n':len(valid),'clusters':len(counts)}

def parse_date(value):
    if not value or 'T' not in value: return None
    t = dt.datetime.fromisoformat(value.replace('Z','+00:00'))
    return t.replace(tzinfo=dt.timezone.utc) if t.tzinfo is None else t

def load_games():
    main = read(ROOT/'results/game_metrics.csv')
    main_manifest = {r['game_id']:r for r in json.loads((ROOT/'results/manifest.json').read_text()) if r['status']=='parsed'}
    detail = collections.defaultdict(list)
    with gzip.open(ROOT/'reanalysis-v2/detailed_actions.jsonl.gz','rt') as stream:
        for line in stream:
            a=json.loads(line); detail[(a['game_id'],a['target_player'])].append(a)
    games=[];checks=[]
    for r in main:
        m=main_manifest[r['game_id']];path=ROOT/m['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==m['sha256']
        with gzip.open(ROOT/'results/decoded'/(m['sha256']+'.json.gz'),'rt') as stream: meta=json.load(stream)['meta']
        actions=[a for a in detail[(r['game_id'],r['player'])] if a.get('player')==int(r['player_slot'])]
        assert len([a for a in actions if a['type'] in CORE and 0 <= a['t'] < meta['duration_s']])==int(r['n_commands'])
        games.append(dict(game_id=r['game_id'],player=r['player'],year=int(r['year']),context=r['context'],cluster=r['cluster'],date=r['date'],duration=meta['duration_s'],speed=meta['speed'],dimension=int(r['map_dimension']),partial=False,map_id=r['map_id'],file=m['file'],sha256=m['sha256'],actions=actions))
        checks.append({'game_id':r['game_id'],'player':r['player'],'source_hash_verified':True,'command_count_agrees':True,'source':'preserved detailed body export'})
    tata={r['game']:r for r in read(ROOT/'tatoh/game_metrics.csv') if r['who']=='TaToH'}
    for i,m in enumerate(json.loads((ROOT/'deadline-sparse/all_tatoh_provenance.json').read_text())):
        path=ROOT/m['file']; assert hashlib.sha256(path.read_bytes()).hexdigest()==m['sha256']
        actions=[];ts=0
        with path.open('rb') as stream:
            head=decompress(stream);version,game,save,log=parse_version(head,stream)
            header=B.D.de_prefix(head,save)
            me=next(p for p in header['players'] if p['number']==m['slot'])
            assert me['name']==m['identity']
            if m['year']=='2026': assert me['profile_id']==197388
            assert abs(header['speed']-m['nominal_speed'])<1e-8
            fast.meta(stream)
            while stream.tell()<path.stat().st_size:
                op,payload=fast.operation(stream)
                if op is fast.Operation.SYNC: ts+=payload[0]
                elif op is fast.Operation.ACTION:
                    typ,p=payload
                    if p.get('player_id')==m['slot']:
                        actions.append(dict(t=ts/1000,type=typ.name,**{k:p[k] for k in FIELDS if k in p}))
            assert stream.tell()==m['body_end']==path.stat().st_size
        assert ts/1000==m['duration_game_seconds']
        date=dt.datetime.fromtimestamp(header['timestamp'],dt.timezone.utc).isoformat() if header.get('timestamp') else m['date']
        games.append(dict(game_id=m['game_id'],player='TaToH',year=int(m['year']),context=m['context'],cluster=m['cluster'],date=date,duration=ts/1000,speed=m['nominal_speed'],dimension=m['dimension'],partial=m['partial'],map_id=header['map_id'],file=m['file'],sha256=m['sha256'],actions=actions))
        checks.append({'game_id':m['game_id'],'player':'TaToH','source_hash_verified':True,'body_end_verified':True,'clock_verified':True,'identity_verified':True,'source':'fresh full replay body'})
        if (i+1)%10==0: print('Parsed TaToH',i+1,'of 54',flush=True)
    (OUT/'source_validation.json').write_text(json.dumps(checks,indent=2)+'\n')
    assert len(games)==98
    return games

def session_metadata(games, gap_minutes=30):
    """Use the complete cached match listing where available, including unparsed games."""
    listing=json.loads((ROOT/'tatoh/aoe2companion_matches_2026-08-10_to_2026-10-04.json').read_text())
    selected={g['game_id']:g for g in games if g['year']==2026}
    pool=collections.defaultdict(list);uncovered=[]
    for context,entries in [('ranked',listing['rm_1v1']),('tournament',listing['unranked'])]:
        seen=set()
        for m in entries:
            if m['matchId'] in seen:continue
            seen.add(m['matchId']);start=parse_date(m.get('started'));end=parse_date(m.get('finished'))
            if not start or not end or end<start: continue
            pool[('TaToH','all cached modes')].append({'id':('ranked_' if context=='ranked' else 'lobby_')+str(m['matchId']),'start':start,'end':end,'source':'cached account match log across ranked and unranked modes (includes games without parsed replays)'})
    for g in selected.values():
        if g['player']=='TaToH':continue
        start=parse_date(g['date'])
        if start:pool[(g['player'],g['context'])].append({'id':g['game_id'],'start':start,'end':start+dt.timedelta(seconds=g['duration']/g['speed']),'source':'sampled replay timestamps; unobserved games cannot be excluded'})
    mapped={};sessions=[]
    for (player,context),entries in sorted(pool.items()):
        entries.sort(key=lambda x:x['start']);groups=[]
        for entry in entries:
            if not groups or (entry['start']-groups[-1][-1]['end']).total_seconds()>gap_minutes*60:
                groups.append([])
            groups[-1].append(entry)
        for group in groups:
            start=group[0]['start'];sid=f'{player}_{context}_{start.isoformat()}';active=0
            for ordinal,entry in enumerate(group,1):
                mapped[entry['id']]={'session_id':sid,'observed_game_ordinal':ordinal,'session_elapsed_hours':(entry['start']-start).total_seconds()/3600,'prior_logged_play_hours':active/3600,'session_source':entry['source'],'session_logged_games':len(group),'session_start_is_observed_lower_bound':True}
                active+=(entry['end']-entry['start']).total_seconds()
            sessions.append({'session_id':sid,'player':player,'context':context,'session_start_utc':start.isoformat(),'logged_games':len(group),'parsed_games':sum(e['id'] in selected for e in group),'observed_elapsed_hours':(group[-1]['end']-start).total_seconds()/3600,'gap_threshold_minutes':gap_minutes,'session_source':group[0]['source']})
    for g in selected.values():
        if g['game_id'] not in mapped:uncovered.append(g['game_id'])
    return mapped,sessions,uncovered

def summarize_sessions(games, open_rows, gap_minutes):
    mapped,sessions,uncovered=session_metadata(games,gap_minutes)
    bysession=collections.defaultdict(list)
    for r in open_rows:
        if r['year']==2026 and r['game_id'] in mapped:
            bysession[(mapped[r['game_id']]['session_id'],r['context'])].append({**r,**mapped[r['game_id']]})
    first_last=[];opening=[]
    fields=['core_cpm','burst_p95_10s_core_cpm','p_core_gap_gt5s','approx_dedup_core_cpm']
    for (sid,context),rows in bysession.items():
        rows.sort(key=lambda r:r['observed_game_ordinal']);opening+=rows
        if len(rows)<3:continue
        first,last=rows[0],rows[-1]
        delta_hours=last['session_elapsed_hours']-first['session_elapsed_hours']
        if delta_hours<=0:continue
        summary={'player':first['player'],'context':first['context'],'session_id':sid,'cluster':sid,'gap_threshold_minutes':gap_minutes,'n_openings':len(rows),'first_game_id':first['game_id'],'last_game_id':last['game_id'],'first_observed_ordinal':first['observed_game_ordinal'],'last_observed_ordinal':last['observed_game_ordinal'],'hours_between_first_last_openings':delta_hours,'session_source':first['session_source']}
        xs=[r['session_elapsed_hours'] for r in rows];mx=st.mean(xs);den=sum((x-mx)**2 for x in xs)
        for field in fields:
            vals=[r[field] for r in rows]
            summary[field+'_first']=first[field];summary[field+'_last']=last[field]
            summary[field+'_last_minus_first']=difference(last[field],first[field])
            summary[field+'_last_over_first']=ratio(last[field],first[field])
            summary[field+'_slope_per_hour']=sum((x-mx)*(v-st.mean(vals)) for x,v in zip(xs,vals))/den if all(v is not None for v in vals) and den else None
        ordinal_target=first['observed_game_ordinal']+5
        sixth=next((r for r in rows if r['observed_game_ordinal']==ordinal_target),None)
        summary['sixth_relative_observed_game_id']=sixth['game_id'] if sixth else None
        summary['sixth_over_first_open_core_cpm']=ratio(sixth['core_cpm'],first['core_cpm']) if sixth else None
        first_last.append(summary)
    return first_last,opening,sessions,uncovered

def main():
    # Meaningful checks: time scaling, strict threshold, and interval boundaries.
    steady=[{'t':t*.5*2,'type':'MOVE'} for t in range(2400)]
    a=metrics(steady,2,0,600,120);b=metrics(steady,2,600,1200,120)
    assert a['core_cpm']==b['core_cpm']==120 and a['p_core_gap_gt5s']==0
    five=metrics([{'t':t,'type':'MOVE'} for t in [0,5,10]],1,0,11,120)
    assert five['p_core_gap_gt5s']==0
    assert metrics([{'t':t,'type':'MOVE'} for t in [0,5,10]],1,0,10,120)['n_core_commands']==2
    games=load_games();window_rows=[];paired=[];cohort=[]
    existing={(r['game_id'],r['player'],r['window']):r for r in read(ROOT/'deadline-sparse/behavior_features_all.csv')}
    for g in games:
        base={k:g[k] for k in ['game_id','player','year','context','cluster','date','partial','map_id','sha256']}
        base.update(duration_game_min=g['duration']/60,long_game_45plus=g['duration']>=2700)
        windows=[]
        for i in range(4):
            start=i*600;end=start+600
            if end<=g['duration']:windows.append((f'{i*10}-{(i+1)*10}',start,end,'clock phase'))
        if g['duration']>2400:windows.append(('40+',2400,g['duration'],'clock phase; variable length'))
        if g['duration']>=2700:
            windows.extend([('40-45',2400,2700,'clock phase; fixed five minutes'),('40+ excluding final 60 game seconds',2400,g['duration']-60,'terminal minute sensitivity')])
        for tech,label in [(101,'Feudal'),(102,'Castle'),(103,'Imperial')]:
            request=next((a['t'] for a in g['actions'] if a['type']=='RESEARCH' and a.get('technology_id')==tech),None)
            if request is not None:
                for offset in [0,300]:
                    start=request+offset;end=start+300
                    if end<=g['duration']:windows.append((f'{label} request +{offset//60}-{offset//60+5} min',start,end,'request anchor; not completed age or combat phase'))
        rows={}
        for label,start,end,kind in windows:
            r={**base,'window':label,'window_kind':kind,'start_game_s':start,'end_game_s':end,**metrics(g['actions'],g['speed'],start,end,g['dimension'])}
            rows[label]=r;window_rows.append(r)
        if '0-10' in rows:
            old=existing[(g['game_id'],g['player'],'first 10 game minutes')]
            assert math.isclose(rows['0-10']['core_cpm'],float(old['core_cpm']),rel_tol=1e-10)
            assert math.isclose(rows['0-10']['all_recorded_cpm'],float(old['all_recorded_cpm']),rel_tol=1e-10)
        cohort.append({**base,'qualifies_45plus':g['duration']>=2700,'state_demand_measured':False,'useful_state_change_measured':False})
        if g['duration']>=2700:
            opening=rows['0-10']
            for label in ['40+','40-45','40+ excluding final 60 game seconds']:
                late=rows[label]
                paired.append({**base,'late_window':label,'opening_core_cpm':opening['core_cpm'],'late_core_cpm':late['core_cpm'],'core_cpm_late_over_open':ratio(late['core_cpm'],opening['core_cpm']),'opening_burst_p95_10s_core_cpm':opening['burst_p95_10s_core_cpm'],'late_burst_p95_10s_core_cpm':late['burst_p95_10s_core_cpm'],'burst_p95_late_over_open':ratio(late['burst_p95_10s_core_cpm'],opening['burst_p95_10s_core_cpm']),'peak_10s_late_over_open':ratio(late['peak_10s_core_cpm'],opening['peak_10s_core_cpm']),'opening_p_core_gap_gt5s':opening['p_core_gap_gt5s'],'late_p_core_gap_gt5s':late['p_core_gap_gt5s'],'p_core_gap_gt5s_late_minus_open':difference(late['p_core_gap_gt5s'],opening['p_core_gap_gt5s']),'silence_time_late_minus_open':difference(late['silence_time_gt5s_fraction'],opening['silence_time_gt5s_fraction']),'approx_dedup_late_over_open':ratio(late['approx_dedup_core_cpm'],opening['approx_dedup_core_cpm'])})
    write('cohort_inventory.csv',cohort);write('window_metrics.csv',window_rows);write('long_game_paired_changes.csv',paired)
    summary=[]
    for player,year,context,window in sorted({(r['player'],r['year'],r['context'],r['late_window']) for r in paired}):
        rows=[r for r in paired if (r['player'],r['year'],r['context'],r['late_window'])==(player,year,context,window)]
        for field in ['opening_core_cpm','late_core_cpm','core_cpm_late_over_open','burst_p95_late_over_open','peak_10s_late_over_open','p_core_gap_gt5s_late_minus_open','silence_time_late_minus_open','approx_dedup_late_over_open']:
            summary.append({'player':player,'year':year,'context':context,'late_window':window,'metric':field,**weighted_summary(rows,field)})
    write('long_game_period_summary.csv',summary)
    open_rows=[r for r in window_rows if r['window']=='0-10']
    all_sessions=[];primary=None;session_summary=[]
    for threshold in [15,30,60]:
        first_last,openings,sessions,uncovered=summarize_sessions(games,open_rows,threshold)
        all_sessions+=first_last
        if threshold==30:
            primary=first_last;write('session_opening_metrics.csv',openings);write('observed_session_inventory.csv',sessions)
            (OUT/'session_uncovered_games.json').write_text(json.dumps(uncovered,indent=2)+'\n')
        for player,context in sorted({(r['player'],r['context']) for r in first_last}):
            group=[r for r in first_last if (r['player'],r['context'])==(player,context)]
            for field in ['core_cpm_last_over_first','burst_p95_10s_core_cpm_last_over_first','p_core_gap_gt5s_last_minus_first','approx_dedup_core_cpm_last_over_first','core_cpm_slope_per_hour','p_core_gap_gt5s_slope_per_hour']:
                vals=[r[field] for r in group if r[field] is not None]
                session_summary.append({'player':player,'context':context,'gap_threshold_minutes':threshold,'metric':field,'sessions':len(vals),'median':st.median(vals) if vals else None,'min':min(vals) if vals else None,'max':max(vals) if vals else None,'positive_sessions':sum(v> (1 if 'over_first' in field else 0) for v in vals),'negative_sessions':sum(v< (1 if 'over_first' in field else 0) for v in vals)})
    write('session_first_last_and_slopes.csv',all_sessions);write('session_summary.csv',session_summary)
    # Fixed-phase summaries preserve the same qualifying long-game cohort throughout.
    phases=[]
    for player,year,context in sorted({(r['player'],r['year'],r['context']) for r in paired}):
        for label in ['0-10','10-20','20-30','30-40','40-45']:
            rs=[r for r in window_rows if r['long_game_45plus'] and (r['player'],r['year'],r['context'],r['window'])==(player,year,context,label)]
            for field in ['core_cpm','burst_p95_10s_core_cpm','p_core_gap_gt5s','approx_dedup_core_cpm']:
                phases.append({'player':player,'year':year,'context':context,'window':label,'metric':field,**weighted_summary(rs,field)})
    write('long_game_phase_summary.csv',phases)
    anchors=[]
    for player,year,context,window in sorted({(r['player'],r['year'],r['context'],r['window']) for r in window_rows if r['year']>=2021 and 'request' in r['window']}):
        rs=[r for r in window_rows if(r['player'],r['year'],r['context'],r['window'])==(player,year,context,window)]
        for field in ['core_cpm','burst_p95_10s_core_cpm','p_core_gap_gt5s','approx_dedup_core_cpm']:
            anchors.append({'player':player,'year':year,'context':context,'window':window,'metric':field,**weighted_summary(rs,field)})
    write('request_anchor_period_summary.csv',anchors)
    long_count=sum(g['duration']>=2700 for g in games)
    fixed=[r for r in window_rows if r['long_game_45plus'] and r['window'] in ['0-10','10-20','20-30','30-40','40-45']]
    assert len(fixed)==long_count*5
    fixed_groups=collections.defaultdict(set)
    for r in fixed:fixed_groups[r['game_id'],r['player']].add(r['window'])
    assert all(len(v)==5 for v in fixed_groups.values())
    for r in window_rows:
        n=r['adjacent_core_gaps'];count=r['long_gap_count_gt5s']
        assert 0<=count<=n and r['n_core_commands']<=r['n_recorded_actions']
        if n:assert math.isclose(r['p_core_gap_gt5s'],count/n,abs_tol=1e-12)
        assert r['core_cpm']==r['n_core_commands']/r['window_nominal_seconds']*60
    validation={'verified_player_game_observations':len(games),'openings':len(open_rows),'qualifying_long_player_game_observations':long_count,'long_game_unique_source_files':len({g['sha256'] for g in games if g['duration']>=2700}),'window_rows':len(window_rows),'source_hashes_verified':True,'fresh_tatoh_body_clock_and_identity_verified':54,'existing_opening_rates_match':True,'metric_boundary_checks_pass':True,'game_state_demand_measured':False,'useful_state_change_per_command_measured':False,'causal_aging_effect_identified':False,'historical_exact_session_timestamps_available':False,'session_analysis_year':2026,'session_analysis_uses_cached_unparsed_matches':True,'primary_session_break_minutes':30,'sensitivity_session_break_minutes':[15,60],'same_45plus_cohort_in_all_five_clock_windows_verified':True,'gap_numerators_denominators_verified':True,'core_rates_count_and_duration_verified':True,'primary_eligible_observed_session_contexts':len(primary),'phase_request_anchor_window_rows':sum('request' in r['window'] for r in window_rows)}
    (OUT/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    print(json.dumps(validation,indent=2))

if __name__=='__main__':main()
