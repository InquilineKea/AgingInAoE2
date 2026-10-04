# TaToH: ratings and replay analysis (2026-10-04)

Scripts: `../scripts/fetch_tatoh.py` (downloads), `../scripts/tatoh_analyze.py`
(analysis). Full output: `results.txt`. Per-game metrics for TaToH and each opponent:
`game_metrics.csv`. Peer tournament-Elo series: `tournament_elo_peers.csv`; DauT/TheViper/TaToH peer ranks and records: `peer_comparison.txt` (`../scripts/peer_compare.py`).
Download log with hashes and HTTP status: `downloads.json`.

## Short answer

**There is no absolute decline. There is a relative one.**

- **Ladder:** RM 1v1 is at a career high. It stood at 2884 on 2026-09-30, the
  maximum of the history available since Dec 2022, and ranks #6.
- **Tournament Elo is flat:** 2364 (2022 median) → 2381 → 2437 → 2407 → 2411
  (2026). The peak was 2472 in May 2024.
- **Relative to eight other top players, he slid from 1st (2022) to 6th of 9
  (2025–26).** The gap to the best of them went from 0 to −186. His series record
  against those players went from 61% (2022) to 50% (2023–25) to 30% (2026 so far,
  3–7, small n). His overall series win rate stays 69–76%: he still beats the
  rest of the field.
- **What's behind it, as far as the data can show:** the others rose while he
  plateaued. From 2022 to 2026 Hera gained +248, Liereyy +210, ACCM +161,
  Yo +99, TaToH +47. His tournament volume against this group also fell: 42 series
  in 2023, 18 in 2024, 16 in 2025, 10 in 2026 so far. Total series fell from 109
  to 58, 67 and 35. Whether less top-level play is a cause or a consequence can't
  be separated here.
- **The replays show no mechanical slowdown.** Opening and mid-game command rates
  and the median command gap match his only usable 2021 game. His long pauses in
  mid-game are shorter. The 2021 baseline is a single game, though (see limits).

## Tournament Elo, yearly median (aoe-elo.com)

| year | ACCM | DauT | Hera | Liereyy | MbL | Nicov | **TaToH** | TheViper | Yo | TaToH rank | gap to best |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2019 | 2040 | 2119 | 2037 | 2193 | 2187 | 2116 | **2179** | 2309 | 2137 | 4/9 | −130 |
| 2020 | 2135 | 2148 | 2219 | 2200 | 2169 | 2158 | **2205** | 2280 | 2234 | 4/9 | −75 |
| 2021 | 2194 | 2222 | 2302 | 2281 | 2204 | 2209 | **2247** | 2338 | 2275 | 5/9 | −91 |
| 2022 | 2274 | 2270 | 2350 | 2338 | 2248 | 2287 | **2364** | 2358 | 2333 | **1/9** | 0 |
| 2023 | 2332 | 2337 | 2436 | 2406 | 2262 | 2307 | **2381** | 2387 | 2373 | 4/9 | −55 |
| 2024 | 2356 | 2371 | 2533 | 2389 | 2311 | 2332 | **2437** | 2444 | 2398 | 3/9 | −96 |
| 2025 | 2414 | 2328 | 2574 | 2483 | 2359 | 2351 | **2407** | 2432 | 2425 | 6/9 | −167 |
| 2026 | 2435 | 2296 | 2598 | 2548 | 2364 | 2332 | **2411** | 2456 | 2432 | 6/9 | −186 |

The scale drifts upward over time, which is why rank and gap matter more than the
raw number. The peer set is a hand-picked group of long-running top players, not
the full top 10.

## Replay sample and weighting

| period | games | clusters | TaToH W–L | context |
|---|---|---|---|---|
| 2021 tournament | 1 (partial, first 69.5 game-min) | HC4 Ro16 vs Hera | series lost | custom tournament map |
| 2026 tournament | 13 | 4 series: DongHaiDi, Lamo, Capoch, Sora Kuma | 12–1 | Garrison qualifiers / lobbies, custom maps |
| 2026 ranked | 40 | 12 play days | 32–7 | RM 1v1, mostly Arabian Desert |

Excluded: two restarts (<5 game-min), one 2026 file whose header failed
validation, and the 2019 archive.org file. That file's players are "+Zaid" and
"feudalVoy", so TaToH's identity can't be verified from it.
**Weighting:** inside each period, every series or play day gets equal weight and
games share their cluster's weight (weighted medians). This keeps a single
11-game ranked day or a 4-game series from dominating.

## Replay metrics, TaToH (cluster-weighted medians)

| metric | 2021 tournament (n=1) | 2026 tournament | 2026 ranked |
|---|---|---|---|
| Opening (0–10 min) core CPM | 101.2 | 102.8 | 108.0 |
| CPM, minutes 5–10 | 79.8 | 90.6 | 97.0 |
| CPM, minutes 10–20 | 80.1 | 80.1 | 93.0 |
| Whole-game CPM | 77.3 | 85.6 | 91.0 |
| Rapid re-click share, opening | 0.33 | 0.35 | 0.40 |
| De-duplicated opening CPM | 68.3 | 60.3 | 65.9 |
| Median gap, opening (s) | 0.25 | 0.25 | 0.24 |
| p90 gap, opening (s) | 1.38 | 1.45 | 1.44 |
| p99 gap, minutes 10–20 (s) | 5.97 | 4.40 | 3.84 |

Definitions and timing-resolution limits (~0.12 s network turns) are the same as
in `../reanalysis-v2/FOLLOWUP.md`. Age-up click times are in `game_metrics.csv`
but are **not comparable**. The 2026 tournament maps (Regicide Fortress, Chaos Pit,
Nomad, Xingu, …) put Feudal at about 4–6 min because of their settings.

**Same-game comparison with opponents** (same map and patch). In 2026 tournaments
TaToH's opening CPM is +4.4 above his opponent's (13 games); in ranked it's +12.5
(39 games). In mid-game the 2026 tournament difference is about zero.

**Fixed-matchup anchor, TaToH vs Hera:**

| game | TaToH opening CPM | Hera opening CPM | ratio |
|---|---|---|---|
| HC4 2021, game 1 | 101.2 | 108.5 | 0.93 |
| Ranked, 2026-09-22 | 102.4 | 120.2 | 0.85 |

TaToH is unchanged and Hera is faster. This matches the rating story (Hera rising,
TaToH flat). It is one game on each side and should not be over-read.

**Reference, same metric code:** opening CPM in 2026 is 84.8 for DauT, 102.8 for
TheViper and about 103–108 for TaToH.

## Why there is no proper long time series

No weighted set of older TaToH replays could be built from accessible public sources:

- **Microsoft replay endpoint:** retains about 6–8 weeks. Every TaToH game tested
  before late August 2026 returns 404.
- **ageofnotes HC4 pack** (`7.-HC4-Ro16-Le-Loi-vs-John-the-Fearless.zip`): truncated
  on the server at exactly 512 KiB (`content-length: 524288`). Only 84.8% of
  game 1 was recoverable, by raw-deflate salvage. The truncated copy is kept in `raw/`.
- **aocrecs.com** (HC2, HC3, NAC1–3, KotD2 archives): does not respond.
- **aoezone.net** recorded-game threads: behind a browser bot challenge, which was
  not circumvented.
- **Liquipedia's Google Drive links** for TaToH's events: tournament handbooks,
  not replays.
- **aoe2recs.com:** now a live spectator dashboard, not an archive.

With replay packs for, e.g., 2019 (Voobly/UserPatch), 2022 and 2024, `fetch_tatoh.py`
and `tatoh_analyze.py` can be extended to a real per-year series. Classic-engine
files would be timing-quantized and not directly comparable to DE (see FOLLOWUP §3).
