# TaToH extension and basic replay APM

TaToH adds one partial 2021 tournament replay, two 2026 tournament games and two 2026 ranked games. Earliest available tournament games were selected by date/game name; ranked games use the existing TheViper-versus-TaToH capture and one additional compatible short replay. This is convenience sampling. The two recent ranked games are from separate days. There is no verified 2011/2012 TaToH baseline.

| Period | Games | Partial games | Opening core CPM | Whole available core CPM |
|---|---:|---:|---:|---:|
| 2021 tournament | 1 | 1 | 101.2 | 77.3 |
| 2026 ranked | 2 | 0 | 113.6 | 103.4 |
| 2026 tournament | 2 | 0 | 91.8 | 85.3 |

The 2021 archive was truncated upstream. Its first 69.5 game minutes were recovered; opening coverage is present, but its available-replay rate is not a complete-match rate. That single historical game cannot establish a temporal trend. TaToH identity is checked through profile 197388 or the documented HC4 alias Le Loi.

## Basic APM definition

Replay-derived APM counts all decoded ACTION records explicitly attributed to the player, including production/queue commands, divided by nominal minutes (game clock / recorded game speed). It does not count mouse clicks, camera movement, hotkeys or selections that leave no attributed ACTION record. ACTION semantics and ownership coverage differ across engine versions. Do not present this as device-input APM or directly compare it to CaptureAge/eAPM without matching definitions. Core CPM excludes non-core action types; the two measures have different denominators of actions.

| Player | Period | Games | Opening replay APM | Whole available replay APM |
|---|---|---:|---:|---:|
| DauT | 2011 1v1 challenge | 2 | 47.5 | 46.1 |
| DauT | 2012 team game | 2 | 57.8 | 42.9 |
| DauT | 2021 1v1 tournament | 2 | 101.4 | 89.4 |
| DauT | 2026 1v1 ranked | 2 | 104.9 | 107.5 |
| TaToH | 2021 tournament | 1 | 106.1 | 98.1 |
| TaToH | 2026 ranked | 2 | 144.4 | 141.8 |
| TaToH | 2026 tournament | 2 | 107.7 | 121.8 |
| TheViper | 2012 team game | 2 | 56.1 | 68.0 |
| TheViper | 2021 1v1 tournament | 2 | 132.8 | 125.2 |
| TheViper | 2026 1v1 ranked | 2 | 128.9 | 131.3 |

These rates measure recorded actions. Reaction time, working-memory capacity and compensation remain unmeasured. No age-effect test is claimed.

Completed engine captures: one DauT match and two TheViper matches. The 14.6-minute TheViper game also includes TaToH, so one complete TaToH state stream is already available. The additional 17.6-minute TaToH match is also fully captured. All four selected match captures passed end verification with zero reported skipped simulation steps. Current binary state remains undecoded. State command summaries are included; raw state streams remain in engine-pass and are not embedded in this small ZIP.
