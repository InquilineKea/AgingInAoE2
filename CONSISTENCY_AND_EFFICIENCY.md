# Consistency across matches and command efficiency

The selected discussion concerns variability across matches, within sessions, after losses, successive games in a series, and patterns repeated across different days. These are useful questions, but their implementation status differs.

| Question | Current evidence | Limit |
|---|---|---|
| Does a pattern vary between games? | Per-game opening/whole-replay feature rows, period game medians and observed ranges, and cluster-weighted period summaries | Descriptive coverage; no dedicated cross-game variance or reliability model |
| Are command gaps uneven within a game? | Gap CV, gap burstiness, five-second command-count CV, gap quantiles and silence fractions | Command timing measures, not attention or reaction-time diagnoses |
| Does command behavior change within a game? | TaToH 0–5, 5–10, 10–15 and 15–20 game-minute rates and named interval gap summaries | Phase differences can reflect the game's demands rather than fatigue |
| Does performance change over successive games or after a loss? | Recorded dates, series/session clusters and known game outcomes are preserved | The new stamina analysis implements recent ordered-session opening comparisons and descriptive elapsed-hour slopes. After-loss analyses are still incomplete; missing team/partial outcomes remain missing |
| Does the same pattern repeat on different days? | Multiple recent TaToH day clusters; period aggregation gives equal weight to clusters | Independent-day replication has not been formally tested; some player-period samples contain only one cluster |
| Do more commands represent more repetition? | Approximate rapid nearby/same-target repeats and approximate deduplicated core command rates | Destination/target coverage differs between recordings; repeats are not automatically wasted commands |
| Can fewer commands maintain the same output? | A testable hypothesis; competitive results and command counts are stored separately | Validated unit/economic state outputs are needed before claiming output-per-command efficiency or cognitive compensation |

Read `trait_dictionary.csv` before comparing rates. Raw command counts omit device inputs, and useful repeated commands cannot be distinguished from unnecessary repeats solely by proximity. A change in approximate deduplicated rate is not proof of a change in skill, working memory or compensation.

The [stamina follow-up](stamina/REPORT.md) now measures fixed within-game intervals and recent observed-session trajectories. Session history is missing for older recordings, so it does not identify age-related changes in session fatigue. An exploratory replay synchronization counter is audited separately; it is not validated state demand or useful output.
