# Individual findings across earliest and latest recordings

These are descriptive comparisons of the available archive, not causal aging effects. The period estimates below give each series/session equal weight; this can differ from the earlier two-game pilot or an unweighted game median. The full tables retain both weighted and game medians and observed ranges. Core commands are MOVE, ORDER, BUILD, RESEARCH, DELETE, BUY, SELL and WALL. Basic replay APM counts all attributed ACTION records, including non-core/production commands; it is not device-input APM.

## DauT

Earliest archive: four November 2011 challenge games. Latest archive: five September 2026 ranked games. Opening attributed-action rate rises 53.3 → 99.7/minute, core rate 53.3 → 84.8, and approximate deduplicated core rate 38.7 → 61.7. Classic ownership and encoding differences make the apparent increase uninterpretable as cognitive improvement. The earliest and latest individual files also show higher recorded command rates, but that comparison has one game per endpoint.

The more comparable 2021→2026 DE comparison (9 games/2 series → 5 games/1 session) shows:

- Opening core rate decreases 95.8 → 84.8/minute; all-action rate is nearly unchanged, 100.9 → 99.7. Whole-game core rate rises 74.7 → 86.1 and all-action rate rises 88.6 → 106.7.
- Median positive opening command gap is nearly unchanged, 0.364 → 0.362 nominal seconds; p99 is unchanged, 3.865 → 3.872. The share of opening time in command gaps of at least five seconds increases 1.7% → 4.1%; whole-game long-gap time decreases 6.2% → 5.8%. This is a phase-specific pause pattern, not generalized slowing.
- Opening gap burstiness decreases 0.093 → 0.079; whole-game burstiness increases 0.097 → 0.131. Timing regularity therefore also depends on phase.
- Whole-game rapid nearby/same-target repeat share increases 29.0% → 32.0%, but deduplicated core rate still rises 55.5 → 62.5. The whole-game action increase is not explained entirely by re-clicks.
- Whole-game category entropy decreases 1.221 → 0.976 bits and category switches decrease 28.7% → 25.2%. Opening category entropy increases 0.700 → 0.756. A lower whole-game diversity score is not a memory-capacity score.
- Large destination jumps decrease: opening 7.8% → 5.1%, whole game 8.9% → 6.2%. Whole-game destination entropy decreases 3.313 → 3.047 bits. Commands are more spatially concentrated in these recent games; unit movement and camera attention are unmeasured.
- Whole-game build, research and market command rates decrease (5.75 → 3.22, 1.31 → 0.93, 0.45 → 0.33/minute), while wall requests increase 0.34 → 0.44. Shorter games and different maps/strategies can explain these composition changes. Opening wall/research rates are unchanged at their period medians.
- Feudal research is requested earlier, 8:00 → 6:44 game-clock time. This is an opening-strategy change; completed age-ups have not been measured.
- Raw actor-group size/revisit changes are not interpretable longitudinally because selection reuse and explicit-list coverage differ. Recent engine captures improve coverage, but have no historical engine baseline.

Overall observed pattern: quieter opening core activity, more whole-game commands, more spatial concentration and modestly more repetition. The increased opening pause fraction is a candidate for matched follow-up, but the stable opening cadence and greater later activity do not establish broad age-related slowing.

## TheViper

Earliest archive: nine 2012 team-game observations across three clusters. Latest archive: five September 2026 ranked games from one session. Opening attributed-action rate rises 73.8 → 138.2/minute; core rate rises 73.7 → 102.8. Team-versus-1v1 settings and classic-versus-DE ownership/encoding differences prevent an age interpretation.

The 2021→2026 DE comparison (5 games/2 series → 5 games/1 session) shows:

- Opening core rate decreases 111.4 → 102.8/minute with equal-cluster weighting; opening all-action rate increases 117.0 → 138.2. The earlier unweighted opening core median was 122.2, illustrating sensitivity to series weighting. Whole-game core rate rises 91.4 → 103.3; all-action rate rises 115.5 → 141.1.
- Median positive opening gap is stable, 0.243 → 0.246 seconds, and p99 is stable, 3.552 → 3.504. Opening long-gap time decreases 3.6% → 3.1%; whole-game long-gap time decreases 7.3% → 4.9%.
- Whole-game repeat share increases 39.1% → 46.3%. Approximate deduplicated whole-game core rate decreases 60.6 → 58.3. Higher raw action volume therefore does not imply more distinct actions; re-clicks contribute substantially. Repetition can be useful micro or redundant input, so efficiency cannot be inferred without outcomes/state.
- Whole-game category entropy decreases 1.421 → 1.089 bits and category switches decrease 27.7% → 22.7%. Opening category entropy also decreases slightly, 0.933 → 0.873.
- Large destination jumps decrease, opening 9.3% → 4.5% and whole game 9.9% → 6.1%. Whole-game destination entropy decreases 3.491 → 2.833 bits. This is greater command concentration, not a demonstrated loss of attention switching.
- Whole-game build and research command rates decrease 6.44 → 2.75 and 2.74 → 0.59/minute. Opening build and wall rates are unchanged at period medians. Whole-game strategy/duration composition matters substantially.
- Feudal research is requested earlier, 7:42 → 6:41 game-clock time. Different openings can explain phase-specific activity changes.
- Group switching and revisit traits from raw records are coverage-limited; the recent engine actor tables cannot supply a younger baseline.

Overall observed pattern: more non-core recorded actions and repeated orders, more spatially concentrated command destinations, fewer long pauses, and lower deduplicated whole-game core volume. The repetition/deduplication change is worth investigating, but is not proof of slowing or compensation.

## TaToH

Earliest verified identity baseline: one partial March 2021 tournament recording containing the first 69.5 game minutes. Latest samples: 13 tournament games across four series and 40 ranked games across 12 days in 2026. One 6.2-minute ranked game is omitted from ten-minute opening metrics. The latest individual file is from October 3, 2026.

The 2019 community-attributed FeudalVoy replay is separate: opening core rate is 108.7 versus 108.0 in recent ranked play, but the identity is not independently verified, the recording appears to be a Feudal-only challenge, and classic ownership is incomplete. It is not a verified earlier cognitive baseline.

For 2021→2026 tournament play:

- Opening core rate is stable, 101.2 → 102.8/minute, while all-action rate rises 106.1 → 130.5. Whole-available-replay core rate rises 77.3 → 85.6, but the old denominator is an incomplete match.
- Opening median positive gap is stable, 0.249 → 0.246 seconds. Opening p99 increases 2.95 → 3.30 seconds, while time in gaps of at least five seconds decreases 6.2% → 3.4%. The opening tail is mixed rather than uniformly slower. Whole-game p99 decreases 5.10 → 4.68.
- Opening approximate deduplicated core rate decreases 68.3 → 60.3; whole-game deduplicated rate rises slightly, 57.2 → 59.2. Whole-game repeat share is stable, 30.7% → 30.8%.
- Opening category entropy increases 0.824 → 0.998 bits, while whole-game entropy decreases 1.567 → 1.313. Opening large destination jumps increase 3.8% → 8.8%; whole-game jumps are nearly unchanged, 10.3% → 9.9%. Custom tournament maps/settings differ, so these are composition changes.
- Opening build requests decrease 2.87 → 2.54/minute; wall requests are unchanged at 1.52. Research requests rise from zero to 0.85/minute, but start-age/regicide/custom-map settings make this a poor planning or cognition comparison.

For 2021 tournament→2026 ranked play, opening core rate rises 101.2 → 108.0 and whole-game rate rises 77.3 → 91.0; opening deduplicated rate is close, 68.3 → 66.4. Opening long-gap time decreases to 2.0%, while p99 increases to 3.45 seconds. The latest individual tournament game's opening p99 is essentially the same as the old game's (2.95 → 2.96 seconds). Single-game and aggregate tails therefore need repeated-session validation.

Overall observed pattern: stable tournament core cadence, greater all-action volume, fewer long command silences, and context-dependent changes in diversity and spatial distribution. The historical baseline is too small to establish a trend or aging effect.

## Competitive outcomes and unavailable traits

The separate local rating snapshot has DauT's 2026 annual tournament median 75 points below his highest annual median (2024), TheViper at his highest annual median, and TaToH 26 points below his highest annual median (2024). These are competitive-result changes, with partial-year and rating-pool limitations; they do not identify cognitive causes. Sample wins and losses are reported separately, with unavailable team outcomes and the TaToH partial-game result left unknown.

Economy idle time, completed production efficiency, combat efficiency, projectile avoidance, visibility-conditioned threat response and multiple-front interference cannot yet be compared: the required state/visibility schema is undecoded. Working-memory capacity, perceptual reaction time and compensation have not been measured. The final tables preserve missing values and restrictions instead of inventing scores.
