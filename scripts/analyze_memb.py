"""Add MembTV as a distinct cohort using the existing descriptive definitions.

No historical or cross-context aging contrast is fabricated. Session boundaries
use all cached public match logs, including unsampled and short games.
"""
from pathlib import Path
import collections, csv, datetime as dt, gzip, hashlib, json, statistics as st, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import behavior_metrics as B
import replay_detail_features as R
import stamina_analysis as S
from mgz import fast
OUT=ROOT/'memb'

def write(name,rows):
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def date(value):return dt.datetime.fromisoformat(value.replace('Z','+00:00'))

def session_map(matches,threshold):
    ordered=sorted([m for m in matches if m.get('started') and m.get('finished')],key=lambda m:m['started'])
    result={};session=0;last_finish=None;start=None;ordinal=0
    for m in ordered:
        t=date(m['started']);finish=date(m['finished'])
        if last_finish is None or (t-last_finish).total_seconds()>threshold*60:
            session+=1;start=t;ordinal=0
        ordinal+=1;sid=f'memb-{threshold}-{session}'
        result[m['matchId']]={'session_id':sid,'observed_game_ordinal':ordinal,
            'session_elapsed_hours':(t-start).total_seconds()/3600,
            'left_log_boundary_censored':session==1}
        last_finish=max(finish,last_finish) if last_finish else finish
    return result

def main():
    matches=json.loads((OUT/'match-log.json').read_text());matchmap={m['matchId']:m for m in matches}
    downloads=json.loads((OUT/'downloads.json').read_text())
    games=[];traits=[];windows=[];longs=[];failures=[];exclusions=[];actions_export=[]
    for row in downloads:
        if 'file' not in row:continue
        path=ROOT/row['file'];mid=row['match_id'];match=matchmap[mid]
        try:
            assert hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256']
            meta,_=B.D.decode(path)
            me=[p for p in meta['players'] if p.get('profile_id')==196407]
            assert len(me)==1;me=me[0]
            assert abs((date(meta['date_utc'])-date(match['started'])).total_seconds())<120
            assert meta['body_end']==path.stat().st_size
            if meta['duration_s']<60:
                exclusions.append({'game_id':mid,'file':row['file'],'duration_game_seconds':meta['duration_s'],
                    'reason':'Aborted recording under one game minute; excluded before command analysis',
                    'profile_and_start_verified':True,'body_end_verified':True,'sync_checks':meta['sync_checks']})
                print(mid,'excluded short abort',meta['duration_s'],flush=True)
                continue
            assert meta['sync_checks']>0
            aa=[];ts=0
            with path.open('rb') as f:
                f.seek(meta['body_start']);fast.meta(f)
                while f.tell()<path.stat().st_size:
                    op,payload=fast.operation(f)
                    if op is fast.Operation.SYNC:ts+=payload[0]
                    elif op is fast.Operation.ACTION:
                        typ,p=payload
                        if p.get('player_id')==me['number']:
                            a={'t':ts/1000,'type':typ.name,'player':me['number']}
                            a.update({k:p.get(k) for k in R.FIELDS});aa.append(a)
            assert abs(ts/1000-meta['duration_s'])<1e-6
            context='1v1 ranked' if match['leaderboard']=='rm_1v1' else f"{len(meta['players'])}-player {match['leaderboard']} {match['mapName']}"
            age=(date(match['started']).date()-dt.date(1977,7,22)).days/365.2425
            base={'game_id':str(mid),'player':'MembTV','year':date(match['started']).year,
                'date':match['started'],'context':context,'cluster':match['started'][:10],
                'map':match['mapName'],'map_dimension':meta['dimension'],'civilization_id':me['civilization_id'],
                'profile_id':196407,'slot':me['number'],'age_years':age}
            games.append({**base,'duration_game_minutes':meta['duration_s']/60,'nominal_speed':meta['speed'],
                'players':len(meta['players']),'file':row['file'],'sha256':row['sha256'],
                'sync_checks':meta['sync_checks'],'header_date_agrees':True,'body_end_agrees':True,
                'save_version':meta['save_version'],'postgame_present':meta['operations'].get('POSTGAME',0)>0})
            # The presence of POSTGAME validates a completed recording; missing
            # POSTGAME is retained as partial and is not silently called a match.
            for name,end in [('whole available replay',meta['duration_s']),('first 10 game minutes',600)]:
                if end>meta['duration_s']:continue
                x=B.calc(aa,meta['speed'],end,meta['dimension'])
                y=R.features(aa,meta,me['number'],end)
                assert abs(x['core_cpm']-y['core_cpm_nominal'])<1e-8
                traits.append({**base,'window':name,**x,**y})
            for start in range(0,int(meta['duration_s']),600):
                end=start+600
                if end<=meta['duration_s']:
                    windows.append({**base,'window':f'{start//60}-{end//60}',
                        **S.metrics(aa,meta['speed'],start,end,meta['dimension'])})
            if meta['duration_s']>=2700:
                opening=S.metrics(aa,meta['speed'],0,600,meta['dimension'])
                for label,start,end in [('40-45',2400,2700),('40+',2400,meta['duration_s']),('40+ excluding final minute',2400,meta['duration_s']-60)]:
                    late=S.metrics(aa,meta['speed'],start,end,meta['dimension'])
                    longs.append({**base,'late_window':label,'partial_recording':not games[-1]['postgame_present'],
                        'core_cpm_late_over_opening':S.ratio(late['core_cpm'],opening['core_cpm']),
                        'burst_p95_late_over_opening':S.ratio(late['burst_p95_10s_core_cpm'],opening['burst_p95_10s_core_cpm']),
                        'p_gap_late_minus_opening':S.difference(late['p_core_gap_gt5s'],opening['p_core_gap_gt5s']),
                        'opening_core_cpm':opening['core_cpm'],'late_core_cpm':late['core_cpm'],
                        'opening_gap_count':opening['adjacent_core_gaps'],'late_gap_count':late['adjacent_core_gaps']})
            for tid,label in [(101,'Feudal'),(102,'Castle'),(103,'Imperial')]:
                request=next((a['t'] for a in aa if a['type']=='RESEARCH' and a.get('technology_id')==tid),None)
                if request is not None:
                    for offset in (0,300):
                        start=request+offset;end=start+300
                        if end<=meta['duration_s']:
                            windows.append({**base,'window':f'{label} request +{offset//60}-{offset//60+5}',
                                **S.metrics(aa,meta['speed'],start,end,meta['dimension'])})
            actions_export += [{'game_id':str(mid),**a} for a in aa]
            print(mid,'verified',round(meta['duration_s']/60,1),'minutes',len(aa),'owned actions',flush=True)
        except Exception as e:failures.append({'game_id':mid,'file':row['file'],'error':type(e).__name__+': '+str(e)})
    write('game_inventory.csv',games);write('trait_metrics.csv',traits);write('window_metrics.csv',windows);write('long_game_paired_changes.csv',longs)
    (OUT/'excluded_recordings.json').write_text(json.dumps(exclusions,indent=2)+'\n')
    with gzip.open(OUT/'owned_commands.jsonl.gz','wt') as f:
        for a in actions_export:f.write(json.dumps(a,separators=(',',':'))+'\n')
    summary=[]
    fields=[k for k in traits[0] if k not in base and k!='window'] if traits else []
    for context,window in sorted({(r['context'],r['window']) for r in traits}):
        rows=[r for r in traits if r['context']==context and r['window']==window]
        summary.append({'player':'MembTV','context':context,'window':window,'games':len(rows),
            'day_clusters':len({r['cluster'] for r in rows}),
            **{k:S.weighted_summary(rows,k)['weighted_median'] for k in fields}})
    write('trait_summary.csv',summary)
    longsummary=[]
    for context,label in sorted({(r['context'],r['late_window']) for r in longs}):
        rows=[r for r in longs if r['context']==context and r['late_window']==label]
        longsummary.append({'context':context,'late_window':label,'games':len(rows),
            'day_clusters':len({r['cluster'] for r in rows}),
            **{k:S.weighted_summary(rows,k)['weighted_median'] for k in ['core_cpm_late_over_opening','burst_p95_late_over_opening','p_gap_late_minus_opening']}})
    write('long_game_summary.csv',longsummary)
    sessions=[];sessionopen=[];opens=[r for r in windows if r['window']=='0-10']
    for threshold in (15,30,60):
        mapped=session_map(matches,threshold)
        bysession=collections.defaultdict(list)
        for r in opens:
            m=mapped[int(r['game_id'])];row={**r,**m,'gap_threshold_minutes':threshold}
            sessionopen.append(row);bysession[(m['session_id'],r['context'])].append(row)
        for (sid,context),rows in bysession.items():
            rows.sort(key=lambda r:r['observed_game_ordinal'])
            logged=[mid for mid,m in mapped.items() if m['session_id']==sid]
            sampled={int(r['game_id']) for r in games}|{r['game_id'] for r in exclusions}
            complete_sampling=all(mid in sampled for mid in logged)
            if len(rows)<3:continue
            first,last=rows[0],rows[-1]
            item={'session_id':sid,'context':context,'gap_threshold_minutes':threshold,
                'n_openings':len(rows),'logged_games':len(logged),'sample_covers_all_logged_games':complete_sampling,
                'left_log_boundary_censored':first['left_log_boundary_censored'],
                'first_game_id':first['game_id'],'last_game_id':last['game_id'],
                'hours_between_first_last':last['session_elapsed_hours']-first['session_elapsed_hours']}
            for k in ['core_cpm','burst_p95_10s_core_cpm','p_core_gap_gt5s','approx_dedup_core_cpm']:
                item[k+'_last_over_first']=S.ratio(last[k],first[k]);item[k+'_last_minus_first']=S.difference(last[k],first[k])
                xs=[r['session_elapsed_hours'] for r in rows];ys=[r[k] for r in rows];mx=st.mean(xs)
                den=sum((x-mx)**2 for x in xs)
                item[k+'_slope_per_hour']=sum((x-mx)*(y-st.mean(ys)) for x,y in zip(xs,ys))/den if den and all(y is not None for y in ys) else None
            sessions.append(item)
    write('session_opening_metrics.csv',sessionopen);write('session_comparisons.csv',sessions)
    validation={'profile_id':196407,'verified_games':len(games),'download_attempts':len(downloads),
        'unavailable_downloads':sum('file' not in r for r in downloads),'parse_failures':failures,'short_abort_exclusions':len(exclusions),
        'all_verified_headers_match_profile_and_logged_start':True,'all_verified_body_clocks_checked':True,
        'complete_recordings':sum(r['postgame_present'] for r in games),'trait_fields':len(fields),
        'trait_windows':len(traits),'phase_windows':len(windows),
        'long_games':len({r['game_id'] for r in longs}),
        'eligible_primary_complete_sessions':sum(r['gap_threshold_minutes']==30 and r['sample_covers_all_logged_games'] and not r['left_log_boundary_censored'] for r in sessions),
        'historical_replays_obtained':False,'age_effect_identified':False,
        'raw_replays_may_contain_public_match_chat':True,'derived_command_export_excludes_chat_and_viewlocks':True}
    (OUT/'validation.json').write_text(json.dumps(validation,indent=2)+'\n');print(json.dumps(validation,indent=2),flush=True)
    assert not failures,'Inspect failures before publishing'

if __name__=='__main__':main()
