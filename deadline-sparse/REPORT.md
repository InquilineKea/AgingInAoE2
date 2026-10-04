# Sparse replay pilot: DauT and TheViper across career periods

A reproducible hackathon pilot measuring command behavior in younger and later career recordings. This is a descriptive feasibility study; it does not measure cognitive aging.

## Sampling and provenance

Earliest dated two games per player/year with game_id tie-break; 2026 TheViper uses the two shortest available games for deadline-compatible state validation. Selection uses no command-feature outcome. Convenience sampling and duration selection introduce bias.

Two games per available player/year: DauT 2011, 2012, 2021, 2026; TheViper 2012, 2021, 2026. All selected raw replay SHA-256 hashes were checked. Every sampled game has whole-game commands and a standardized first-ten-game-minute window. Historical dates can be upload/filename dates; see provenance.json.

14 player-game observations from 14 distinct replay files. Shared team games can contribute observations to both players and are not independent.

## Measured results

Opening and whole-game command rates are per nominal real minute: game-clock duration divided by replay-recorded nominal speed. They are not directly measured human input rates.

| Player | Year | Games / clusters | Opening commands/min | Whole-game commands/min | Opening large destination jumps |
|---|---:|---:|---:|---:|---:|
| DauT | 2011 | 2 / 1 | 47.5 | 45.6 | 5.7% |
| DauT | 2012 | 2 / 1 | 57.8 | 42.5 | 12.9% |
| DauT | 2021 | 2 / 2 | 97.1 | 71.2 | 13.2% |
| DauT | 2026 | 2 / 1 | 88.8 | 87.9 | 5.1% |
| TheViper | 2012 | 2 / 1 | 55.6 | 47.6 | 2.3% |
| TheViper | 2021 | 2 / 1 | 126.6 | 107.5 | 10.3% |
| TheViper | 2026 | 2 / 1 | 99.4 | 100.7 | 3.9% |

A large destination jump is a distance of at least one-quarter map diagonal between consecutive valid move/order destinations. It measures spatial command dispersion; it does not measure gaze, attention switching or memory.

DauT: the sparse opening median changes from 97.1 in 2021 to 88.8 in 2026 (-8.5%). This is a sample difference, not an identified age effect.
TheViper: the sparse opening median changes from 126.6 in 2021 to 99.4 in 2026 (-21.5%). This is a sample difference, not an identified age effect.

Full-data sensitivity check: the previously validated 2021/2026 opening medians are DauT 95.82 → 84.84 and TheViper 122.19 → 102.75. Whole-game medians rise in that larger sample (DauT 74.72 → 86.12; TheViper 94.73 → 103.32). A general slowing claim is therefore unsupported. See full_period_summary.csv.

## What the features can establish

- Command frequency and destination dispersion: observed replay command behavior.
- Build/wall/research rates: issued commands, not completed actions or strategic success.
- Reaction time: unavailable without a visible threat onset and a linked response. Command gaps are not reaction time.
- Working memory: not measured. No validated memory task or capacity estimate is present.
- Compensation: hypothesis only. More planning or repeated commands cannot by itself establish compensation.
- Onager dodging: zero classified episodes; projectile/state decoding and threat visibility remain unvalidated.

## State capture status

Recent game-state streams are optional technical validation, separate from the longitudinal command comparison. The running sparse queue targets one complete DauT game and the two shortest recent TheViper games. A second DauT capture preserves more than ten game minutes but is an incomplete match. Historical 2021 state simulation needs an older DE engine; 2011/2012 needs a compatible classic engine. These historical state frames have not been collected. The current API22 binary state schema is not decoded. See state_capture_status.json for the build-time snapshot and ../engine-pass/status.json for live progress.

## Limits and next experiment

Classic and DE files have different command encoding and timestamp granularity; cross-engine rates are exploratory. The 2012 recordings include team games; player-slot ownership and research coverage vary by version. 2021 is tournament play and 2026 is a small ranked session. Maps, opponents, civilizations, patches and game lengths differ. Two games per stratum provide no reliable population uncertainty or age attribution; no significance tests are presented. Explicit actor selection covers only part of raw commands, so group switching is excluded from longitudinal conclusions.

The next falsifiable experiment would sample matched maps, civilizations, opponents and game phases, identify visible projectile threats, measure threat-to-command latency in game-clock time with timestamp-resolution checks, and score dodge outcomes. Repeated sessions and independent tournaments are required before an age interpretation.

## Reproduce

Run `python artifacts/aoe2-aging/scripts/deadline_sparse.py` from the repository root. Inputs are the existing verified replay-command tables and original raw files. The ZIP includes sampled replays, provenance, selected rows, period summaries, full-data sensitivity, validation and the script. No credentials or player chat are included.
