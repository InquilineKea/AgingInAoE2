# Reaction-time and aging proxies from raw replay commands (2026-10-04)

Script: `../scripts/rt_aging.py` (definitions are in its docstring). It reads the raw
replays for all three players: 25 DauT and 19 TheViper observations from
`../raw/`, and 54 TaToH games from `../tatoh/raw/`. It also reads the opponents'
commands in the same files. Per-game values: `rt_aging_games.csv`; summary:
`rt_aging_results.txt`.

## Verdict

**None of these proxies shows an age-related slowdown for DauT, TheViper or
TaToH.** The two measures with the biggest changes over time move the same way for
their opponents in the same games, so they reflect the game version or era, not the
players. Against opponents in the same game (same map, patch and engine), all three
are as fast as or faster than their opponents in both 2021 and 2026. These are
command-timing proxies, not validated reaction-time or cognitive measures.

## What can and cannot be measured

Replays store commands, not what was on screen, so true stimulus→response time is
unavailable. Two events have a stimulus time that can be reconstructed:

- **Age-up arrival:** the research takes a fixed 130 s (Feudal) or 160 s (Castle) of
  game time, and the game blocks some commands until it completes. This is an
  anticipated stimulus, like a foreperiod task.
- **Attack onset:** another player's ORDER targeting one of the player's units after
  20 s of quiet. The latency includes attacker travel time and the game's alert delay.

## Results (cluster-weighted medians, nominal seconds)

| group | Feudal response | Castle response | attack-onset response | spatial switch cost | task switch cost |
|---|---|---|---|---|---|
| DauT 2011 (classic) | 2.2 | 2.6 | 1.8 | – | – |
| DauT 2021 tournament | 2.4 | 2.1 | 1.9 | 0.73 | 0.54 |
| DauT 2026 ranked | 6.4 | 5.7 (n2) | 0.5 | 0.61 | 0.53 |
| TheViper 2012 team (classic) | 2.5 | 2.8 | 1.6 | – | – |
| TheViper 2021 tournament | 6.6 | 1.5 | 2.2 | 0.95 | 0.60 |
| TheViper 2026 ranked | 6.4 | 1.4 | 1.5 | 0.84 | 0.36 |
| TaToH 2021 tournament (n=1) | 11.0 | 6.2 | 2.3 | 0.96 | 0.48 |
| TaToH 2026 tournament | 2.3 | 4.0 | 0.8 | 0.72 | 0.47 |
| TaToH 2026 ranked | 6.0 | 3.2 | 1.6 | 0.72 | 0.36 |

### Age-up response

Per-game values are bimodal. There is a fast anticipatory mode at 0.5–3 s and a
slow mode at 6–24 s. The slow mode most likely comes from Feudal being queued
behind a villager, or from a deliberate wait; neither can be corrected without game
state. Context dominates: TaToH in the same weeks of 2026 has a median of 2.3 s in
tournament games and 6.0 s in ranked. DauT's apparent rise (2.4 → 6.4 s) coincides
with his switch from tournament to ranked games and is within that context range.
His fastest games are 1.2 s (2021) and 2.8 s (2026); TheViper's are 0.6 and 2.5 s.
Five games per period cannot separate this from noise.

### Attack-onset response and corrective re-orders: era artifacts

| era (DE 1v1) | focal median | opponent median |
|---|---|---|
| attack response, 2021 | 2.21 s | 2.17 s |
| attack response, 2026 | 1.21 s | 1.08 s |
| corrective re-orders per 100, 2021 | 0.18 | 0.22 |
| corrective re-orders per 100, 2026 | 2.74 | 2.64 |

Both shifts are shared with opponents, which points to changes in the game version
or recording. Neither should be read as a player change. The focal-minus-opponent
attack response is about 0 in every period.

### Switch costs (DE only)

This is the extra time after a far camera-scale jump, or after switching command
type. Switch costs are a classic age-sensitive measure in cognitive studies. They
do not rise for anyone:

- DauT: spatial 0.73 → 0.61 s, task 0.54 → 0.53 s
- TheViper: spatial 0.95 → 0.84 s, task 0.60 → 0.36 s
- TaToH: spatial 0.96 → 0.72 s

Compared with opponents in the same game, every player's switch costs are lower
than his opponent's in both eras. The margin is about −0.1 to −0.4 s, and it is
larger in 2026. 2026 opponents are mostly weaker ladder players, so this partly
reflects opponent level. Timestamps are quantized to about 0.12 s, so differences
under about 0.15 s are at resolution.

### Fatigue

The ratio of CPM in minutes 30–40 to minutes 10–20 is only computable in games
lasting 40+ minutes. That leaves 1 such 2026 game each for DauT and TheViper, so it
is not interpretable. TaToH's ratio is 0.96 in his 2021 game and 0.78–1.01 in 2026.

## Limits

- No game state: no unit vision, idle time, hit times or camera position.
- The classic 2011/2012 engine records time in ~1–1.5 s steps. Classic timing is
  only usable for multi-second latencies, and switch costs are not computed for it.
- 2021 vs 2026 is confounded with tournament vs ranked play, map pool, opponent
  level and game patch. TaToH's 2021 data is one partial game.
- These proxies have not been validated against laboratory reaction-time tasks.

A real reaction-time measure would need playback through the game engine (e.g.
CaptureAge or the LibreMatch state stream) to time each first visible enemy unit
against the player's response. That depends on installing AoE2DE (see
`../reanalysis-v2/REPORT.md`).
