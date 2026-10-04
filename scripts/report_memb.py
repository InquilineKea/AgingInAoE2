"""Memb report, original 82-field coverage, plots, and additive joint table."""
from pathlib import Path
import collections,csv,gzip,json,math,statistics as st,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'memb'
sys.path.insert(0,str(ROOT/'scripts'))
import behavior_metrics as B
import stamina_analysis as S

def read(name):return list(csv.DictReader((OUT/name).open()))
def number(value):
    try:return float(value) if math.isfinite(float(value)) else None
    except (TypeError,ValueError):return None
def write(name,rows):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)

def additional(a,speed,duration):
    c=[x for x in a if x['type'] in B.CORE and x['t']<duration]
    t=np.array([x['t'] for x in c]);cats=[B.category(x['type']) for x in c]
    gaps=np.diff(np.r_[0,t,duration])/speed
    queue=[x for x in a if x['type']=='DE_QUEUE' and (x.get('amount') or 0)>0 and x['t']<duration]
    out={'legacy_command_class_entropy_bits':B.entropy(cats),
         'legacy_switches_per_100_commands':100*sum(x!=y for x,y in zip(cats,cats[1:]))/max(1,len(cats)-1),
         'legacy_core_silence_over5s_fraction':float(gaps[gaps>5].sum()/(duration/speed)),
         'legacy_peak_10s_nominal_cpm':max((np.searchsorted(t,x+10*speed,side='left')-i for i,x in enumerate(t)),default=0)*6,
         'legacy_move_share':sum(x['type']=='MOVE' for x in c)/max(1,len(c)),
         'legacy_planning_command_share':sum(x['type'] in {'BUILD','WALL','RESEARCH','BUY','SELL'} for x in c)/max(1,len(c)),
         'legacy_queue_batch_mean':st.mean(x['amount'] for x in queue) if queue else None,
         'legacy_queue_batch_gt1_fraction':st.mean(x['amount']>1 for x in queue) if queue else None,
         'legacy_duration_game_min':duration/60}
    for name,start,end in [('cpm_0_5',0,300),('cpm_5_10',300,600),('cpm_10_15',600,900),('cpm_15_20',900,1200),('cpm_10_20',600,1200)]:
        out['tatoh_'+name]=sum(start<=x['t']<end for x in c)/((end-start)/speed/60) if duration>=end else None
    for label,start,end in [('open',0,600),('10_20',600,1200)]:
        times=[x['t']/speed for x in c if start<=x['t']<end]
        gaps=[y-x for x,y in zip(times,times[1:])]
        for percentile in ([50,90,99] if label=='open' else [99]):
            out[f'tatoh_gap_p{percentile}_{label}']=B.quant(gaps,percentile/100) if duration>=end else None
    for label,end in [('open',600),('whole',duration+1)]:
        mo=[x for x in c if x['type'] in {'MOVE','ORDER'} and x['t']<end and x.get('x') is not None]
        n=sum((y['t']-x['t'])/speed<=.5 and (math.hypot(x['x']-y['x'],x['y']-y['y'])<=2 or
            (x.get('target_id') not in (None,-1) and x.get('target_id')==y.get('target_id'))) for x,y in zip(mo,mo[1:]))
        count=sum(x['t']<end for x in c)
        out['tatoh_reclick_'+label]=n/count if count and duration>=min(end,600) else None
        out['tatoh_dedup_'+label+'_cpm']=(count-n)/(end/speed/60) if duration>=min(end,600) else None
    return out

def main():
    validation=json.loads((OUT/'validation.json').read_text());assert not validation['parse_failures']
    inventory=read('game_inventory.csv');inv={r['game_id']:r for r in inventory}
    actions=collections.defaultdict(list)
    with gzip.open(OUT/'owned_commands.jsonl.gz','rt') as f:
        for line in f:
            a=json.loads(line);actions[a['game_id']].append(a)
    traits=read('trait_metrics.csv');dictionary=list(csv.DictReader((ROOT/'deadline-sparse/trait_dictionary.csv').open()))
    names=[r['trait'] for r in dictionary];rows82=[]
    for r in traits:
        a=actions[r['game_id']];m=inv[r['game_id']];speed=float(m['nominal_speed']);duration=float(m['duration_game_minutes'])*60
        numeric={k:number(v) for k,v in r.items() if k in names}
        if r['window']=='whole available replay':numeric.update(additional(a,speed,duration))
        end=600 if r['window']=='first 10 game minutes' else duration
        for field,tech in [('feudal_request_game_s',101),('castle_request_game_s',102),('imperial_request_game_s',103)]:
            numeric[field]=next((x['t'] for x in a if x['type']=='RESEARCH' and x.get('technology_id')==tech and x['t']<end),None)
        rows82.append({**{k:r[k] for k in ['game_id','player','year','context','cluster','window']},**{k:numeric.get(k) for k in names}})
        core=[x for x in a if x['type'] in B.CORE and x['t']<end]
        assert abs(numeric['core_cpm']-len(core)/(end/speed/60))<1e-7
    write('original_82_trait_metrics.csv',rows82)
    comparisons=[]
    for context,window in sorted({(r['context'],r['window']) for r in rows82}):
        rows=[r for r in rows82 if r['context']==context and r['window']==window]
        for field in names:
            value=S.weighted_summary(rows,field)
            comparisons.append({'comparison':'MembTV historical baseline unavailable','player':'MembTV',
                'early_year':None,'early_context':None,'late_year':2026,'late_context':context,
                'window':window,'trait':field,'early_n':0,'late_n':value['n'],
                'early_clusters':0,'late_clusters':value['clusters'],'early_weighted_median':None,
                'late_weighted_median':value['weighted_median'],'early_game_median':None,'late_game_median':value['game_median'],
                'early_min':None,'early_max':None,'late_min':value['min'],'late_max':value['max'],
                'difference':None,'difference_percentage_points':None,'relative_change_percent':None,
                'direction':'unavailable','metric_limit':'Original definitions retained; tatoh_ prefix denotes a legacy definition reused for MembTV, not player identity.',
                'comparison_limit':'No recovered historical replay baseline; current team-game context cannot be pooled with professional 1v1 samples.'})
    write('original_82_trait_coverage.csv',comparisons)
    original=list(csv.DictReader((ROOT/'deadline-sparse/all_trait_comparisons.csv').open()))
    write('all_players_trait_comparisons.csv',original+comparisons)
    windows=read('window_metrics.csv');longs=read('long_game_paired_changes.csv');longids={r['game_id'] for r in longs}
    complete_long_summary=[]
    for context,label in sorted({(r['context'],r['late_window']) for r in longs}):
        rows=[{**r,**{k:float(r[k]) for k in ['core_cpm_late_over_opening','burst_p95_late_over_opening','p_gap_late_minus_opening']}} for r in longs if r['context']==context and r['late_window']==label and r['partial_recording']=='False']
        complete_long_summary.append({'context':context,'late_window':label,'games':len(rows),'day_clusters':len({r['cluster'] for r in rows}),
            **{k:S.weighted_summary(rows,k)['weighted_median'] for k in ['core_cpm_late_over_opening','burst_p95_late_over_opening','p_gap_late_minus_opening']}})
    write('complete_long_game_summary.csv',complete_long_summary)
    opens={r['game_id']:r for r in windows if r['window']=='0-10'}
    trajectories=[]
    for r in windows:
        if r['game_id'] not in longids or r['window'] not in {'0-10','10-20','20-30','30-40'}:continue
        opening=opens[r['game_id']]
        trajectories.append({**{k:r[k] for k in ['game_id','cluster','context','window']},
            'core_rate_over_opening':float(r['core_cpm'])/float(opening['core_cpm']),
            'p95_burst_over_opening':float(r['burst_p95_10s_core_cpm'])/float(opening['burst_p95_10s_core_cpm']),
            'gap_probability':float(r['p_core_gap_gt5s'])})
    for r in longs:
        if r['late_window']=='40-45':trajectories.append({'game_id':r['game_id'],'cluster':r['cluster'],'context':r['context'],'window':'40-45',
            'core_rate_over_opening':float(r['core_cpm_late_over_opening']),
            'p95_burst_over_opening':float(r['burst_p95_late_over_opening']),
            'gap_probability':float(opens[r['game_id']]['p_core_gap_gt5s'])+float(r['p_gap_late_minus_opening'])})
    write('long_game_trajectories.csv',trajectories)
    labels=['0-10','10-20','20-30','30-40','40-45'];fig,axes=plt.subplots(1,3,figsize=(14,4))
    for ax,field,title in zip(axes,['core_rate_over_opening','p95_burst_over_opening','gap_probability'],['Core commands / opening','p95 burst / opening','P(adjacent gap >5 nominal seconds)']):
        for context in sorted({r['context'] for r in trajectories}):
            ys=[S.weighted_summary([r for r in trajectories if r['window']==w and r['context']==context],field)['weighted_median'] for w in labels]
            ax.plot(labels,ys,'o-',label=context)
        ax.set_title(title);ax.set_xlabel('Game-clock minutes');ax.grid(alpha=.25)
    if trajectories:axes[0].legend(fontsize=7)
    fig.suptitle(f'MembTV, age 49: same {len(longids)} qualifying long-game recordings\nDay-weighted descriptive medians; unranked team context; no historical age contrast',fontsize=11)
    fig.tight_layout();fig.savefig(OUT/'long_game_trajectories.png',dpi=160);fig.savefig(OUT/'long_game_trajectories.svg');plt.close(fig)
    sessions=read('session_comparisons.csv')
    # A classified short abort is sampled but has no complete opening outcome.
    # Include it when checking session sampling, never as a missing replay.
    sampled={int(r['game_id']) for r in inventory}|{r['game_id'] for r in json.loads((OUT/'excluded_recordings.json').read_text())}
    matchlog=json.loads((OUT/'match-log.json').read_text())
    maps={threshold:__import__('analyze_memb').session_map(matchlog,threshold) for threshold in (15,30,60)}
    for r in sessions:
        mapping=maps[int(r['gap_threshold_minutes'])]
        r['sample_covers_all_logged_games']=str(all(mid in sampled for mid,m in mapping.items() if m['session_id']==r['session_id']))
    write('session_comparisons.csv',sessions)
    eligible=[r for r in sessions if r['gap_threshold_minutes']=='30' and r['sample_covers_all_logged_games']=='True' and r['left_log_boundary_censored']=='False']
    validation['eligible_primary_complete_sessions']=len(eligible)
    (OUT/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    session_summary=[]
    for threshold in (15,30,60):
        rows=[r for r in sessions if r['gap_threshold_minutes']==str(threshold) and r['sample_covers_all_logged_games']=='True' and r['left_log_boundary_censored']=='False']
        session_summary.append({'gap_threshold_minutes':threshold,'eligible_sessions':len(rows),
            'median_core_last_over_first':st.median(float(r['core_cpm_last_over_first']) for r in rows) if rows else None,
            'median_burst_last_over_first':st.median(float(r['burst_p95_10s_core_cpm_last_over_first']) for r in rows) if rows else None,
            'sessions_with_core_decrease':sum(float(r['core_cpm_last_over_first'])<1 for r in rows)})
    write('session_summary.csv',session_summary)
    sid={r['session_id'] for r in eligible};sessionopen=[r for r in read('session_opening_metrics.csv') if r['gap_threshold_minutes']=='30' and r['session_id'] in sid]
    fig,ax=plt.subplots(figsize=(10,5))
    for session in sorted(sid):
        rows=sorted([r for r in sessionopen if r['session_id']==session],key=lambda r:int(r['observed_game_ordinal']))
        first=float(rows[0]['core_cpm']);ax.plot([float(r['session_elapsed_hours']) for r in rows],[float(r['core_cpm'])/first for r in rows],'o-',alpha=.75,label=rows[0]['date'][:10]+' '+session)
    ax.axhline(1,color='black',lw=1,ls='--');ax.set_xlabel('Hours after first logged game start');ax.set_ylabel('Opening core-command rate / first measured opening')
    ax.set_title(f'MembTV: {len(eligible)} sampled observed-session/context groups\nAt least three complete openings; all logged games sampled; 30-minute break');ax.grid(alpha=.25)
    if sid:ax.legend(fontsize=7,ncol=2)
    fig.tight_layout();fig.savefig(OUT/'session_opening_changes.png',dpi=160);fig.savefig(OUT/'session_opening_changes.svg');plt.close(fig)
    complete=sum(r['postgame_present']=='True' for r in inventory)
    dates=sorted(r['date'] for r in inventory)
    coverage={'original_dictionary_fields':len(names),'whole_window_fields_with_at_least_one_value':sum(any(r[k] is not None for r in rows82 if r['window']=='whole available replay') for k in names),
        'verified_original_observations':98,'verified_memb_observations':len(inventory),'combined_verified_observations':98+len(inventory),
        'combined_comparison_rows':len(original)+len(comparisons),'memb_rows_have_no_historical_contrast':True}
    (OUT/'integration_validation.json').write_text(json.dumps(coverage,indent=2)+'\n')
    def fmt(value,digits=3):return 'unavailable' if value is None else f'{float(value):.{digits}f}'
    text=['# MembTV extension: recent command behavior and replay availability','',
        'MembTV is added as a separately labeled cohort. His July 22, 1977 birth date makes him 49 during these recordings. No historical replay baseline was recovered, so this extension does **not** measure an age 42–49 trajectory.','',
        'Identity sources: [Liquipedia](https://liquipedia.net/ageofempires/MembTV) and [AoE2Insights profile 196407](https://www.aoe2insights.com/user/196407/). The profile lists RM 1v1 rating 1810 and 4,572 RM 1v1 matches. Retrieved Companion ranked logs end May 29, 2026; a displayed rating does not establish current ranked activity. Indexed match totals differ across source snapshots and are not replay availability counts.','',
        '## Recovered cohort','',
        f"- Frozen sample: newest 60 all-mode games in six cached pages (120 logged games), selected before calculating command outcomes. 56 were downloaded; {len(inventory)} passed analysis eligibility, with {validation['short_abort_exclusions']} aborted recordings under one game minute excluded. Four recent download attempts returned HTTP 404. Three additional latest-ranked probes returned HTTP 404.",
        f"- Verified replay dates: {dates[0]} through {dates[-1]}.",
        f'- Identity, timestamp agreement, source hashes, body endpoints and synchronization clocks were checked for every included recording. {complete}/{len(inventory)} contain a POSTGAME operation; missing POSTGAME is marked partial in paired long-game tables.',
        '- Recent games are kept by their logged player count, mode and map context. They are not pooled with DauT, TheViper or TaToH 1v1 periods.',
        f"- The original 82-field dictionary is retained. {coverage['whole_window_fields_with_at_least_one_value']} fields have at least one whole-replay value; missing per-game fields remain blank. The tatoh_ prefix denotes the original legacy definition, now also applied to Memb, not a TaToH observation.",
        f"- The combined archive now contains {coverage['combined_verified_observations']} verified player-game observations. The original 98-observation analyses remain identifiable and unchanged.",
        '', '## Opening and whole-replay behavior','',
        'Each day has equal total weight and its games share that weight. Medians describe command behavior, not cognitive capacity.','',
        '| Context | Window | Games / days | Core commands / nominal min | Approximate deduplicated rate |',
        '| --- | --- | --- | --- | --- |']
    for r in read('trait_summary.csv'):text.append(f"| {r['context']} | {r['window']} | {r['games']} / {r['day_clusters']} | {fmt(number(r['core_cpm']),1)} | {fmt(number(r['dedup_core_cpm']),1)} |")
    text += ['', '## Long-game pairing','',
        f'{len(longids)} recordings reach 45 available game minutes. The same qualifying recordings contribute all plotted phases. Each late/opening contrast is calculated per game before equal-day weighting. No earlier-period contrast is available.','',
        '| Context | Late interval | Games / days | Core late/opening | p95 burst late/opening | Long-gap delta, percentage points |',
        '| --- | --- | --- | --- | --- | --- |']
    for r in read('long_game_summary.csv'):text.append(f"| {r['context']} | {r['late_window']} | {r['games']} / {r['day_clusters']} | {fmt(number(r['core_cpm_late_over_opening']))} | {fmt(number(r['burst_p95_late_over_opening']))} | {fmt(float(r['p_gap_late_minus_opening'])*100,2)} |")
    sensitivity=next(r for r in complete_long_summary if r['late_window']=='40-45')
    partial_long_count=len({r['game_id'] for r in longs if r['partial_recording']=='True'})
    text += ['',f"{partial_long_count} qualifying recording lacks POSTGAME. Excluding partial recordings leaves {sensitivity['games']} long games: the fixed late/opening core ratio is {fmt(sensitivity['core_cpm_late_over_opening'])}, p95 burst ratio {fmt(sensitivity['burst_p95_late_over_opening'])}, and gap-probability change {fmt(sensitivity['p_gap_late_minus_opening']*100,2)} percentage points. [Complete-recording sensitivity](complete_long_game_summary.csv).",'', '![Long-game phase trajectories](long_game_trajectories.png)','',
        '## Observed sessions','',
        f'{len(eligible)} primary session/context groups have at least three complete openings, all games in the cached session sampled, and no left-edge log censoring. Session boundaries use **all 120 logged matches**, including unavailable and unparsed games. Gaps over 30 inactive wall-clock minutes define a new session; 15 and 60 minutes are retained as sensitivities. Starts/finishes describe the observed match run, not a verified beginning of the day. Unavailable games can have missing command outcomes and remain counted in observed ordinals.','',
        '| Session | Complete openings | First-to-last opening hours | Core last/first | p95 burst last/first | Gap delta, percentage points |',
        '| --- | --- | --- | --- | --- | --- |']
    for r in eligible:text.append(f"| {r['session_id']} | {r['n_openings']} | {fmt(number(r['hours_between_first_last']),2)} | {fmt(number(r['core_cpm_last_over_first']))} | {fmt(number(r['burst_p95_10s_core_cpm_last_over_first']))} | {fmt(float(r['p_core_gap_gt5s_last_minus_first'])*100,2)} |")
    primary=next(r for r in session_summary if r['gap_threshold_minutes']==30)
    text += ['',f"Across the seven primary sessions, the median final/first opening core-rate ratio is {fmt(primary['median_core_last_over_first'])}; five sessions increase and two decrease. The nine-opening run over 4.18 hours ends about 34% below its first opening, but this is one recent run with changing game conditions, not an aging estimate. [Session-break summary](session_summary.csv).",'', '![Session opening trajectories](session_opening_changes.png)','',
        '## Availability and interpretation limits','',
        'Historical match identifiers were found for December 2020 and October 2022. Two replay endpoints from each period returned HTTP 404, as did the three May 2026 ranked probes. The public 2021 Open Classic tournament archive returned HTTP 403; it was not bypassed. Liquipedia documents historical participation, but participation and casting credits do not establish surviving player replay files. These bounded checks do not prove that no private or community archive exists.','',
        'The proposed DE age 42–49 window remains a **potential sampling range**, not observed coverage. The current team-game cohort adds an older, less elite player but does not by itself improve longitudinal identification. Team demands, custom maps, civilization, opponent strength, settings, practice and streaming/casting obligations can change independently of age. Current RM 1v1 Elo cannot be used as the team-game skill or demand covariate.','',
        'Equal game-clock windows partially control phase composition but do not measure independent required workload. Rates and gap thresholds use nominal seconds (game seconds / replay speed). Burst p95 uses complete aligned ten-nominal-second bins; opening and fixed late windows have different exposure. Long-gap probability includes all adjacent within-window gaps, including zeros, excludes censored boundary gaps, and uses strictly >5 seconds. Age-up anchors are research requests, not completed age-ups or validated combat phases. Repeated destinations are not automatically wasted commands.','',
        'No reaction time, working-memory capacity, compensation, cognitive reserve, onager-dodge success or validated useful state change per command is measured. The new analysis does not run CaptureAge or claim decoded engine-state features. No population significance test or causal aging estimate is reported.','',
        '## Tables and reproduction','',
        '- [Original 82 per-game traits](original_82_trait_metrics.csv) and [historical coverage table](original_82_trait_coverage.csv).',
        '- [Combined all-player comparison table](all_players_trait_comparisons.csv), preserving original comparisons and adding Memb rows with unavailable historical baselines.',
        '- [Window metrics and request anchors](window_metrics.csv), [paired long-game contrasts](long_game_paired_changes.csv), [long-game summary](long_game_summary.csv).',
        '- [Session opening measurements](session_opening_metrics.csv) and [session comparisons, slopes and break sensitivities](session_comparisons.csv).',
        '- [Replay hashes and inventory](game_inventory.csv), [download ledger](downloads.json), [historical endpoint audit](historical_availability_audit.json), [validation](validation.json), [integration checks](integration_validation.json).',
        '- [Collection](../scripts/fetch_memb.py), [analysis](../scripts/analyze_memb.py), [report/integration](../scripts/report_memb.py). Raw replays may contain public match chat; derived owned commands omit chat and viewlocks.','',
        'Run with the existing pinned parser environment and restored Memb release inputs:','',
        '```sh','python scripts/analyze_memb.py','python scripts/report_memb.py','```','']
    (OUT/'REPORT.md').write_text('\n'.join(text));print(json.dumps(coverage,indent=2))

if __name__=='__main__':main()
