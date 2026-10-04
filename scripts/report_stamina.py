"""Write the command-trajectory report and export scientific plots."""
from pathlib import Path
import collections, csv, json, math, statistics as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'stamina'
def read(name):
    with (OUT/name).open() as f:return list(csv.DictReader(f))
def number(x):
    try:return float(x)
    except (ValueError,TypeError):return None
def fmt(x,scale=1,precision=3):
    value=number(x);return 'unavailable' if value is None else f'{value*scale:.{precision}f}'
def table(headers,rows):
    return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(map(str,r))+' |\n' for r in rows)
def wm(rows,field):
    valid=[r for r in rows if number(r.get(field)) is not None]
    counts=collections.Counter(r['cluster'] for r in valid)
    pairs=sorted((number(r[field]),1/counts[r['cluster']]) for r in valid)
    if not pairs:return None
    half=sum(w for _,w in pairs)/2;total=0
    for i,(v,w) in enumerate(pairs):
        total+=w
        if total>=half-1e-12:
            return (v+pairs[i+1][0])/2 if math.isclose(total,half,abs_tol=1e-12) and i+1<len(pairs) else v

cohort=read('cohort_inventory.csv');period=read('long_game_period_summary.csv');pairs=read('long_game_paired_changes.csv');windows=read('window_metrics.csv');sessions=read('session_summary.csv');firstlast=read('session_first_last_and_slopes.csv')
def val(player,year,context,window,metric):
    return next((r for r in period if (r['player'],r['year'],r['context'],r['late_window'],r['metric'])==(player,str(year),context,window,metric)),None)

text='''# Long-game and observed-session command trajectories

This extension tests within-game command timing and recent observed-session patterns using the existing 98 verified player-game observations. It does not measure cognitive reserve, normalize independent game-state demand, or establish an aging effect. Whole-game command volume is an inadequate stamina outcome because phase composition and duration differ.

## Design and definitions

- Long-game cohort: recordings with at least 45 available game minutes. The same qualifying games contribute 0–10, 10–20, 20–30, 30–40 and fixed 40–45-minute measurements. This avoids comparing late-game survivors with openings from all short and long games, but selection on reaching 45 minutes remains a confound.
- Opening baseline: each qualifying game's own first ten game minutes. Ratios/differences are computed per game before period aggregation. Each series/session-day receives equal total weight; games share that weight. Game medians and ranges are preserved in CSV.
- Clock: intervals are game-clock minutes. Command rates, ten-second burst bins and five-second gap thresholds use nominal seconds (game seconds divided by recorded speed), matching previous analyses. This is not observed human wall-clock reaction time.
- Burst: p95 of core-command rates in complete, aligned ten-nominal-second bins. Maximum ten-second rate is also reported. Core commands are MOVE, ORDER, BUILD, RESEARCH, DELETE, BUY, SELL and WALL; these rates are not device-input APM. Opening and fixed late intervals differ in length (ten versus five game minutes); p95 reduces, but does not remove, sample-size effects. Maximum bursts are particularly exposure-sensitive.
- Gap probability: number of adjacent within-window core-command gaps strictly greater than five nominal seconds divided by all adjacent gaps, including zero gaps. Boundary gaps are excluded because they are censored. This is distinct from the fraction of window time spent in long command silences, which is stored separately and includes edge intervals.
- Sensitivities: requested 40+ available interval, fixed 40–45 interval, maximum versus p95 bursts, and 40+ with the final available recording minute omitted. A partial recording's endpoint is not a known match endpoint.
- Research anchors: fixed five-minute intervals after Feudal/Castle/Imperial RESEARCH requests, plus the following five-minute interval where available. Requests are not completed age-ups; these are neither validated combat phases nor guaranteed equivalent game states.
- Command footprint: explicit commanded actor IDs, commanded production-building IDs, queue requests and command diversity are recorded as input-side descriptors. They depend on command choices and coverage; they are not independent workload measurements or useful state output. Approximate repeated destination/target pairs are not automatically wasted commands.

## Available long games

'''
coverage=[]
for player,year,context in sorted({(r['player'],r['year'],r['context']) for r in cohort}):
    rows=[r for r in cohort if (r['player'],r['year'],r['context'])==(player,year,context)];long=[r for r in rows if r['qualifies_45plus']=='True']
    coverage.append([player,year,context,len(rows),len(long),len({r['cluster'] for r in long}),sum(r['partial']=='True' for r in long)])
text+=table(['Player','Year','Context','All games','45+ games','Long-game clusters','Partial long recordings'],coverage)
text+='''
The 2011 DauT sample has no 45+ recording. Classic 2012 team games are retained as a separate appendix-level comparison; ownership/encoding, team demands and timing resolution prevent a clean comparison with recent DE 1v1 games. TaToH's 2021 recording covers the fixed 40–45 interval, but its variable 40+ result ends at the partial recording cutoff.

## Fixed 40–45 versus the same game's 0–10 baseline

Ratios below are medians of per-game ratios, with equal cluster weights. A ratio below 1 means lower late-window command throughput/burst size. The gap column is an absolute difference in percentage points: positive means more late-window gaps over five seconds. Neither direction alone identifies fatigue, because workload and strategy remain unmeasured.

'''
display=[]
for player,year,context in sorted({(r['player'],r['year'],r['context']) for r in period if r['year'] in ['2021','2026']}):
    sample=val(player,year,context,'40-45','core_cpm_late_over_open')
    display.append([player,year,context,f"{sample['n']} / {sample['clusters']}",fmt(sample['weighted_median']),fmt(val(player,year,context,'40-45','burst_p95_late_over_open')['weighted_median']),fmt(val(player,year,context,'40-45','peak_10s_late_over_open')['weighted_median']),fmt(val(player,year,context,'40-45','p_core_gap_gt5s_late_minus_open')['weighted_median'],100,2)])
text+=table(['Player','Year','Context','Games / clusters','Core-rate ratio','p95 burst ratio','Maximum burst ratio','Long-gap Δ pp'],display)
text+='\n![Fixed-phase trajectories](long_game_trajectories.png)\n\n'
text+='''The plots retain the identical long-game cohort throughout. Rates are normalized to each game's own opening; gap probability is shown directly. Lines are descriptive medians, not fatigue-adjusted performance or confidence intervals.

## Requested 40+ interval and endpoint sensitivity

'''
display=[]
for player,year,context in sorted({(r['player'],r['year'],r['context']) for r in period if r['year'] in ['2021','2026']}):
    for late in ['40+','40+ excluding final 60 game seconds']:
        sample=val(player,year,context,late,'burst_p95_late_over_open')
        display.append([player,year,context,late,fmt(sample['weighted_median']),fmt(val(player,year,context,late,'peak_10s_late_over_open')['weighted_median']),fmt(val(player,year,context,late,'p_core_gap_gt5s_late_minus_open')['weighted_median'],100,2)])
text+=table(['Player','Year','Context','Late interval','p95 burst ratio','Maximum burst ratio','Long-gap Δ pp'],display)
text+='''
## Research-request-aligned windows

The following comparisons hold the relative interval at the first five game minutes after an age-up research request. Completed age-up times and combat status are unknown, and start-age/maps/settings can differ. These are operational anchors, not verified Feudal combat, early Castle or Imperial state equivalence. The full `request_anchor_period_summary.csv` also contains the following five-minute windows, bursts, long-gap probabilities and approximate deduplicated rates.

'''
anchors=read('request_anchor_period_summary.csv');anchor_display=[]
for r in anchors:
    if r['metric']=='core_cpm' and '+0-5 min' in r['window']:
        anchor_display.append([r['player'],r['year'],r['context'],r['window'],r['n'],r['clusters'],fmt(r['weighted_median'],1,1)])
text+=table(['Player','Year','Context','Request-relative interval','Games','Clusters','Core commands / nominal min'],anchor_display)
text+='''
## Observed-session analysis

TaToH's cached account log supplies starts/finishes for ranked and unranked matches, including matches whose replays were not parsed. Modes are combined when defining observed sessions, then command comparisons stay within a context. For DauT and TheViper only sampled replay timestamps are available, so omitted intervening games cannot be ruled out. A session starts after more than 30 logged inactive minutes; 15 and 60 minutes are sensitivity definitions. Elapsed time starts at the first logged match in the observed run, not a verified beginning of the player's day or practice session.

Every measured session outcome uses the same first ten game minutes. Sessions need at least three available complete openings for first/last comparisons and descriptive linear slopes. This removes the opening-versus-late-game duration mix from this session outcome, but maps, civilizations, opponents, openings, losses and selection still differ. The first measured opening can follow an unparsed or short game. Ordinals include logged games without metrics. `session_first_last_and_slopes.csv` records the actual endpoint ordinals, elapsed hours, slopes, and first-to-sixth-relative-observed-game contrasts when available.

'''
display=[]
for player,context in sorted({(r['player'],r['context']) for r in sessions}):
    def s(metric):return next(r for r in sessions if (r['player'],r['context'],r['gap_threshold_minutes'],r['metric'])==(player,context,'30',metric))
    rate=s('core_cpm_last_over_first');burst=s('burst_p95_10s_core_cpm_last_over_first');gap=s('p_core_gap_gt5s_last_minus_first');slope=s('core_cpm_slope_per_hour')
    display.append([player,context,rate['sessions'],fmt(rate['median']),f"{rate['negative_sessions']}/{rate['sessions']}",fmt(burst['median']),fmt(gap['median'],100,2),fmt(slope['median'],1,2)])
text+=table(['Player','Context','Eligible sessions','Last/first opening core rate','Sessions with lower final core rate','Last/first opening p95 burst','Long-gap Δ pp','Median core-rate slope per hour'],display)
text+='\n![Observed-session opening changes](session_opening_changes.png)\n\n'
text+='''The slope is a descriptive within-session association with elapsed hours, without independent demand adjustment. The colored lines connect available openings and do not imply that every intervening logged game has measurements. First/last comparisons and session-break sensitivities are reported together; none is selected as a confirmatory aging test.

## Session-break sensitivity

'''
display=[]
for r in sessions:
    if r['metric']=='core_cpm_last_over_first':display.append([r['player'],r['context'],r['gap_threshold_minutes'],r['sessions'],fmt(r['median']),fmt(r['min']),fmt(r['max'])])
text+=table(['Player','Context','Break threshold min','Sessions','Median final/first core rate','Min','Max'],display)
text+='''
## Exploratory synchronization-counter demand proxy

The DE replay body contains per-player synchronization counters. The installed `mgz==1.8.51` parser labels one `obj_count`, but explicitly warns that the field meanings are guesses. This audit extracts that field in the 19 qualifying DE player-game observations, checks the source hashes and synchronization clocks, and calculates a time-weighted counter average. Counters are not carried over gaps longer than 30 game seconds. A normalized input-rate result requires at least 95% counter-time coverage in both intervals.

The exploratory quantity is core-command rate per 100 units of the recorded counter. It is **not useful state change per command**, a validated living-unit count, or independent required workload. It can include buildings/foundations and objects that remain after a unit dies; its relation to visible threats or active control demand is not established. The parser also omits player payloads when a presumed resource field is zero. The recent Viper long game fails the 95% coverage requirement, so its normalized contrast is withheld. Dividing by a growing counter can mechanically produce a large decrease even if control remains effective; group orders do not require one command per object.

'''
audit=read('sync_counter_period_audit.csv');audit_display=[]
for player,year,context in sorted({(r['player'],r['year'],r['context']) for r in audit}):
    def av(field):return next(r for r in audit if(r['player'],r['year'],r['context'],r['metric'])==(player,year,context,field))
    growth=av('obj_counter_late_over_open');normalized=av('counter_normalized_core_late_over_open')
    audit_display.append([player,year,context,growth['n'],fmt(growth['weighted_median'],1,2),fmt(normalized['weighted_median']),normalized['n']])
text+=table(['Player','Year','Context','Long games','Counter growth 40–45 / 0–10','Counter-normalized input-rate ratio','Coverage-qualified contrasts'],audit_display)
text+='''
This audit demonstrates that a demand-proxy calculation is technically possible, but the semantics and coverage prevent treating it as control efficiency. No validated output or cognitive-capacity result follows. See `sync_counter_validation.json` and the [upstream synchronization-parser contribution](https://github.com/happyleavesaoc/aoc-mgz/pull/123). The parser's explicit caveats are preserved as source provenance.

## What the three-effect model can and cannot identify

The dataset can describe command outcome = f(recording period, game-clock interval), and recent command outcome = f(elapsed observed-session hours) while holding the outcome interval at 0–10 minutes. Per-game pairing and session-based summaries reduce some mixture effects. A full age × in-game time × session-time model is not identified here: historical session timestamps are missing, older recent-period long-game samples are tiny, and within each player age is tied to recording year and all the patch/practice/context changes accompanying it. Numeric age coefficients would overstate what this archive can support.

Useful game-state change per command requires validated economic/unit trajectories and a defined useful outcome, with visibility and opposing threats where relevant. Army size, active fronts, production capacity, idle time, resource stock, combat opportunities and threat intensity are not decoded for these historic/recent comparisons. Equal clock windows and request anchors are partial controls, not demand normalization. Late-window deterioration would be a candidate pattern to investigate; absence of deterioration would not show that cognitive reserve is preserved.

No population p-values or causal aging estimates are reported. Counts, per-game results, cluster weighting and session sensitivities are available for inspection. The provisional 2019 attribution is excluded.

## Files and reproduction

- `window_metrics.csv`: all complete clock windows and request anchors with counts, gap denominators, bursts, rates and command-footprint descriptors.
- `cohort_inventory.csv`: inclusion, duration, partial status, hashes and unavailable state measures.
- `long_game_paired_changes.csv`, `long_game_period_summary.csv`, `long_game_phase_summary.csv`: paired changes and long-game summaries.
- `session_opening_metrics.csv`, `observed_session_inventory.csv`, `session_first_last_and_slopes.csv`, `session_summary.csv`: recent observed-session metrics and sensitivities.
- `source_validation.json`, `validation.json`: source hashes, body-clock checks, identity checks, opening agreement and scope.

Restore the original release inputs as described in the root README, then run:

```sh
.venv/bin/python scripts/stamina_analysis.py
.venv/bin/python scripts/sync_proxy_audit.py
.venv/bin/python scripts/report_stamina.py
```
'''

# Graph identical long-game cohort, with per-game normalization before aggregation.
labels=['0-10','10-20','20-30','30-40','40-45']
fig,axes=plt.subplots(2,3,figsize=(15,8),sharex=True)
colors={'2021':'#3465a4','2026':'#a23c67'}
openings={(r['game_id'],r['player']):number(r['core_cpm']) for r in windows if r['window']=='0-10'}
for j,player in enumerate(['DauT','TheViper','TaToH']):
    for year,context in sorted({(r['year'],r['context']) for r in windows if r['player']==player and r['year'] in ['2021','2026'] and r['long_game_45plus']=='True'}):
        ys=[];gs=[]
        for label in labels:
            rows=[dict(r,normalized=100*number(r['core_cpm'])/openings[r['game_id'],r['player']]) for r in windows if (r['player'],r['year'],r['context'],r['window'],r['long_game_45plus'])==(player,year,context,label,'True')]
            ys.append(wm(rows,'normalized'));gs.append(100*wm(rows,'p_core_gap_gt5s'))
        n=len({r['game_id'] for r in windows if r['player']==player and r['year']==year and r['context']==context and r['long_game_45plus']=='True'})
        label=f'{year} {context}, n={n}';style='--' if context=='ranked' else '-'
        axes[0,j].plot(labels,ys,marker='o',color=colors[year],linestyle=style,label=label)
        axes[1,j].plot(labels,gs,marker='o',color=colors[year],linestyle=style)
    axes[0,j].set_title(player);axes[0,j].axhline(100,color='gray',linewidth=.7,linestyle=':');axes[0,j].legend(fontsize=8)
    for ax in axes[:,j]:ax.grid(alpha=.2)
    axes[1,j].set_xlabel('Game-clock interval (minutes)')
axes[0,0].set_ylabel('Core command rate (% of own opening)');axes[1,0].set_ylabel('Adjacent core gaps >5 nominal s (%)')
fig.suptitle('Long recordings only: descriptive command trajectories\n2026 DauT/Viper each have one qualifying long game; TaToH 2021 is one partial recording',fontsize=12)
fig.tight_layout();fig.savefig(OUT/'long_game_trajectories.png',dpi=170);fig.savefig(OUT/'long_game_trajectories.svg');plt.close(fig)

opening_sessions=read('session_opening_metrics.csv');eligible={(r['session_id'],r['context']) for r in firstlast if r['gap_threshold_minutes']=='30'}
fig,axes=plt.subplots(1,3,figsize=(15,4.8))
for ax,player in zip(axes,['DauT','TheViper','TaToH']):
    groups=collections.defaultdict(list)
    for r in opening_sessions:
        if r['player']==player and (r['session_id'],r['context']) in eligible:groups[(r['session_id'],r['context'])].append(r)
    for (sid,context),rs in sorted(groups.items()):
        rs.sort(key=lambda r:number(r['session_elapsed_hours']));base=number(rs[0]['core_cpm'])
        ax.plot([number(r['session_elapsed_hours']) for r in rs],[number(r['core_cpm'])/base*100 for r in rs],marker='o',linewidth=1,alpha=.75,label=sid.split('_')[-1][:10]+' '+context)
    ax.set_title(player+f' ({len(groups)} observed sessions)');ax.axhline(100,color='gray',linestyle=':',linewidth=.7);ax.set_xlabel('Hours since first logged/sampled game');ax.grid(alpha=.2)
    if len(groups)<=3:ax.legend(fontsize=8)
axes[0].set_ylabel('Opening core rate (% of first measured opening)')
fig.suptitle('Recent 2026 observed-session patterns: opening outcomes only; not an age comparison',fontsize=12);fig.tight_layout();fig.savefig(OUT/'session_opening_changes.png',dpi=170);fig.savefig(OUT/'session_opening_changes.svg');plt.close(fig)
(OUT/'REPORT.md').write_text(text)
print(json.dumps({'report':str(OUT/'REPORT.md'),'plots':2,'report_bytes':len(text)},indent=2))
