# DauT and TheViper: longitudinal replay pilot

Completed locally on 2026-10-04. Actual downloads and command parsing, with explicit acquisition gaps. This is a descriptive convenience sample, not an identified estimate of cognitive aging.

## Main finding

The sampled behavior changes over time, but the direction depends on the comparison. Whole-game median core command rate rises from 2021 to 2026 for both players, while the rate in the first ten game minutes falls for both. This disagreement is evidence that game phase/composition matters; it does not establish an age-related slowdown or preserved cognition. The maps, patch, opponents and tournament-versus-ladder setting also change.

| Player   |   whole_game_change_pct |   opening_change_pct |   whole_game_switch_change |
|:---------|------------------------:|---------------------:|---------------------------:|
| DauT     |                   15.25 |               -11.46 |                      -3.46 |
| TheViper |                    9.07 |               -15.91 |                      -4.22 |

## What was actually obtained

46 extracted replay files from 18 source ZIP archives: 31 from 2021/2026 and 15 from 2011/2012. 43 files pass decoding and ownership checks. Five of those are byte-identical duplicates despite different filenames, and one has neither target player; all six are excluded from metrics. Thus 37 distinct games contribute 44 player-game observations (25 DauT, 19 TheViper; seven games contain both). Three files are rejected by the inclusion checks: one 2012 replay has incomplete core-command ownership, and two additional 2021 HC4 replays are restored recordings with nonzero initial restore times (21:16 and 2:11 game time). The construct parser recovers their headers after the fast-header path fails. They are excluded because their partial coverage cannot support the same zero-origin opening comparison. Every raw file remains preserved. The duplicate/source issues illustrate why filenames alone cannot establish sample size.

| player   |   year | context        |   games |
|:---------|-------:|:---------------|--------:|
| DauT     |   2011 | 1v1 challenge  |       4 |
| DauT     |   2012 | team game      |       7 |
| DauT     |   2021 | 1v1 tournament |       9 |
| DauT     |   2026 | 1v1 ranked     |       5 |
| TheViper |   2012 | team game      |       9 |
| TheViper |   2021 | 1v1 tournament |       5 |
| TheViper |   2026 | 1v1 ranked     |       5 |

The six-game May 2012 team series contains both players, providing the strongest same-game comparison available in this pilot. Three other Viper team games and a four-versus-four recording were downloaded; one of those Viper files is rejected, and an unrelated eight-player game is excluded. Team games are presented separately, not pooled into a 1v1 aging curve. The early date labels come from archive upload dates and filenames; exact play dates are unverified. The September 2026 timestamps are read from the replay headers.

For 2021, the HC4 aliases are Gonzalo Pizarro = DauT and Ivaylo = TheViper, based on the source page's alias reveal. The HC4 profile IDs belong to tournament aliases and are not assumed to equal the current ladder profiles. September 2026 identities are checked against header profile 198035 (DauT) and 196240 (TheViper), including their actual player slots. All ten recent games are ranked RM 1v1.

The 2003–2006 DauT and 2018 samples proposed in the shared chat could not be acquired from the checked links. Some AoEZone attachment pages explicitly say the attachment cannot be shown; the recently restored 2004 pack is listed but its download is blocked/times out in this environment, so its availability remains unresolved. AoE2recs returns a browser 522 timeout. These failures do not prove that all copies are lost. The earlier chat's July 2026 exemplar returns HTTP 404 at Microsoft's replay endpoint and was replaced with September recordings. See acquisition_gaps.json for exact links and statuses. Early-period replay coverage is therefore incomplete.

## Measures and observed values

| Player   |   Year | Context        |   Games |   Source/session clusters |   Core commands / nominal minute |   Median gap (nominal seconds) |   Class switches / 100 commands |   DE queue batch mean |
|:---------|-------:|:---------------|--------:|--------------------------:|---------------------------------:|-------------------------------:|--------------------------------:|----------------------:|
| DauT     |   2011 | 1v1 challenge  |       4 |                         1 |                           50.482 |                          0.72  |                          31.792 |               nan     |
| DauT     |   2012 | team game      |       7 |                         2 |                           46.929 |                          0.66  |                          32.306 |               nan     |
| DauT     |   2021 | 1v1 tournament |       9 |                         2 |                           74.722 |                          0.48  |                          28.712 |                 1.007 |
| DauT     |   2026 | 1v1 ranked     |       5 |                         1 |                           86.118 |                          0.362 |                          25.249 |                 1.04  |
| TheViper |   2012 | team game      |       9 |                         3 |                           62.487 |                          0.51  |                          29.191 |               nan     |
| TheViper |   2021 | 1v1 tournament |       5 |                         2 |                           94.728 |                          0.247 |                          26.917 |                 1     |
| TheViper |   2026 | 1v1 ranked     |       5 |                         1 |                          103.323 |                          0.238 |                          22.695 |                 1     |

Each value is a median across games, giving every game equal weight. Core commands are MOVE, ORDER, BUILD, RESEARCH, DELETE, BUY, SELL and WALL; WALL and BUILD share the construction class, BUY and SELL share the market class. Commands whose ownership is missing in a generation are excluded from every generation. Raw command count is not physical keyboard/mouse APM and is not the same definition as a website's eAPM. Repeated movement commands are retained, not interpreted as useful actions or capacity.

The replay clock is simulated game time. For the nominal wall-time columns, game timestamps are divided by the recorded speed (1.5 in these classic files, approximately 1.69 in the DE files). This estimates active wall time under the nominal speed and cannot recover lag, pauses, hardware input latency or actual frame timing. Game-time versions of the metrics are also in the CSVs. Simultaneous command timestamps are retained; positive-gap percentiles are available separately and must not be treated as a person's minimum RT.

Whole-game class-switch medians fall from 28.71 to 25.25 per 100 core commands for DauT and from 26.92 to 22.70 for TheViper. However, the first-ten-minute switch rates rise (16.88 to 19.56 for DauT; 18.42 to 21.09 for TheViper), another phase-dependent result. Command-class entropy and 4×4 spatial entropy describe the distribution of recorded commands/coordinates, not the distribution of attention. Generic ORDER commands have ambiguous economic/military purpose and are not assigned to either task.

In the six paired 2012 games, TheViper's command rate exceeds DauT's in all six. The per-game excess is 12.09–24.33 core commands per nominal minute. This establishes an older play-style difference within those shared games; it does not identify a difference in working memory or reaction time.

### First ten game minutes (fixed exposure window)

| player   |   year |   core_cpm_nominal |   gap_median_nominal_s |   switches_per_100_commands |
|:---------|-------:|-------------------:|-----------------------:|----------------------------:|
| DauT     |   2021 |             95.823 |                  0.364 |                      16.883 |
| DauT     |   2026 |             84.838 |                  0.362 |                      19.557 |
| TheViper |   2021 |            122.187 |                  0.237 |                      18.421 |
| TheViper |   2026 |            102.752 |                  0.246 |                      21.087 |

This restriction reduces whole-game duration/composition differences but does not equate build orders, visible events, map, civilization, opponent pressure or biological age effects. It is a sensitivity analysis, not a matched experiment. Five-minute trajectories are preserved in phase_metrics.csv.

## Reaction time, working memory and compensation

| Requested construct | What these recordings support | Current conclusion |
|---|---|---|
| Reaction time | Inter-command gaps, command cadence and short-window burst rate | True RT is unmeasured. A gap is not stimulus-to-response latency; the relevant visible stimulus/onset and correct response are not identified. |
| Working memory | Command-class switches, sequence entropy and spatial command dispersion | WM capacity and its change are unmeasured. These behavior proxies have no validated mapping to a memory score in this pilot. |
| Compensation | Production batching and patterns of command allocation, alongside competitive results | No demonstrated compensation mechanism. A style change cannot establish that strategy compensates for a capacity loss unless both the loss and the compensating behavior are measured under comparable demands. |

DauT's DE-only mean positive queue batch moves from approximately 1.007 to 1.040 units per command at the game-median level; TheViper's remains 1.000. This small, context-sensitive change is a candidate for follow-up, not evidence of cognitive compensation. Classic QUEUE ownership is incomplete, so queue batching is not compared to 2011/2012. No hidden task management, camera awareness, control-group use, or building idle time is claimed to have been reconstructed. No stimulus-linked RT or recall task was performed.

## Competitive history, kept separate

Downloaded and extracted 793 dated DauT tournament-series entries (2002–2026) and 637 dated TheViper entries (2011–2026) from AoE Tournament Elo. Synthetic initial-estimate/current-Elo chart points are excluded. The 'victory/defeat/draw' label is used, because score ordering can be reversed when the player is on the right side. Walkovers/forfeits can occur in this archive and remain part of its listed-series data.

The site's listed-series win fractions change from 52/79 (65.8%) in 2021 to 51/66 (77.3%) in 2026 for DauT, and from 50/58 (86.2%) to 21/34 (61.8%) for TheViper. The 2026 year is partial. These are not opponent-adjusted biological performance scores: field strength, event selection and formats vary, and archive completeness is not established. Site-defined Elo is a competitive-context metric with potential long-run scale drift, not an absolute cognitive-capacity scale. Neither the replay convenience samples nor win fractions prove decline, improvement or compensation caused by aging.

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
