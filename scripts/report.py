from pathlib import Path
import json,datetime,base64,html
import pandas as pd,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'results'
df=pd.read_csv(R/'game_metrics.csv');s=pd.read_csv(R/'period_summary.csv');o=pd.read_csv(R/'opening_summary.csv');years=pd.read_csv(R/'tournament_years.csv');h=pd.read_csv(R/'tournament_history.csv');manifest=json.loads((R/'manifest.json').read_text());fail=json.loads((R/'failures.json').read_text())

raw_count=sum(1 for p in (ROOT/'raw').rglob('*') if p.suffix.lower() in ['.mgx','.mgz','.aoe2record'])
archive_count=len(list((ROOT/'raw').glob('*.zip')))
duplicate_count=sum(x['status']=='duplicate; excluded' for x in manifest)
unique_target_games=df.game_id.nunique()
player_counts=df.groupby('player').size().to_dict()

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white','axes.facecolor':'#fafafa'})
colors={'DauT':'#2d6baf','TheViper':'#b34d35'}
# Separate early team games and later 1v1 in the figure; no interpolated aging curve.
fig,axes=plt.subplots(2,2,figsize=(13,9))
for ax,metric,title in [(axes[0,0],'core_cpm_nominal','Whole-game command rate'),(axes[0,1],'gap_median_nominal_s','Median gap between core commands')]:
 for player in colors:
  z=df[(df.player==player)&(df.context!='team game')]
  for year,g in z.groupby('year'):
   offset=-0.07 if player=='DauT' else 0.07
   jitter=np.linspace(-0.08,0.08,len(g))
   x={2011:0,2021:1,2026:2}[year]
   ax.scatter(x+offset+jitter,g[metric],s=25,alpha=.5,color=colors[player])
   ax.scatter(x+offset,g[metric].median(),s=100,color=colors[player],label=player if year==2026 else None,edgecolors='white',linewidth=1,zorder=4)
 ax.set_xticks([0,1,2],['2011\nDauT challenge','2021\nHC4 tournament','2026\nranked session']);ax.set_title(title,fontweight='bold');ax.grid(axis='y',alpha=.15)
axes[0,0].set_ylabel('Core commands / nominal wall minute');axes[0,0].legend();axes[0,1].set_ylabel('Nominal wall seconds — NOT reaction time')
ax=axes[1,0]
for player in colors:
 a=s[(s.player==player)&(s.year.isin([2021,2026]))].set_index('year');b=o[(o.player==player)&(o.year.isin([2021,2026]))].set_index('year')
 x=np.array([0,1])+(-.15 if player=='DauT' else .15)
 whole=100*(a.loc[2026,'core_cpm_nominal']/a.loc[2021,'core_cpm_nominal']-1);opening=100*(b.loc[2026,'core_cpm_nominal']/b.loc[2021,'core_cpm_nominal']-1)
 ax.bar(x,[whole,opening],width=.28,color=colors[player],label=player)
 for pos,val in zip(x,[whole,opening]):ax.text(pos,val+(1 if val>=0 else -1),f'{val:+.1f}%',ha='center',va='bottom' if val>=0 else 'top',fontsize=10)
ax.axhline(0,color='#555',lw=1);ax.set_xticks([0,1],['Whole game','First 10 game minutes']);ax.set_ylim(-29,18);ax.set_ylabel('Change in period median, 2021 → 2026');ax.set_title('Direction changes with phase restriction',fontweight='bold');ax.legend()
ax=axes[1,1]
paired=pd.read_csv(R/'paired_2012_differences.csv');ax.scatter(np.arange(1,len(paired)+1),paired.core_cpm_nominal_viper_minus_daut,color='#705a9b',s=65);ax.axhline(0,color='#555',lw=1);ax.set_xlabel('Six paired games, sorted by replay hash');ax.set_ylabel('TheViper − DauT core commands / nominal minute');ax.set_title('2012: same-game comparison (team games)',fontweight='bold');ax.set_ylim(0,29)
fig.suptitle('DauT and TheViper: downloaded replay pilot\nConvenience samples; game format, map, patch and opponents change across periods',fontsize=15,fontweight='bold')
fig.text(.5,.015,'Dots = individual games; large dots = medians. Nominal wall time = game time / replay speed; excludes pauses, lag and physical input.',ha='center',fontsize=9)
fig.tight_layout(rect=(0,.035,1,.93));fig.savefig(R/'replay_comparison.png',dpi=170);fig.savefig(R/'replay_comparison.svg');plt.close(fig)
fig,axes=plt.subplots(2,1,figsize=(12,8),sharex=True)
for player in colors:
 z=years[years.player==player];axes[0].plot(z.year,z.elo_median,marker='o',label=player,color=colors[player]);axes[1].plot(z.year,100*z.series_win_fraction,marker='o',label=player,color=colors[player])
axes[0].set_title('Tournament history: descriptive competitive context',fontsize=15,fontweight='bold');axes[0].set_ylabel('Median site-defined tournament Elo');axes[0].legend();axes[1].set_ylabel('Won series / listed series (%)');axes[1].set_xlabel('Calendar year (2026 partial)');axes[1].set_ylim(0,100)
for ax in axes:ax.grid(alpha=.18)
fig.text(.5,.012,'Rating scale, field strength, series format, qualification and schedule vary; historical completeness is not established. No causal aging interpretation.',ha='center',fontsize=8.5);fig.tight_layout(rect=(0,.035,1,1));fig.savefig(R/'tournament_context.png',dpi=170);plt.close(fig)

summary=s[['player','year','context','n_games','n_clusters','core_cpm_nominal','gap_median_nominal_s','switches_per_100_commands','queue_batch_mean']].copy()
summary.columns=['Player','Year','Context','Games','Source/session clusters','Core commands / nominal minute','Median gap (nominal seconds)','Class switches / 100 commands','DE queue batch mean']
opening=o[o.year.isin([2021,2026])][['player','year','core_cpm_nominal','gap_median_nominal_s','switches_per_100_commands']]
comparison=[]
for player in ['DauT','TheViper']:
 a=s[(s.player==player)&s.year.isin([2021,2026])].set_index('year');b=o[(o.player==player)&o.year.isin([2021,2026])].set_index('year')
 comparison.append(dict(Player=player,whole_game_change_pct=100*(a.loc[2026,'core_cpm_nominal']/a.loc[2021,'core_cpm_nominal']-1),opening_change_pct=100*(b.loc[2026,'core_cpm_nominal']/b.loc[2021,'core_cpm_nominal']-1),whole_game_switch_change=a.loc[2026,'switches_per_100_commands']-a.loc[2021,'switches_per_100_commands']))
pd.DataFrame(comparison).to_csv(R/'comparison_2021_2026.csv',index=False)
counts=df.groupby(['player','year','context']).size().reset_index(name='games')
line=lambda text:text+'\n\n'
text='''# DauT and TheViper: longitudinal replay pilot

Completed locally on 2026-10-04. Actual downloads and command parsing, with explicit acquisition gaps. This is a descriptive convenience sample, not an identified estimate of cognitive aging.

## Main finding

The sampled behavior changes over time, but the direction depends on the comparison. Whole-game median core command rate rises from 2021 to 2026 for both players, while the rate in the first ten game minutes falls for both. This disagreement is evidence that game phase/composition matters; it does not establish an age-related slowdown or preserved cognition. The maps, patch, opponents and tournament-versus-ladder setting also change.

'''
text+=pd.DataFrame(comparison).round(2).to_markdown(index=False)+'\n\n'
text+='''## What was actually obtained

46 extracted replay files from 18 source ZIP archives: 31 from 2021/2026 and 15 from 2011/2012. 43 files pass decoding and ownership checks. Five of those are byte-identical duplicates despite different filenames, and one has neither target player; all six are excluded from metrics. Thus 37 distinct games contribute 44 player-game observations (25 DauT, 19 TheViper; seven games contain both). Three files are rejected by the inclusion checks: one 2012 replay has incomplete core-command ownership, and two additional 2021 HC4 replays are restored recordings with nonzero initial restore times (21:16 and 2:11 game time). The construct parser recovers their headers after the fast-header path fails. They are excluded because their partial coverage cannot support the same zero-origin opening comparison. Every raw file remains preserved. The duplicate/source issues illustrate why filenames alone cannot establish sample size.

'''
text+=counts.to_markdown(index=False)+'\n\n'
text+='''The six-game May 2012 team series contains both players, providing the strongest same-game comparison available in this pilot. Three other Viper team games and a four-versus-four recording were downloaded; one of those Viper files is rejected, and an unrelated eight-player game is excluded. Team games are presented separately, not pooled into a 1v1 aging curve. The early date labels come from archive upload dates and filenames; exact play dates are unverified. The September 2026 timestamps are read from the replay headers.

For 2021, the HC4 aliases are Gonzalo Pizarro = DauT and Ivaylo = TheViper, based on the source page's alias reveal. The HC4 profile IDs belong to tournament aliases and are not assumed to equal the current ladder profiles. September 2026 identities are checked against header profile 198035 (DauT) and 196240 (TheViper), including their actual player slots. All ten recent games are ranked RM 1v1.

The 2003–2006 DauT and 2018 samples proposed in the shared chat could not be acquired from the checked links. Some AoEZone attachment pages explicitly say the attachment cannot be shown; the recently restored 2004 pack is listed but its download is blocked/times out in this environment, so its availability remains unresolved. AoE2recs returns a browser 522 timeout. These failures do not prove that all copies are lost. The earlier chat's July 2026 exemplar returns HTTP 404 at Microsoft's replay endpoint and was replaced with September recordings. See acquisition_gaps.json for exact links and statuses. Early-period replay coverage is therefore incomplete.

## Measures and observed values

'''
text+=summary.round(3).to_markdown(index=False)+'\n\n'
text+='''Each value is a median across games, giving every game equal weight. Core commands are MOVE, ORDER, BUILD, RESEARCH, DELETE, BUY, SELL and WALL; WALL and BUILD share the construction class, BUY and SELL share the market class. Commands whose ownership is missing in a generation are excluded from every generation. Raw command count is not physical keyboard/mouse APM and is not the same definition as a website's eAPM. Repeated movement commands are retained, not interpreted as useful actions or capacity.

The replay clock is simulated game time. For the nominal wall-time columns, game timestamps are divided by the recorded speed (1.5 in these classic files, approximately 1.69 in the DE files). This estimates active wall time under the nominal speed and cannot recover lag, pauses, hardware input latency or actual frame timing. Game-time versions of the metrics are also in the CSVs. Simultaneous command timestamps are retained; positive-gap percentiles are available separately and must not be treated as a person's minimum RT.

Whole-game class-switch medians fall from 28.71 to 25.25 per 100 core commands for DauT and from 26.92 to 22.70 for TheViper. However, the first-ten-minute switch rates rise (16.88 to 19.56 for DauT; 18.42 to 21.09 for TheViper), another phase-dependent result. Command-class entropy and 4×4 spatial entropy describe the distribution of recorded commands/coordinates, not the distribution of attention. Generic ORDER commands have ambiguous economic/military purpose and are not assigned to either task.

In the six paired 2012 games, TheViper's command rate exceeds DauT's in all six. The per-game excess is 12.09–24.33 core commands per nominal minute. This establishes an older play-style difference within those shared games; it does not identify a difference in working memory or reaction time.

'''
text+='### First ten game minutes (fixed exposure window)\n\n'+opening.round(3).to_markdown(index=False)+'\n\n'
text+='''This restriction reduces whole-game duration/composition differences but does not equate build orders, visible events, map, civilization, opponent pressure or biological age effects. It is a sensitivity analysis, not a matched experiment. Five-minute trajectories are preserved in phase_metrics.csv.

## Reaction time, working memory and compensation

| Requested construct | What these recordings support | Current conclusion |
|---|---|---|
| Reaction time | Inter-command gaps, command cadence and short-window burst rate | True RT is unmeasured. A gap is not stimulus-to-response latency; the relevant visible stimulus/onset and correct response are not identified. |
| Working memory | Command-class switches, sequence entropy and spatial command dispersion | WM capacity and its change are unmeasured. These behavior proxies have no validated mapping to a memory score in this pilot. |
| Compensation | Production batching and patterns of command allocation, alongside competitive results | No demonstrated compensation mechanism. A style change cannot establish that strategy compensates for a capacity loss unless both the loss and the compensating behavior are measured under comparable demands. |

DauT's DE-only mean positive queue batch moves from approximately 1.007 to 1.040 units per command at the game-median level; TheViper's remains 1.000. This small, context-sensitive change is a candidate for follow-up, not evidence of cognitive compensation. Classic QUEUE ownership is incomplete, so queue batching is not compared to 2011/2012. No hidden task management, camera awareness, control-group use, or building idle time is claimed to have been reconstructed. No stimulus-linked RT or recall task was performed.

## Competitive history, kept separate

'''
text+=f"Downloaded and extracted {len(h[h.player=='DauT'])} dated DauT tournament-series entries (2002–2026) and {len(h[h.player=='TheViper'])} dated TheViper entries (2011–2026) from AoE Tournament Elo. Synthetic initial-estimate/current-Elo chart points are excluded. The 'victory/defeat/draw' label is used, because score ordering can be reversed when the player is on the right side. Walkovers/forfeits can occur in this archive and remain part of its listed-series data.\n\n"
text+='''The site's listed-series win fractions change from 52/79 (65.8%) in 2021 to 51/66 (77.3%) in 2026 for DauT, and from 50/58 (86.2%) to 21/34 (61.8%) for TheViper. The 2026 year is partial. These are not opponent-adjusted biological performance scores: field strength, event selection and formats vary, and archive completeness is not established. Site-defined Elo is a competitive-context metric with potential long-run scale drift, not an absolute cognitive-capacity scale. Neither the replay convenience samples nor win fractions prove decline, improvement or compensation caused by aging.

## Validation and limitations

- SHA-256 hashes and original source ZIPs are preserved. Decompressed command caches and exported timestamps contain no chat text. Fixtures used during parser development are outside the sample inventory.
- The 2021 decoder is checked against mgz.model on one game per player, requiring exact timestamp, action type and player-owner agreement for every action plus identical duration. All legacy headers are read using the official construct parser. All analyzed bodies are consumed to the physical end of file; recordings with nonzero parsed restore times or inconsistent synchronization clocks are rejected. For the partially decoded 68.9 headers, scenario restore state is unavailable; the observed independent body clocks agree with a zero-origin accumulated clock. Five accepted 2012 files contain 65 actions marked ERROR/unrecognized by the body decoder. These actions have no assigned owner and are excluded; parsed core-command results therefore do not cover every recorded command. No ERROR actions occur in the included 2011, 2021 or 2026 files.
- DE 68.9 is not fully supported by mgz 1.8.51's high-level header parser. The local reader follows its documented DE lobby prefix and validates a newly present empty trailing string after each active player. It reads active identities, recorded speed, date and map dimension, then parses the existing command stream; it does not claim to decode the full new scenario/object state. The ten recent target profile identities and all available body synchronization clocks are checked. See validation.json and scripts/decode.py.
- The local parser and mgz.model share low-level body code; agreement is an implementation cross-check, not independent ground-truth replay playback. The 68.9 addition needs external validation before broader scientific use. No user-facing cognitive result is based on unsupported scenario reconstruction.
- Games within a series/session are correlated. Each 2021 player contributes two series and each recent player one session. No p-values, pseudo-independent command-level tests, confidence intervals or fitted aging curves are reported. The effective independent coverage is much smaller than the number of games.
- We have no matched maps/opponents across periods, no equipment, input bindings, training, fatigue or injury covariates, no repeated laboratory cognition measures and only two players. Calendar time, age, patch and experience are entangled.

## Reproduction and extension

From the project directory, run:

```sh
artifacts/aoe2-aging/.venv/bin/python artifacts/aoe2-aging/scripts/analyze.py
artifacts/aoe2-aging/.venv/bin/python artifacts/aoe2-aging/scripts/validate.py
MPLCONFIGDIR=/private/tmp/aoe2-aging-mpl artifacts/aoe2-aging/.venv/bin/python artifacts/aoe2-aging/scripts/report.py
```

The saved environment uses Python 3.9.13, mgz 1.8.51, aocref 2.0.42, construct 2.8.16 and six 1.17.0; package provenance snapshots are in sources/. Analysis also uses existing numpy 1.26.4, pandas 2.3.3, matplotlib 3.8.2, requests and BeautifulSoup. New packages are confined to this artifact's .venv.

A defensible next study would obtain the unresolved classic/2018 replay packs, collect several independent tournaments/sessions per player and period, stratify 1v1/team format, match map/civilization/opponent level and game phase, and validate stimulus-response event extraction against actual playback. Reaction-time estimates would require an identified visible stimulus, an eligible action, and an exposure denominator including nonresponses. WM would require a validated external task or a separately validated demand model. A compensation claim would then require evidence that a measured strategy change offsets a measured loss under comparable demand; this pilot cannot establish that relationship.

## Sources

- [Shared conversation](https://chatgpt.com/share/6ac2716e-4a5c-83eb-8424-722026696d27): target periods and proposed constructs; assertions were checked rather than treated as data.
- [Hidden Cup 4 archives and alias reveal](https://ageofnotes.com/tutorials/hidden-cup-4-download-all-recorded-games-hc4-2021/).
- [2011 DauT challenge archive](https://uu.getuploader.com/toric/download/110), [2012 paired team series](https://uu.getuploader.com/toric/download/147), [January 2012 expert pack](https://uu.getuploader.com/toric/download/119), [August 2012 team game](https://uu.getuploader.com/toric/download/159).
- [DauT match/profile source](https://www.aoe2insights.com/user/198035/), [TheViper match/profile source](https://www.aoe2insights.com/user/196240/); per-game match URLs are in manifest.json. Microsoft replay requests use the source gameId and profileId. Older files may no longer be available from Microsoft.
- [DauT tournament history](https://aoe-elo.com/player/1/DauT), [TheViper tournament history](https://aoe-elo.com/player/29/TheViper).
- [aoc-mgz source and format parser](https://github.com/happyleavesaoc/aoc-mgz). The local prefix reader is adapted from mgz/fast/header.py under that repository's MIT license.
'''
assert raw_count==46 and archive_count==18 and unique_target_games==37 and len(df)==44 and duplicate_count==5 and len(fail)==3
assert player_counts=={'DauT':25,'TheViper':19}
assert not df.duplicated(['game_id','player']).any()
(ROOT/'REPORT.md').write_text(text)
(ROOT/'README.md').write_text('''# Downloaded AoE2 longitudinal pilot

Open REPORT.md or report.html for findings, missing periods and limits. Raw downloaded archives/replays are in raw/. Results, figures, hashes and validation are in results/. Scripts and pinned added-package versions are included. This is a local descriptive pilot, not a validated cognitive aging result.

46 downloaded replay files; 37 distinct target-player games analyzed, producing 44 player-game observations. Five duplicate files, three validation failures and one unrelated game are excluded. No 2003–2006 or 2018 replay metrics were produced.

The full reproducible methodology and source links are in REPORT.md. Cognitive reaction time, working memory and compensation are unmeasured; behavioral timing/style proxies are reported separately.
''')
# Portable, offline HTML: tables, graphs and searchable per-game data.
img=lambda p:'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()
html_report='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DauT / TheViper replay pilot</title><style>body{font:16px/1.6 system-ui;background:#f6f7fa;color:#17253a;margin:0}main{max-width:1150px;margin:auto;padding:36px}h1{font-size:34px;line-height:1.2}h2{margin-top:40px}img{width:100%;background:white;border-radius:12px}table{border-collapse:collapse;font-size:13px;width:100%;background:white}td,th{text-align:left;padding:9px;border-bottom:1px solid #dce2e9}th{background:#e7ecf3}section{overflow:auto} .notice{border-left:5px solid #b66b25;background:#fff4e4;padding:18px}input,select{font:inherit;padding:8px;margin:8px}a{color:#2466a2}pre{white-space:pre-wrap;background:#fff;padding:16px}</style><main><h1>DauT &amp; TheViper<br>Downloaded replay pilot</h1><p>2011/2012 · 2021 · September 2026 — analyzed locally, 4 October 2026</p><div class="notice"><b>The direction changes with game phase.</b> Whole-game command rates rise from 2021 to 2026; rates in the first ten game minutes fall. These samples cannot identify cognitive aging. Reaction time and working-memory capacity were not measured, and compensation was not demonstrated.</div>'''
html_report+=f'<h2>Replay results</h2><img alt="Replay command rates and phase sensitivity" src="{img(R/"replay_comparison.png")}"><p>46 downloaded replay files, 37 distinct target games analyzed, 44 player-game observations. Five duplicates, three validation failures and one unrelated recording excluded. Missing 2003–2006 and 2018 recordings remain explicit gaps.</p><section>'+summary.round(3).to_html(index=False,border=0)+'</section>'
html_report+='<h2>Fixed opening window</h2><p>First ten game minutes; patch, map and opponent remain unmatched.</p><section>'+opening.round(3).to_html(index=False,border=0)+'</section>'
html_report+=f'<h2>Separate competitive context</h2><img alt="Tournament Elo and listed-series win fractions" src="{img(R/"tournament_context.png")}"><p>Historical completeness and long-term rating-scale stability are unverified. 2026 is a partial year; listed series can include forfeits.</p>'
html_report+='<h2>Inspect individual games</h2><label>Player <select id="player"><option value="">Both</option><option>DauT</option><option>TheViper</option></select></label><label>Search <input id="search" placeholder="year, context or alias"></label><section id="games">'+df[['player','year','context','game_id','alias','core_cpm_nominal','gap_median_nominal_s','switches_per_100_commands','duration_game_min']].round(3).to_html(index=False,border=0)+'</section><script>function filter(){let p=document.querySelector("#player").value,q=document.querySelector("#search").value.toLowerCase();document.querySelectorAll("#games tbody tr").forEach(r=>r.hidden=(p&&r.cells[0].textContent!==p)||!r.textContent.toLowerCase().includes(q))}document.querySelector("#player").addEventListener("change",filter);document.querySelector("#search").addEventListener("input",filter)</script>'
html_report+='<h2>Full methods, findings, sources and limitations</h2><p><a href="REPORT.md">REPORT.md</a> · <a href="results/game_metrics.csv">Per-game CSV</a> · <a href="results/manifest.json">Raw-file inventory and SHA-256 hashes</a> · <a href="results/acquisition_gaps.json">Acquisition gaps</a> · <a href="results/validation.json">Validation evidence</a></p><pre>'+html.escape(text)+'</pre></main></html>'
(ROOT/'report.html').write_text(html_report)
print('Report and figures written',ROOT)
