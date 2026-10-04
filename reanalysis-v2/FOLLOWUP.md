## Follow-up analysis (2026-10-04): what the opening slowdown is, and the rating record

Source: `../scripts/followup_v3.py` re-reads `detailed_actions.jsonl.gz` (97,117
commands) and joins `../results/manifest.json` / `game_metrics.csv` for date, map,
civilization and result. Full output: `followup_results.txt`. Core commands are
MOVE, ORDER, BUILD, RESEARCH, DELETE, BUY, SELL, WALL; rates are per nominal
minute (game clock ÷ recorded speed). The script reproduces the opening medians
above exactly (95.82 / 84.84 DauT, 122.19 / 102.75 TheViper).

**Summary.** Nothing in these replays looks like age-related slowing. The 2026
opening dip sits in game minutes 5–10, coincides with faster, more uniform Feudal
openings, and reverses after minute 10. Within the engine's ~0.12 s timing
resolution, the fastest command cadence is unchanged, and mid-game long pauses
shrink. TheViper's whole-game increase is entirely rapid repeat clicking. Ratings
show DauT modestly off his 2023–24 peak; TheViper is near his tournament peak.

### 1. Matched game-time bins resolve the opening-versus-whole-game paradox

Median core commands per nominal minute. Each bin includes only games that last
past its end.

| | 0–5 | 5–10 | 10–15 | 15–20 | 20–25 |
|---|---|---|---|---|---|
| DauT 2021 (n=9→8) | 104 | 86 | 77 | 77 | 75 |
| DauT 2026 (n=5→3) | 97 | **73** | **96** | 84 | 83 |
| TheViper 2021 (n=5→4) | 120 | 102 | 97 | 83 | 85 |
| TheViper 2026 (n=5→3) | 112 | **92** | **116** | 98 | 101 |

The 2021 tournament games decline steadily with game time. The 2026 ranked games
dip in minutes 5–10, then run about 20 commands/min above 2021 from minute 10 onward. The
whole-game increase is therefore not merely a shorter-game composition effect.
Later bins have small, survivor-selected samples. Median game length: 2021 about 40–49
game min, 2026 about 25–28.

### 2. Openings changed

First Feudal Age research click, game clock (median, range):
DauT 7:59 (6:24–11:15) → 6:43 (6:25–7:51); TheViper 7:42 (7:23–10:43) → 6:40
(6:14–8:22). First Castle click medians: DauT 18:14 → 20:10, TheViper 15:58 →
17:46. The 2021 Hidden Cup 4 games (all map id 59) mix booms and fast-castle
openings. The 2026 ladder games (mostly map id 216) are nearly all fast Feudal
into early aggression. A shorter, more uniform Dark Age plausibly explains the
lower 5–10 minute command rate. DauT's 2012 RESEARCH commands are missing
(ownership gap in that file version), so his 2012 age-ups are unavailable.
Villager queue counts before Feudal were rejected. The 2021 values (23–30 queued)
are physically implausible and must include cancels or re-queues.

### 3. Timing distribution (DE only, 2021 vs 2026)

| | window | gap p50 (s) | gap p90 | gap p99 | peak 10-s rate |
|---|---|---|---|---|---|
| DauT | 0–10 min | 0.364 → 0.362 | 1.50 → 1.60 | 3.87 → 3.87 | 198 → 174 |
| DauT | 10–20 min | 0.364 → 0.362 | 1.85 → 1.56 | 5.11 → 4.06 | 198 → 210 |
| TheViper | 0–10 min | 0.237 → 0.246 | 1.22 → 1.44 | 3.45 → 3.50 | 222 → 204 |
| TheViper | 10–20 min | 0.249 → 0.238 | 1.76 → 1.38 | 5.37 → 3.37 | 216 → 255 |

Median cadence is unchanged. The long-pause tail (where generalized slowing would be
expected) shortens in mid-game. **Resolution limit:** DE command timestamps are
quantized to ~0.195–0.208 game s (~0.12 nominal s) network turns. The 10th
percentile of positive gaps is about 0.115–0.123 s for every group because it
sits on this floor. Slowing of tens of milliseconds is undetectable here. Classic
2011/2012 files are quantized at ~1–1.5 game s and are excluded from timing
comparisons.

### 4. Rapid re-clicks

Re-click = MOVE/ORDER within 0.5 nominal s of the previous MOVE/ORDER, with
destination within 2 tiles or the same target.

| | re-click share, opening | de-duplicated opening CPM | re-click share, whole | de-duplicated whole CPM |
|---|---|---|---|---|
| DauT 2021 → 2026 | 27% → 27% | 67 → 62 | 27% → 30% | 55 → 63 |
| TheViper 2021 → 2026 | 40% → 41% | 76 → 63 | 35% → 44% | 62 → 58 |

About 40% of TheViper's opening commands are near-duplicates (DauT about 27%). Raw counts
inflate the between-player gap. TheViper's whole-game rise disappears after
de-duplication. DauT's survives.

### 5. Same-era player comparison

Opening CPM ratio TheViper/DauT: 1.20 (2012), 1.28 (2021), 1.21 (2026). DauT, the
older player, fell less from 2021 to 2026 (−11% vs −16%). A shared shift is better
explained by shared context (patch, ladder vs tournament, maps, opponents) than
by age.

### 6. Uncertainty and context

Exact game-level permutation tests, 2021 vs 2026, all give p = 0.12–0.20. This
holds for opening, minutes 10–20 and whole-game CPM, with Cliff's δ of
|0.33–0.62|. These tests treat games in a series as independent and are therefore
anti-conservative. Each 2026 sample is one evening, i.e. one cluster. Opponents
differ sharply. In 2021, DauT went 5–4 and TheViper 5–0 against top pros under
Hidden Cup aliases. In 2026, both went 4–1 against ladder opponents, and three of
DauT's games were against clanmate Kingstone. Within the 2026 sessions, opening
CPM shows no monotone trend across games 1–5.

### 7. Have their ratings declined?

**Tournament Elo** (aoe-elo.com series data, `../results/tournament_years.csv`):

| | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (partial) |
|---|---|---|---|---|---|---|
| DauT median | 2222 | 2270 | 2337 | **2371** | 2328 | 2296 (last 2276) |
| TheViper median | 2338 | 2358 | 2387 | 2444 | 2432 | **2456** (max 2481) |
| TheViper − DauT | 116 | 88 | 50 | 73 | 104 | 160 |

**RM 1v1 ladder** (aoe2companion snapshot 2026-10-04,
`ladder_rm1v1_history.csv`; history starts Oct 2022):

| | 2022 | 2023 | 2024 | 2025 | 2026 | peak | latest |
|---|---|---|---|---|---|---|---|
| DauT median | 2403 | 2578 | 2541 | 2488 | 2576 | 2752 (Jun 2023) | 2684 |
| TheViper median | 2592 | 2692 | 2660 | 2659 | 2705 | 2911 (Nov 2024) | 2781 |

- **DauT:** modestly off peak. His tournament Elo peaked in 2023–24 and is
  down about 75 (median) to 120 (last value) points, but remains above 2021–22. The
  gap to TheViper widened from about 50 (2023) to about 160 (2026). His ladder rating is
  noisy, with no clear trend. The 2026 median matches 2023, and the latest value is
  about 70 below his 2023 peak.
- **TheViper:** no decline. His 2026 tournament median is the highest of the series.
  His ladder rating is about 130 below a single Nov 2024 high, but his 2026 median is his
  highest annual median.
- His tournament series win share fell (86% in 2021 → 62% in 2026) while his
  Elo rose. This points to tougher fields and Elo's opponent adjustment, not
  weaker play.
- Caveats: both rating scales can drift (pool growth, inflation at the top, the
  DE-era tournament boom). Ladder ratings depend on how often and against whom
  each player queues. 2026 is a partial year. Ratings measure competitive results
  and say nothing directly about cognition.

### 8. Peer comparison (relative standing)

Tournament Elo drifts upward for everyone, so standing relative to peers is the
fairer test. Peer set: ACCM, DauT, Hera, Liereyy, MbL, Nicov, TaToH, TheViper, Yo
(aoe-elo.com). Source: `../scripts/peer_compare.py`; full output:
`../tatoh/peer_comparison.txt`. Ranks use yearly median Elo. Series records
exclude draws.

| year | DauT rank | DauT gap to best | DauT vs peers | Viper rank | Viper gap to best other | Viper vs peers |
|---|---|---|---|---|---|---|
| 2018 | 7/9 | −216 | 3–8 | 1/9 | +152 | 12–2 |
| 2020 | 8/9 | −132 | 4–11 | 1/9 | +46 | 27–10 |
| 2021 | 6/9 | −116 | 14–15 | 1/9 | +36 | 21–6 |
| 2022 | 8/9 | −94 | 5–15 | 2/9 | −6 | 14–6 |
| 2023 | 6/9 | −99 | 11–16 | 3/9 | −49 | 26–19 |
| 2024 | 6/9 | −162 | 4–12 | 2/9 | −89 | 14–10 |
| 2025 | 9/9 | −246 | 3–11 | 3/9 | −142 | 9–9 |
| 2026 | 9/9 | −302 | 0–2 | 3/9 | −142 | 6–6 |

Elo gain 2021→2026 (2022→2026): Hera +295 (+248), Liereyy +268 (+211),
ACCM +241 (+161), MbL +160 (+116), Yo +157 (+99), TaToH +164 (+48),
Nicov +123 (+45), TheViper +118 (+98), DauT +74 (+26).

- **TheViper:** ranked #1 of this group every year from 2015 to 2021. He has been
  #2–3 since 2022, and his lead turned into a 142-point deficit to Hera. His series
  record against peers fell from 78% (2021) to 50% (2025–26), while his record
  against everyone else stays 68–89%. His absolute Elo is still at its peak, the
  same plateau-while-others-rise pattern as TaToH.
- **DauT:** never near the top of this group. He has the smallest gain of the nine,
  is last in 2025–26, and his gap to the best grew from −94 (2022) to −302 (2026).
  He has won 21–27% of series against peers since 2022 (0–2 so far in 2026), but
  still wins 77–85% against everyone else. This is the clearest relative decline of
  the three. His absolute Elo is down about 75 from its 2024 peak.
- **Common factor:** most of everyone's relative slide comes from Hera, Liereyy and
  ACCM climbing about 160–250 points since 2022. Fewer series against peers in
  2025–26 make those win rates noisy. Birth years were not used here, so this does
  not test whether gains track age.

The pattern most consistent with these data is a possible modest post-2023
decline in DauT's competitive results, absolute and relative. TheViper shows a
relative slip only, with no absolute decline. The command data contain no
signature of slowing for either player.
