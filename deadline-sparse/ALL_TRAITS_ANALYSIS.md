# Earliest-to-latest analysis of all measured replay traits

All available measurements are compared below. The 255-entry catalog includes candidates and controls; many require world state or visibility that has not been decoded. Those candidates are not silently treated as completed traits.

The expanded command dataset has 98 verified player-game observations: 44 DauT/TheViper observations and 54 TaToH observations. One 6.2-minute TaToH replay is excluded from the ten-minute opening window. The community-attributed 2019 replay is analyzed separately.

Each session/series receives equal weight inside a period; games share that cluster weight. Weighted medians are used for the headline comparison, with game medians and full observed ranges retained in CSV. This is descriptive analysis. The very small number of independent early clusters precludes reliable aging-effect inference.

## Endpoint files

- DauT: 211c10a368c4 (2011-11 (uploaded 2011-11-29), 1v1 challenge) → 23d4576b7264 (2026-09-25T00:26:26+00:00, 1v1 ranked).
- TheViper: 2a4d86704ada (2012-01-06 (filename; uploaded 2012-01-07), team game) → 3598af4f05ca (2026-09-30T15:48:39+00:00, 1v1 ranked).
- TaToH: hc4_tatoh_vs_hera (2021-03, tournament) → lobby_511057711 (2026-10-03T17:05, tournament).

These are the earliest and latest dated files available here, not first/last career games. Exact month-level ordering can be uncertain. The single-game CSV provides the literal contrast; period tables provide a less brittle comparison.

## Main interpretation

DauT and TheViper issue more attributed commands in recent DE recordings than in the earliest classic files, but missing classic command ownership and different settings prevent interpreting the increase as improved cognition. Within DE, both show lower core-command rates in the opening but higher whole-game core rates. APM, deduplication, phase and command types change the result. TaToH has only one partial 2021 baseline; tournament and ranked comparisons must stay separate.

No measured trait establishes reaction-time change, working-memory change, compensation or causal aging. Repetition, gaps, diversity and spatial switching are behavior measures. Actor-group comparisons from raw files have coverage artifacts; recent engine captures resolve actor lists but have no historical engine baseline.

## Key measures

### DauT earliest period

2011 1v1 challenge → 2026 1v1 ranked. Limits: classic versus DE; challenge versus ranked; age cannot be isolated.

| Trait | Window | Early weighted median | Late weighted median | Direction |
|---|---|---:|---:|---|
| all_recorded_cpm | first 10 game minutes | 53.25 | 99.71 | increase |
| all_recorded_cpm | whole available replay | 50.7 | 106.7 | increase |
| core_cpm | first 10 game minutes | 53.25 | 84.84 | increase |
| core_cpm | whole available replay | 50.48 | 86.12 | increase |
| dedup_core_cpm | first 10 game minutes | 38.7 | 61.69 | increase |
| dedup_core_cpm | whole available replay | 38.12 | 62.5 | increase |
| core_gap_p50_s | first 10 game minutes | 0.69 | 0.3615 | decrease |
| core_gap_p50_s | whole available replay | 0.75 | 0.3615 | decrease |
| core_gap_p99_s | first 10 game minutes | 9.547 | 3.872 | decrease |
| core_gap_p99_s | whole available replay | 8.358 | 4.333 | decrease |
| command_silence_ge5s_time_fraction | first 10 game minutes | 0.3275 | 0.04062 | decrease |
| command_silence_ge5s_time_fraction | whole available replay | 0.2313 | 0.05773 | decrease |
| core_gap_burstiness | first 10 game minutes | 0.1516 | 0.07851 | decrease |
| core_gap_burstiness | whole available replay | 0.1468 | 0.1309 | decrease |
| core_category_entropy_bits | first 10 game minutes | 0.9903 | 0.7562 | decrease |
| core_category_entropy_bits | whole available replay | 1.351 | 0.9761 | decrease |
| destination_jump_ge_quarter_fraction | first 10 game minutes | 0.06614 | 0.05123 | decrease |
| destination_jump_ge_quarter_fraction | whole available replay | 0.07746 | 0.06245 | decrease |
| rapid_destination_repeat_fraction | first 10 game minutes | 0.284 | 0.2801 | decrease |
| rapid_destination_repeat_fraction | whole available replay | 0.2742 | 0.3197 | increase |

### TheViper earliest period

2012 team game → 2026 1v1 ranked. Limits: classic versus DE; team versus ranked; age cannot be isolated.

| Trait | Window | Early weighted median | Late weighted median | Direction |
|---|---|---:|---:|---|
| all_recorded_cpm | first 10 game minutes | 73.8 | 138.2 | increase |
| all_recorded_cpm | whole available replay | 68.68 | 141.1 | increase |
| core_cpm | first 10 game minutes | 73.72 | 102.8 | increase |
| core_cpm | whole available replay | 62.22 | 103.3 | increase |
| dedup_core_cpm | first 10 game minutes | 56.85 | 63.21 | increase |
| dedup_core_cpm | whole available replay | 47.66 | 58.28 | increase |
| core_gap_p50_s | first 10 game minutes | 0.75 | 0.2462 | decrease |
| core_gap_p50_s | whole available replay | 0.87 | 0.2385 | decrease |
| core_gap_p99_s | first 10 game minutes | 5.543 | 3.504 | decrease |
| core_gap_p99_s | whole available replay | 8.885 | 4.085 | decrease |
| command_silence_ge5s_time_fraction | first 10 game minutes | 0.08325 | 0.03148 | decrease |
| command_silence_ge5s_time_fraction | whole available replay | 0.2454 | 0.04863 | decrease |
| core_gap_burstiness | first 10 game minutes | 0.1572 | 0.1453 | decrease |
| core_gap_burstiness | whole available replay | 0.2309 | 0.1818 | decrease |
| core_category_entropy_bits | first 10 game minutes | 0.8426 | 0.8728 | increase |
| core_category_entropy_bits | whole available replay | 1.391 | 1.089 | decrease |
| destination_jump_ge_quarter_fraction | first 10 game minutes | 0.02013 | 0.04452 | increase |
| destination_jump_ge_quarter_fraction | whole available replay | 0.048 | 0.06142 | increase |
| rapid_destination_repeat_fraction | first 10 game minutes | 0.2296 | 0.4258 | increase |
| rapid_destination_repeat_fraction | whole available replay | 0.2774 | 0.4626 | increase |

### DauT DE control

2021 1v1 tournament → 2026 1v1 ranked. Limits: same engine family; patch/map/opponent/tournament versus ranked confounds.

| Trait | Window | Early weighted median | Late weighted median | Direction |
|---|---|---:|---:|---|
| all_recorded_cpm | first 10 game minutes | 100.9 | 99.71 | decrease |
| all_recorded_cpm | whole available replay | 88.6 | 106.7 | increase |
| core_cpm | first 10 game minutes | 95.82 | 84.84 | decrease |
| core_cpm | whole available replay | 74.72 | 86.12 | increase |
| dedup_core_cpm | first 10 game minutes | 67.26 | 61.69 | decrease |
| dedup_core_cpm | whole available replay | 55.47 | 62.5 | increase |
| core_gap_p50_s | first 10 game minutes | 0.3645 | 0.3615 | decrease |
| core_gap_p50_s | whole available replay | 0.4805 | 0.3615 | decrease |
| core_gap_p99_s | first 10 game minutes | 3.865 | 3.872 | increase |
| core_gap_p99_s | whole available replay | 4.644 | 4.333 | decrease |
| command_silence_ge5s_time_fraction | first 10 game minutes | 0.01667 | 0.04062 | increase |
| command_silence_ge5s_time_fraction | whole available replay | 0.06222 | 0.05773 | decrease |
| core_gap_burstiness | first 10 game minutes | 0.09276 | 0.07851 | decrease |
| core_gap_burstiness | whole available replay | 0.09653 | 0.1309 | increase |
| core_category_entropy_bits | first 10 game minutes | 0.7005 | 0.7562 | increase |
| core_category_entropy_bits | whole available replay | 1.221 | 0.9761 | decrease |
| destination_jump_ge_quarter_fraction | first 10 game minutes | 0.07752 | 0.05123 | decrease |
| destination_jump_ge_quarter_fraction | whole available replay | 0.08948 | 0.06245 | decrease |
| rapid_destination_repeat_fraction | first 10 game minutes | 0.284 | 0.2801 | decrease |
| rapid_destination_repeat_fraction | whole available replay | 0.2897 | 0.3197 | increase |

### TheViper DE control

2021 1v1 tournament → 2026 1v1 ranked. Limits: same engine family; patch/map/opponent/tournament versus ranked confounds.

| Trait | Window | Early weighted median | Late weighted median | Direction |
|---|---|---:|---:|---|
| all_recorded_cpm | first 10 game minutes | 117 | 138.2 | increase |
| all_recorded_cpm | whole available replay | 115.5 | 141.1 | increase |
| core_cpm | first 10 game minutes | 111.4 | 102.8 | decrease |
| core_cpm | whole available replay | 91.37 | 103.3 | increase |
| dedup_core_cpm | first 10 game minutes | 71.06 | 63.21 | decrease |
| dedup_core_cpm | whole available replay | 60.56 | 58.28 | decrease |
| core_gap_p50_s | first 10 game minutes | 0.2426 | 0.2462 | increase |
| core_gap_p50_s | whole available replay | 0.2982 | 0.2385 | decrease |
| core_gap_p99_s | first 10 game minutes | 3.552 | 3.504 | decrease |
| core_gap_p99_s | whole available replay | 4.212 | 4.085 | decrease |
| command_silence_ge5s_time_fraction | first 10 game minutes | 0.03637 | 0.03148 | decrease |
| command_silence_ge5s_time_fraction | whole available replay | 0.07306 | 0.04863 | decrease |
| core_gap_burstiness | first 10 game minutes | 0.1552 | 0.1453 | decrease |
| core_gap_burstiness | whole available replay | 0.1798 | 0.1818 | increase |
| core_category_entropy_bits | first 10 game minutes | 0.9327 | 0.8728 | decrease |
| core_category_entropy_bits | whole available replay | 1.421 | 1.089 | decrease |
| destination_jump_ge_quarter_fraction | first 10 game minutes | 0.09346 | 0.04452 | decrease |
| destination_jump_ge_quarter_fraction | whole available replay | 0.09944 | 0.06142 | decrease |
| rapid_destination_repeat_fraction | first 10 game minutes | 0.4159 | 0.4258 | increase |
| rapid_destination_repeat_fraction | whole available replay | 0.3907 | 0.4626 | increase |

### TaToH tournament control

2021 tournament → 2026 tournament. Limits: one partial historical game; settings/maps/opponents differ.

| Trait | Window | Early weighted median | Late weighted median | Direction |
|---|---|---:|---:|---|
| all_recorded_cpm | first 10 game minutes | 106.1 | 130.5 | increase |
| all_recorded_cpm | whole available replay | 98.11 | 118.1 | increase |
| core_cpm | first 10 game minutes | 101.2 | 102.8 | increase |
| core_cpm | whole available replay | 77.26 | 85.58 | increase |
| dedup_core_cpm | first 10 game minutes | 68.28 | 60.33 | decrease |
| dedup_core_cpm | whole available replay | 57.16 | 59.23 | increase |
| core_gap_p50_s | first 10 game minutes | 0.2485 | 0.2462 | decrease |
| core_gap_p50_s | whole available replay | 0.3645 | 0.3615 | decrease |
| core_gap_p99_s | first 10 game minutes | 2.953 | 3.304 | increase |
| core_gap_p99_s | whole available replay | 5.103 | 4.685 | decrease |
| command_silence_ge5s_time_fraction | first 10 game minutes | 0.06211 | 0.03386 | decrease |
| command_silence_ge5s_time_fraction | whole available replay | 0.09392 | 0.06348 | decrease |
| core_gap_burstiness | first 10 game minutes | 0.1566 | 0.1341 | decrease |
| core_gap_burstiness | whole available replay | 0.1621 | 0.1552 | decrease |
| core_category_entropy_bits | first 10 game minutes | 0.8243 | 0.9977 | increase |
| core_category_entropy_bits | whole available replay | 1.567 | 1.313 | decrease |
| destination_jump_ge_quarter_fraction | first 10 game minutes | 0.03846 | 0.0885 | increase |
| destination_jump_ge_quarter_fraction | whole available replay | 0.1027 | 0.09925 | decrease |
| rapid_destination_repeat_fraction | first 10 game minutes | 0.3409 | 0.37 | increase |
| rapid_destination_repeat_fraction | whole available replay | 0.3074 | 0.308 | increase |

### TaToH earliest verified to ranked

2021 tournament → 2026 ranked. Limits: one partial historical game; tournament versus ranked and map/opponent confounds.

| Trait | Window | Early weighted median | Late weighted median | Direction |
|---|---|---:|---:|---|
| all_recorded_cpm | first 10 game minutes | 106.1 | 134.2 | increase |
| all_recorded_cpm | whole available replay | 98.11 | 125.8 | increase |
| core_cpm | first 10 game minutes | 101.2 | 108 | increase |
| core_cpm | whole available replay | 77.26 | 91.02 | increase |
| dedup_core_cpm | first 10 game minutes | 68.28 | 66.42 | decrease |
| dedup_core_cpm | whole available replay | 57.16 | 62.44 | increase |
| core_gap_p50_s | first 10 game minutes | 0.2485 | 0.2385 | decrease |
| core_gap_p50_s | whole available replay | 0.3645 | 0.3615 | decrease |
| core_gap_p99_s | first 10 game minutes | 2.953 | 3.455 | increase |
| core_gap_p99_s | whole available replay | 5.103 | 4.085 | decrease |
| command_silence_ge5s_time_fraction | first 10 game minutes | 0.06211 | 0.01998 | decrease |
| command_silence_ge5s_time_fraction | whole available replay | 0.09392 | 0.05577 | decrease |
| core_gap_burstiness | first 10 game minutes | 0.1566 | 0.1396 | decrease |
| core_gap_burstiness | whole available replay | 0.1621 | 0.1455 | decrease |
| core_category_entropy_bits | first 10 game minutes | 0.8243 | 0.6841 | decrease |
| core_category_entropy_bits | whole available replay | 1.567 | 1.13 | decrease |
| destination_jump_ge_quarter_fraction | first 10 game minutes | 0.03846 | 0.05424 | increase |
| destination_jump_ge_quarter_fraction | whole available replay | 0.1027 | 0.09255 | decrease |
| rapid_destination_repeat_fraction | first 10 game minutes | 0.3409 | 0.419 | increase |
| rapid_destination_repeat_fraction | whole available replay | 0.3074 | 0.3244 | increase |

### TaToH provisional 2019

2019 provisional Feudal-only → 2026 ranked. Limits: unverified account identity; special challenge; classic command attribution gap; excluded from verified inference.

| Trait | Window | Early weighted median | Late weighted median | Direction |
|---|---|---:|---:|---|
| all_recorded_cpm | first 10 game minutes | 108.7 | 134.2 | increase |
| all_recorded_cpm | whole available replay | 92.67 | 125.8 | increase |
| core_cpm | first 10 game minutes | 108.7 | 108 | decrease |
| core_cpm | whole available replay | 91.54 | 91.02 | decrease |
| dedup_core_cpm | first 10 game minutes | 65.19 | 66.42 | increase |
| dedup_core_cpm | whole available replay | 60.7 | 62.44 | increase |
| core_gap_p50_s | first 10 game minutes | 0.32 | 0.2385 | decrease |
| core_gap_p50_s | whole available replay | 0.6063 | 0.3615 | decrease |
| core_gap_p99_s | first 10 game minutes | 4.627 | 3.455 | decrease |
| core_gap_p99_s | whole available replay | 4.817 | 4.085 | decrease |
| command_silence_ge5s_time_fraction | first 10 game minutes | 0.1027 | 0.01998 | decrease |
| command_silence_ge5s_time_fraction | whole available replay | 0.07264 | 0.05577 | decrease |
| core_gap_burstiness | first 10 game minutes | 0.2112 | 0.1396 | decrease |
| core_gap_burstiness | whole available replay | 0.1571 | 0.1455 | decrease |
| core_category_entropy_bits | first 10 game minutes | 0.6277 | 0.6841 | increase |
| core_category_entropy_bits | whole available replay | 1.215 | 1.13 | decrease |
| destination_jump_ge_quarter_fraction | first 10 game minutes | 0.0453 | 0.05424 | increase |
| destination_jump_ge_quarter_fraction | whole available replay | 0.06861 | 0.09255 | increase |
| rapid_destination_repeat_fraction | first 10 game minutes | 0.4094 | 0.419 | increase |
| rapid_destination_repeat_fraction | whole available replay | 0.3628 | 0.3244 | decrease |

## Every measured trait, with coverage

These tables retain absent baselines as unavailable. Actor-selection numeric changes are reported for completeness but not interpreted as historical group-control changes.

### DauT earliest period

| Trait | Window | Early | Late | Δ | Games early/late |
|---|---|---:|---:|---:|---:|
| all_recorded_cpm | first 10 game minutes | 53.25 | 99.71 | 46.46 | 4/5 |
| core_cpm | first 10 game minutes | 53.25 | 84.84 | 31.59 | 4/5 |
| noncore_action_fraction | first 10 game minutes | 0 | 0.1678 | 0.1678 | 4/5 |
| first_core_command_nominal_s | first 10 game minutes | 2.97 | 1.292 | -1.678 | 4/5 |
| core_gap_p10_s | first 10 game minutes | 0.345 | 0.1231 | -0.2219 | 4/5 |
| core_gap_p50_s | first 10 game minutes | 0.69 | 0.3615 | -0.3285 | 4/5 |
| core_gap_p90_s | first 10 game minutes | 3.165 | 1.596 | -1.569 | 4/5 |
| core_gap_p99_s | first 10 game minutes | 9.547 | 3.872 | -5.675 | 4/5 |
| core_gap_max_s | first 10 game minutes | 14.98 | 6.492 | -8.493 | 4/5 |
| simultaneous_core_gap_fraction | first 10 game minutes | 0.1787 | 0 | -0.1787 | 4/5 |
| core_gap_cv | first 10 game minutes | 1.358 | 1.17 | -0.1873 | 4/5 |
| core_gap_burstiness | first 10 game minutes | 0.1516 | 0.07851 | -0.07312 | 4/5 |
| command_silence_ge5s_time_fraction | first 10 game minutes | 0.3275 | 0.04062 | -0.2868 | 4/5 |
| command_silence_ge10s_time_fraction | first 10 game minutes | 0.09499 | 0 | -0.09499 | 4/5 |
| core_count_5s_cv | first 10 game minutes | 0.7844 | 0.433 | -0.3513 | 4/5 |
| peak_5s_nominal_cpm | first 10 game minutes | 174 | 192 | 18 | 4/5 |
| empty_5s_bin_fraction | first 10 game minutes | 0.1187 | 0.01389 | -0.1049 | 4/5 |
| core_type_entropy_bits | first 10 game minutes | 0.9903 | 0.7914 | -0.1988 | 4/5 |
| core_category_entropy_bits | first 10 game minutes | 0.9903 | 0.7562 | -0.2341 | 4/5 |
| core_type_transition_entropy_bits | first 10 game minutes | 0.828 | 0.6833 | -0.1446 | 4/5 |
| core_type_switch_fraction | first 10 game minutes | 0.2396 | 0.1959 | -0.04369 | 4/5 |
| core_category_switch_fraction | first 10 game minutes | 0.2385 | 0.1956 | -0.04293 | 4/5 |
| core_same_type_triplet_fraction | first 10 game minutes | 0.6357 | 0.7057 | 0.06997 | 4/5 |
| coordinate_coverage | first 10 game minutes | 1 | 1 | 0 | 4/5 |
| destination_jump_diagonal_p50 | first 10 game minutes | 0.02012 | 0.02483 | 0.004707 | 4/5 |
| destination_jump_diagonal_p90 | first 10 game minutes | 0.2125 | 0.1634 | -0.04918 | 4/5 |
| destination_jump_ge_quarter_fraction | first 10 game minutes | 0.06614 | 0.05123 | -0.01491 | 4/5 |
| destination_entropy_4x4_bits | first 10 game minutes | 2.666 | 2.683 | 0.01665 | 4/5 |
| destination_cell_switch_fraction | first 10 game minutes | 0.2906 | 0.3102 | 0.01951 | 4/5 |
| rapid_destination_repeat_fraction | first 10 game minutes | 0.284 | 0.2801 | -0.003974 | 4/5 |
| dedup_core_cpm | first 10 game minutes | 38.7 | 61.69 | 22.99 | 4/5 |
| move_order_commands | first 10 game minutes | 340.5 | 489 | 148.5 | 4/5 |
| explicit_actor_commands | first 10 game minutes | 112.5 | 188 | 75.5 | 4/5 |
| explicit_actor_coverage | first 10 game minutes | 0.3513 | 0.4023 | 0.05104 | 4/5 |
| actor_pair_count | first 10 game minutes | 42.5 | 86 | 43.5 | 4/5 |
| same_actor_pair_count | first 10 game minutes | 0 | 8 | 8 | 4/5 |
| actor_group_size_median | first 10 game minutes | 1 | 1 | 0 | 4/5 |
| actor_group_size_p90 | first 10 game minutes | 3.2 | 3 | -0.2 | 4/5 |
| actor_group_ge10_fraction | first 10 game minutes | 0 | 0.005319 | 0.005319 | 4/5 |
| actor_group_change_fraction | first 10 game minutes | 1 | 0.8939 | -0.1061 | 4/5 |
| actor_overlap_jaccard_median | first 10 game minutes | 0 | 0 | 0 | 4/5 |
| same_actor_gap_nominal_median_s | first 10 game minutes | — | 0.3615 | — | 0/5 |
| same_actor_recommand_under1s_fraction | first 10 game minutes | — | 0.875 | — | 0/5 |
| commanded_actor_ids | first 10 game minutes | 31 | 30 | -1 | 4/5 |
| valid_target_order_fraction | first 10 game minutes | 0.7598 | 1 | 0.2402 | 4/5 |
| distinct_order_target_ids | first 10 game minutes | 24.5 | 30 | 5.5 | 4/5 |
| distinct_building_type_ids | first 10 game minutes | 5 | 6 | 1 | 4/5 |
| distinct_research_type_ids | first 10 game minutes | 1.5 | 2 | 0.5 | 4/5 |
| positive_de_queue_commands | first 10 game minutes | — | 23 | — | 0/5 |
| requested_queue_unit_type_ids | first 10 game minutes | — | 2 | — | 0/5 |
| explicitly_commanded_production_building_ids | first 10 game minutes | — | 2 | — | 0/5 |
| production_command_revisit_nominal_median_s | first 10 game minutes | — | 14.55 | — | 0/5 |
| positive_queue_amount_mean | first 10 game minutes | — | 1.13 | — | 0/5 |
| build_commands_nominal_min | first 10 game minutes | 1.575 | 1.859 | 0.284 | 4/5 |
| wall_commands_nominal_min | first 10 game minutes | 0.075 | 0.507 | 0.432 | 4/5 |
| research_commands_nominal_min | first 10 game minutes | 0.3 | 0.338 | 0.038 | 4/5 |
| market_commands_nominal_min | first 10 game minutes | 0 | 0 | 0 | 4/5 |
| legacy_command_class_entropy_bits | first 10 game minutes | — | — | — | 0/0 |
| legacy_switches_per_100_commands | first 10 game minutes | — | — | — | 0/0 |
| legacy_core_silence_over5s_fraction | first 10 game minutes | — | — | — | 0/0 |
| legacy_peak_10s_nominal_cpm | first 10 game minutes | — | — | — | 0/0 |
| legacy_move_share | first 10 game minutes | — | — | — | 0/0 |
| legacy_planning_command_share | first 10 game minutes | — | — | — | 0/0 |
| legacy_queue_batch_mean | first 10 game minutes | — | — | — | 0/0 |
| legacy_queue_batch_gt1_fraction | first 10 game minutes | — | — | — | 0/0 |
| legacy_duration_game_min | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_0_5 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_5_10 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_10_15 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_15_20 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_10_20 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_reclick_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_dedup_open_cpm | first 10 game minutes | — | — | — | 0/0 |
| tatoh_reclick_whole | first 10 game minutes | — | — | — | 0/0 |
| tatoh_dedup_whole_cpm | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p50_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p90_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p99_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p99_10_20 | first 10 game minutes | — | — | — | 0/0 |
| feudal_request_game_s | first 10 game minutes | 433.3 | 403.7 | -29.63 | 2/5 |
| castle_request_game_s | first 10 game minutes | 463.6 | — | — | 1/0 |
| imperial_request_game_s | first 10 game minutes | — | — | — | 0/0 |
| all_recorded_cpm | whole available replay | 50.7 | 106.7 | 55.99 | 4/5 |
| core_cpm | whole available replay | 50.48 | 86.12 | 35.64 | 4/5 |
| noncore_action_fraction | whole available replay | 0.004429 | 0.1893 | 0.1849 | 4/5 |
| first_core_command_nominal_s | whole available replay | 2.97 | 1.292 | -1.678 | 4/5 |
| core_gap_p10_s | whole available replay | 0.36 | 0.1231 | -0.2369 | 4/5 |
| core_gap_p50_s | whole available replay | 0.75 | 0.3615 | -0.3885 | 4/5 |
| core_gap_p90_s | whole available replay | 3.06 | 1.677 | -1.383 | 4/5 |
| core_gap_p99_s | whole available replay | 8.358 | 4.333 | -4.025 | 4/5 |
| core_gap_max_s | whole available replay | 21.33 | 11.06 | -10.27 | 4/5 |
| simultaneous_core_gap_fraction | whole available replay | 0.1366 | 0.0008319 | -0.1357 | 4/5 |
| core_gap_cv | whole available replay | 1.344 | 1.301 | -0.04302 | 4/5 |
| core_gap_burstiness | whole available replay | 0.1468 | 0.1309 | -0.01591 | 4/5 |
| command_silence_ge5s_time_fraction | whole available replay | 0.2313 | 0.05773 | -0.1736 | 4/5 |
| command_silence_ge10s_time_fraction | whole available replay | 0.06397 | 0.01867 | -0.0453 | 4/5 |
| core_count_5s_cv | whole available replay | 0.7106 | 0.5206 | -0.19 | 4/5 |
| peak_5s_nominal_cpm | whole available replay | 180 | 216 | 36 | 4/5 |
| empty_5s_bin_fraction | whole available replay | 0.08357 | 0.01702 | -0.06655 | 4/5 |
| core_type_entropy_bits | whole available replay | 1.363 | 0.9916 | -0.3714 | 4/5 |
| core_category_entropy_bits | whole available replay | 1.351 | 0.9761 | -0.3751 | 4/5 |
| core_type_transition_entropy_bits | whole available replay | 1.164 | 0.9083 | -0.256 | 4/5 |
| core_type_switch_fraction | whole available replay | 0.3188 | 0.2533 | -0.06553 | 4/5 |
| core_category_switch_fraction | whole available replay | 0.3179 | 0.2525 | -0.06542 | 4/5 |
| core_same_type_triplet_fraction | whole available replay | 0.5083 | 0.6187 | 0.1104 | 4/5 |
| coordinate_coverage | whole available replay | 1 | 1 | 0 | 4/5 |
| destination_jump_diagonal_p50 | whole available replay | 0.02107 | 0.01987 | -0.001196 | 4/5 |
| destination_jump_diagonal_p90 | whole available replay | 0.217 | 0.1679 | -0.04914 | 4/5 |
| destination_jump_ge_quarter_fraction | whole available replay | 0.07746 | 0.06245 | -0.01501 | 4/5 |
| destination_entropy_4x4_bits | whole available replay | 2.664 | 3.047 | 0.3839 | 4/5 |
| destination_cell_switch_fraction | whole available replay | 0.276 | 0.2684 | -0.007565 | 4/5 |
| rapid_destination_repeat_fraction | whole available replay | 0.2742 | 0.3197 | 0.04549 | 4/5 |
| dedup_core_cpm | whole available replay | 38.12 | 62.5 | 24.38 | 4/5 |
| move_order_commands | whole available replay | 1010 | 1268 | 257.5 | 4/5 |
| explicit_actor_commands | whole available replay | 414.5 | 565 | 150.5 | 4/5 |
| explicit_actor_coverage | whole available replay | 0.4135 | 0.4117 | -0.001872 | 4/5 |
| actor_pair_count | whole available replay | 193.5 | 248 | 54.5 | 4/5 |
| same_actor_pair_count | whole available replay | 5.5 | 45 | 39.5 | 4/5 |
| actor_group_size_median | whole available replay | 2 | 2 | 0 | 4/5 |
| actor_group_size_p90 | whole available replay | 13 | 8 | -5 | 4/5 |
| actor_group_ge10_fraction | whole available replay | 0.1392 | 0.05364 | -0.08552 | 4/5 |
| actor_group_change_fraction | whole available replay | 0.9707 | 0.8171 | -0.1536 | 4/5 |
| actor_overlap_jaccard_median | whole available replay | 0 | 0 | 0 | 4/5 |
| same_actor_gap_nominal_median_s | whole available replay | 2.858 | 0.3615 | -2.496 | 4/5 |
| same_actor_recommand_under1s_fraction | whole available replay | 0.1833 | 0.7708 | 0.5875 | 4/5 |
| commanded_actor_ids | whole available replay | 194 | 77 | -117 | 4/5 |
| valid_target_order_fraction | whole available replay | 0.8706 | 1 | 0.1294 | 4/5 |
| distinct_order_target_ids | whole available replay | 125 | 106 | -19 | 4/5 |
| distinct_building_type_ids | whole available replay | 13.5 | 12 | -1.5 | 4/5 |
| distinct_research_type_ids | whole available replay | 23.5 | 12 | -11.5 | 4/5 |
| positive_de_queue_commands | whole available replay | — | 84 | — | 0/5 |
| requested_queue_unit_type_ids | whole available replay | — | 5 | — | 0/5 |
| explicitly_commanded_production_building_ids | whole available replay | — | 5 | — | 0/5 |
| production_command_revisit_nominal_median_s | whole available replay | — | 12.86 | — | 0/5 |
| positive_queue_amount_mean | whole available replay | — | 1.04 | — | 0/5 |
| build_commands_nominal_min | whole available replay | 5.056 | 3.223 | -1.834 | 4/5 |
| wall_commands_nominal_min | whole available replay | 0.1034 | 0.4381 | 0.3347 | 4/5 |
| research_commands_nominal_min | whole available replay | 1.442 | 0.9306 | -0.5117 | 4/5 |
| market_commands_nominal_min | whole available replay | 0.4922 | 0.3286 | -0.1636 | 4/5 |
| legacy_command_class_entropy_bits | whole available replay | 1.351 | 0.9761 | -0.3751 | 4/5 |
| legacy_switches_per_100_commands | whole available replay | 31.79 | 25.25 | -6.542 | 4/5 |
| legacy_core_silence_over5s_fraction | whole available replay | 0.2313 | 0.05773 | -0.1736 | 4/5 |
| legacy_peak_10s_nominal_cpm | whole available replay | 177 | 216 | 39 | 4/5 |
| legacy_move_share | whole available replay | 0.6654 | 0.7799 | 0.1146 | 4/5 |
| legacy_planning_command_share | whole available replay | 0.127 | 0.05015 | -0.07687 | 4/5 |
| legacy_queue_batch_mean | whole available replay | — | 1.04 | — | 0/5 |
| legacy_queue_batch_gt1_fraction | whole available replay | — | 0.01333 | — | 0/5 |
| legacy_duration_game_min | whole available replay | 37.9 | 25.17 | -12.73 | 4/5 |
| tatoh_cpm_0_5 | whole available replay | — | — | — | 0/0 |
| tatoh_cpm_5_10 | whole available replay | — | — | — | 0/0 |
| tatoh_cpm_10_15 | whole available replay | — | — | — | 0/0 |
| tatoh_cpm_15_20 | whole available replay | — | — | — | 0/0 |
| tatoh_cpm_10_20 | whole available replay | — | — | — | 0/0 |
| tatoh_reclick_open | whole available replay | — | — | — | 0/0 |
| tatoh_dedup_open_cpm | whole available replay | — | — | — | 0/0 |
| tatoh_reclick_whole | whole available replay | — | — | — | 0/0 |
| tatoh_dedup_whole_cpm | whole available replay | — | — | — | 0/0 |
| tatoh_gap_p50_open | whole available replay | — | — | — | 0/0 |
| tatoh_gap_p90_open | whole available replay | — | — | — | 0/0 |
| tatoh_gap_p99_open | whole available replay | — | — | — | 0/0 |
| tatoh_gap_p99_10_20 | whole available replay | — | — | — | 0/0 |
| feudal_request_game_s | whole available replay | 599.6 | 403.7 | -195.9 | 4/5 |
| castle_request_game_s | whole available replay | 1053 | 1210 | 157.1 | 4/5 |
| imperial_request_game_s | whole available replay | 1596 | 1929 | 332.7 | 3/1 |

### TheViper earliest period

| Trait | Window | Early | Late | Δ | Games early/late |
|---|---|---:|---:|---:|---:|
| all_recorded_cpm | first 10 game minutes | 73.8 | 138.2 | 64.44 | 9/5 |
| core_cpm | first 10 game minutes | 73.72 | 102.8 | 29.03 | 9/5 |
| noncore_action_fraction | first 10 game minutes | 0.003745 | 0.2319 | 0.2281 | 9/5 |
| first_core_command_nominal_s | first 10 game minutes | 1.98 | 0.8 | -1.18 | 9/5 |
| core_gap_p10_s | first 10 game minutes | 0.585 | 0.1154 | -0.4696 | 9/5 |
| core_gap_p50_s | first 10 game minutes | 0.75 | 0.2462 | -0.5038 | 9/5 |
| core_gap_p90_s | first 10 game minutes | 2.376 | 1.438 | -0.9375 | 9/5 |
| core_gap_p99_s | first 10 game minutes | 5.543 | 3.504 | -2.039 | 9/5 |
| core_gap_max_s | first 10 game minutes | 8.61 | 5.892 | -2.718 | 9/5 |
| simultaneous_core_gap_fraction | first 10 game minutes | 0.3845 | 0.003221 | -0.3813 | 9/5 |
| core_gap_cv | first 10 game minutes | 1.373 | 1.34 | -0.03314 | 9/5 |
| core_gap_burstiness | first 10 game minutes | 0.1572 | 0.1453 | -0.01194 | 9/5 |
| command_silence_ge5s_time_fraction | first 10 game minutes | 0.08325 | 0.03148 | -0.05177 | 9/5 |
| command_silence_ge10s_time_fraction | first 10 game minutes | 0 | 0 | 0 | 9/5 |
| core_count_5s_cv | first 10 game minutes | 0.624 | 0.4836 | -0.1404 | 9/5 |
| peak_5s_nominal_cpm | first 10 game minutes | 264 | 228 | -36 | 9/5 |
| empty_5s_bin_fraction | first 10 game minutes | 0.0125 | 0.02778 | 0.01528 | 9/5 |
| core_type_entropy_bits | first 10 game minutes | 0.8426 | 0.9085 | 0.06599 | 9/5 |
| core_category_entropy_bits | first 10 game minutes | 0.8426 | 0.8728 | 0.03021 | 9/5 |
| core_type_transition_entropy_bits | first 10 game minutes | 0.7316 | 0.7358 | 0.004248 | 9/5 |
| core_type_switch_fraction | first 10 game minutes | 0.2085 | 0.2124 | 0.003872 | 9/5 |
| core_category_switch_fraction | first 10 game minutes | 0.2085 | 0.2109 | 0.002342 | 9/5 |
| core_same_type_triplet_fraction | first 10 game minutes | 0.6675 | 0.6879 | 0.02043 | 9/5 |
| coordinate_coverage | first 10 game minutes | 1 | 1 | 0 | 9/5 |
| destination_jump_diagonal_p50 | first 10 game minutes | 0.01441 | 0.01434 | -6.516e-05 | 9/5 |
| destination_jump_diagonal_p90 | first 10 game minutes | 0.1382 | 0.1588 | 0.02067 | 9/5 |
| destination_jump_ge_quarter_fraction | first 10 game minutes | 0.02013 | 0.04452 | 0.02439 | 9/5 |
| destination_entropy_4x4_bits | first 10 game minutes | 1.75 | 2.478 | 0.7281 | 9/5 |
| destination_cell_switch_fraction | first 10 game minutes | 0.2315 | 0.2633 | 0.03183 | 9/5 |
| rapid_destination_repeat_fraction | first 10 game minutes | 0.2296 | 0.4258 | 0.1962 | 9/5 |
| dedup_core_cpm | first 10 game minutes | 56.85 | 63.21 | 6.356 | 9/5 |
| move_order_commands | first 10 game minutes | 474.5 | 585 | 110.5 | 9/5 |
| explicit_actor_commands | first 10 game minutes | 155 | 197 | 42 | 9/5 |
| explicit_actor_coverage | first 10 game minutes | 0.3359 | 0.3499 | 0.01399 | 9/5 |
| actor_pair_count | first 10 game minutes | 53 | 103 | 50 | 9/5 |
| same_actor_pair_count | first 10 game minutes | 0.5 | 18 | 17.5 | 9/5 |
| actor_group_size_median | first 10 game minutes | 1 | 1 | 0 | 9/5 |
| actor_group_size_p90 | first 10 game minutes | 4.75 | 4 | -0.75 | 9/5 |
| actor_group_ge10_fraction | first 10 game minutes | 0 | 0.004348 | 0.004348 | 9/5 |
| actor_group_change_fraction | first 10 game minutes | 0.9931 | 0.8462 | -0.1469 | 9/5 |
| actor_overlap_jaccard_median | first 10 game minutes | 0 | 0 | 0 | 9/5 |
| same_actor_gap_nominal_median_s | first 10 game minutes | 1.155 | 0.2385 | -0.9165 | 4/5 |
| same_actor_recommand_under1s_fraction | first 10 game minutes | 0.5 | 1 | 0.5 | 4/5 |
| commanded_actor_ids | first 10 game minutes | 32.5 | 29 | -3.5 | 9/5 |
| valid_target_order_fraction | first 10 game minutes | 1 | 1 | 0 | 9/5 |
| distinct_order_target_ids | first 10 game minutes | 29 | 32 | 3 | 9/5 |
| distinct_building_type_ids | first 10 game minutes | 5 | 5 | 0 | 9/5 |
| distinct_research_type_ids | first 10 game minutes | 1 | 2 | 1 | 9/5 |
| positive_de_queue_commands | first 10 game minutes | — | 23 | — | 0/5 |
| requested_queue_unit_type_ids | first 10 game minutes | — | 2 | — | 0/5 |
| explicitly_commanded_production_building_ids | first 10 game minutes | — | 2 | — | 0/5 |
| production_command_revisit_nominal_median_s | first 10 game minutes | — | 14.42 | — | 0/5 |
| positive_queue_amount_mean | first 10 game minutes | — | 1 | — | 0/5 |
| build_commands_nominal_min | first 10 game minutes | 2.025 | 1.859 | -0.166 | 9/5 |
| wall_commands_nominal_min | first 10 game minutes | 0 | 0.676 | 0.676 | 9/5 |
| research_commands_nominal_min | first 10 game minutes | 0.45 | 0.338 | -0.112 | 9/5 |
| market_commands_nominal_min | first 10 game minutes | 0 | 0 | 0 | 9/5 |
| legacy_command_class_entropy_bits | first 10 game minutes | — | — | — | 0/0 |
| legacy_switches_per_100_commands | first 10 game minutes | — | — | — | 0/0 |
| legacy_core_silence_over5s_fraction | first 10 game minutes | — | — | — | 0/0 |
| legacy_peak_10s_nominal_cpm | first 10 game minutes | — | — | — | 0/0 |
| legacy_move_share | first 10 game minutes | — | — | — | 0/0 |
| legacy_planning_command_share | first 10 game minutes | — | — | — | 0/0 |
| legacy_queue_batch_mean | first 10 game minutes | — | — | — | 0/0 |
| legacy_queue_batch_gt1_fraction | first 10 game minutes | — | — | — | 0/0 |
| legacy_duration_game_min | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_0_5 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_5_10 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_10_15 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_15_20 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_10_20 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_reclick_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_dedup_open_cpm | first 10 game minutes | — | — | — | 0/0 |
| tatoh_reclick_whole | first 10 game minutes | — | — | — | 0/0 |
| tatoh_dedup_whole_cpm | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p50_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p90_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p99_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p99_10_20 | first 10 game minutes | — | — | — | 0/0 |
| feudal_request_game_s | first 10 game minutes | 499.3 | 400.6 | -98.67 | 5/5 |
| castle_request_game_s | first 10 game minutes | — | — | — | 0/0 |
| imperial_request_game_s | first 10 game minutes | — | — | — | 0/0 |
| all_recorded_cpm | whole available replay | 68.68 | 141.1 | 72.45 | 9/5 |
| core_cpm | whole available replay | 62.22 | 103.3 | 41.1 | 9/5 |
| noncore_action_fraction | whole available replay | 0.09404 | 0.321 | 0.227 | 9/5 |
| first_core_command_nominal_s | whole available replay | 1.98 | 0.8 | -1.18 | 9/5 |
| core_gap_p10_s | whole available replay | 0.6 | 0.1154 | -0.4846 | 9/5 |
| core_gap_p50_s | whole available replay | 0.87 | 0.2385 | -0.6315 | 9/5 |
| core_gap_p90_s | whole available replay | 3.54 | 1.446 | -2.094 | 9/5 |
| core_gap_p99_s | whole available replay | 8.885 | 4.085 | -4.8 | 9/5 |
| core_gap_max_s | whole available replay | 20.16 | 12.26 | -7.898 | 9/5 |
| simultaneous_core_gap_fraction | whole available replay | 0.3683 | 0.003802 | -0.3645 | 9/5 |
| core_gap_cv | whole available replay | 1.601 | 1.444 | -0.1563 | 9/5 |
| core_gap_burstiness | whole available replay | 0.2309 | 0.1818 | -0.04914 | 9/5 |
| command_silence_ge5s_time_fraction | whole available replay | 0.2454 | 0.04863 | -0.1967 | 9/5 |
| command_silence_ge10s_time_fraction | whole available replay | 0.05156 | 0.01475 | -0.03681 | 9/5 |
| core_count_5s_cv | whole available replay | 0.7617 | 0.5644 | -0.1972 | 9/5 |
| peak_5s_nominal_cpm | whole available replay | 276 | 372 | 96 | 9/5 |
| empty_5s_bin_fraction | whole available replay | 0.07803 | 0.02 | -0.05803 | 9/5 |
| core_type_entropy_bits | whole available replay | 1.399 | 1.117 | -0.2825 | 9/5 |
| core_category_entropy_bits | whole available replay | 1.391 | 1.089 | -0.3011 | 9/5 |
| core_type_transition_entropy_bits | whole available replay | 1.096 | 0.8861 | -0.2096 | 9/5 |
| core_type_switch_fraction | whole available replay | 0.2921 | 0.227 | -0.06516 | 9/5 |
| core_category_switch_fraction | whole available replay | 0.2909 | 0.227 | -0.06399 | 9/5 |
| core_same_type_triplet_fraction | whole available replay | 0.5447 | 0.6315 | 0.08678 | 9/5 |
| coordinate_coverage | whole available replay | 1 | 1 | 0 | 9/5 |
| destination_jump_diagonal_p50 | whole available replay | 0.01144 | 0.01105 | -0.0003936 | 9/5 |
| destination_jump_diagonal_p90 | whole available replay | 0.1436 | 0.1568 | 0.01321 | 9/5 |
| destination_jump_ge_quarter_fraction | whole available replay | 0.048 | 0.06142 | 0.01343 | 9/5 |
| destination_entropy_4x4_bits | whole available replay | 2.598 | 2.833 | 0.235 | 9/5 |
| destination_cell_switch_fraction | whole available replay | 0.1974 | 0.2383 | 0.04088 | 9/5 |
| rapid_destination_repeat_fraction | whole available replay | 0.2774 | 0.4626 | 0.1852 | 9/5 |
| dedup_core_cpm | whole available replay | 47.66 | 58.28 | 10.61 | 9/5 |
| move_order_commands | whole available replay | 1750 | 1620 | -129.5 | 9/5 |
| explicit_actor_commands | whole available replay | 572.5 | 636 | 63.5 | 9/5 |
| explicit_actor_coverage | whole available replay | 0.3193 | 0.3903 | 0.07109 | 9/5 |
| actor_pair_count | whole available replay | 219.5 | 303 | 83.5 | 9/5 |
| same_actor_pair_count | whole available replay | 6 | 90 | 84 | 9/5 |
| actor_group_size_median | whole available replay | 3 | 1 | -2 | 9/5 |
| actor_group_size_p90 | whole available replay | 18 | 8 | -10 | 9/5 |
| actor_group_ge10_fraction | whole available replay | 0.1654 | 0.05975 | -0.1057 | 9/5 |
| actor_group_change_fraction | whole available replay | 0.9665 | 0.7588 | -0.2077 | 9/5 |
| actor_overlap_jaccard_median | whole available replay | 0 | 0 | 0 | 9/5 |
| same_actor_gap_nominal_median_s | whole available replay | 1.605 | 0.2385 | -1.367 | 9/5 |
| same_actor_recommand_under1s_fraction | whole available replay | 0.275 | 0.9 | 0.625 | 9/5 |
| commanded_actor_ids | whole available replay | 294 | 97 | -197 | 9/5 |
| valid_target_order_fraction | whole available replay | 0.9423 | 1 | 0.05769 | 9/5 |
| distinct_order_target_ids | whole available replay | 167 | 115 | -52 | 9/5 |
| distinct_building_type_ids | whole available replay | 13 | 12 | -1 | 9/5 |
| distinct_research_type_ids | whole available replay | 32 | 9 | -23 | 9/5 |
| positive_de_queue_commands | whole available replay | — | 118 | — | 0/5 |
| requested_queue_unit_type_ids | whole available replay | — | 4 | — | 0/5 |
| explicitly_commanded_production_building_ids | whole available replay | — | 4 | — | 0/5 |
| production_command_revisit_nominal_median_s | whole available replay | — | 10.58 | — | 0/5 |
| positive_queue_amount_mean | whole available replay | — | 1 | — | 0/5 |
| build_commands_nominal_min | whole available replay | 4.471 | 2.751 | -1.721 | 9/5 |
| wall_commands_nominal_min | whole available replay | 0.1233 | 0.2974 | 0.1741 | 9/5 |
| research_commands_nominal_min | whole available replay | 2.157 | 0.5948 | -1.562 | 9/5 |
| market_commands_nominal_min | whole available replay | 0.4 | 0.3608 | -0.03911 | 9/5 |
| legacy_command_class_entropy_bits | whole available replay | 1.391 | 1.089 | -0.3011 | 9/5 |
| legacy_switches_per_100_commands | whole available replay | 29.09 | 22.7 | -6.399 | 9/5 |
| legacy_core_silence_over5s_fraction | whole available replay | 0.2454 | 0.04863 | -0.1967 | 9/5 |
| legacy_peak_10s_nominal_cpm | whole available replay | 279 | 324 | 45 | 9/5 |
| legacy_move_share | whole available replay | 0.6898 | 0.7474 | 0.0576 | 9/5 |
| legacy_planning_command_share | whole available replay | 0.1284 | 0.04126 | -0.08711 | 9/5 |
| legacy_queue_batch_mean | whole available replay | — | 1 | — | 0/5 |
| legacy_queue_batch_gt1_fraction | whole available replay | — | 0 | — | 0/5 |
| legacy_duration_game_min | whole available replay | 56.42 | 28.1 | -28.32 | 9/5 |
| tatoh_cpm_0_5 | whole available replay | — | — | — | 0/0 |
| tatoh_cpm_5_10 | whole available replay | — | — | — | 0/0 |
| tatoh_cpm_10_15 | whole available replay | — | — | — | 0/0 |
| tatoh_cpm_15_20 | whole available replay | — | — | — | 0/0 |
| tatoh_cpm_10_20 | whole available replay | — | — | — | 0/0 |
| tatoh_reclick_open | whole available replay | — | — | — | 0/0 |
| tatoh_dedup_open_cpm | whole available replay | — | — | — | 0/0 |
| tatoh_reclick_whole | whole available replay | — | — | — | 0/0 |
| tatoh_dedup_whole_cpm | whole available replay | — | — | — | 0/0 |
| tatoh_gap_p50_open | whole available replay | — | — | — | 0/0 |
| tatoh_gap_p90_open | whole available replay | — | — | — | 0/0 |
| tatoh_gap_p99_open | whole available replay | — | — | — | 0/0 |
| tatoh_gap_p99_10_20 | whole available replay | — | — | — | 0/0 |
| feudal_request_game_s | whole available replay | 659.1 | 400.6 | -258.4 | 9/5 |
| castle_request_game_s | whole available replay | 901.5 | 1066 | 164.8 | 9/4 |
| imperial_request_game_s | whole available replay | 2103 | 2008 | -95.56 | 9/1 |

### DauT DE control

| Trait | Window | Early | Late | Δ | Games early/late |
|---|---|---:|---:|---:|---:|
| all_recorded_cpm | first 10 game minutes | 100.9 | 99.71 | -1.183 | 9/5 |
| core_cpm | first 10 game minutes | 95.82 | 84.84 | -10.99 | 9/5 |
| noncore_action_fraction | first 10 game minutes | 0.05025 | 0.1678 | 0.1175 | 9/5 |
| first_core_command_nominal_s | first 10 game minutes | 1.415 | 1.292 | -0.1231 | 9/5 |
| core_gap_p10_s | first 10 game minutes | 0.116 | 0.1231 | 0.007101 | 9/5 |
| core_gap_p50_s | first 10 game minutes | 0.3645 | 0.3615 | -0.002959 | 9/5 |
| core_gap_p90_s | first 10 game minutes | 1.505 | 1.596 | 0.09107 | 9/5 |
| core_gap_p99_s | first 10 game minutes | 3.865 | 3.872 | 0.007059 | 9/5 |
| core_gap_max_s | first 10 game minutes | 5.849 | 6.492 | 0.6438 | 9/5 |
| simultaneous_core_gap_fraction | first 10 game minutes | 0 | 0 | 0 | 9/5 |
| core_gap_cv | first 10 game minutes | 1.204 | 1.17 | -0.03411 | 9/5 |
| core_gap_burstiness | first 10 game minutes | 0.09276 | 0.07851 | -0.01426 | 9/5 |
| command_silence_ge5s_time_fraction | first 10 game minutes | 0.01667 | 0.04062 | 0.02396 | 9/5 |
| command_silence_ge10s_time_fraction | first 10 game minutes | 0 | 0 | 0 | 9/5 |
| core_count_5s_cv | first 10 game minutes | 0.4514 | 0.433 | -0.01839 | 9/5 |
| peak_5s_nominal_cpm | first 10 game minutes | 216 | 192 | -24 | 9/5 |
| empty_5s_bin_fraction | first 10 game minutes | 0.01389 | 0.01389 | 0 | 9/5 |
| core_type_entropy_bits | first 10 game minutes | 0.7223 | 0.7914 | 0.06913 | 9/5 |
| core_category_entropy_bits | first 10 game minutes | 0.7005 | 0.7562 | 0.05571 | 9/5 |
| core_type_transition_entropy_bits | first 10 game minutes | 0.6035 | 0.6833 | 0.07978 | 9/5 |
| core_type_switch_fraction | first 10 game minutes | 0.1721 | 0.1959 | 0.02382 | 9/5 |
| core_category_switch_fraction | first 10 game minutes | 0.1688 | 0.1956 | 0.02674 | 9/5 |
| core_same_type_triplet_fraction | first 10 game minutes | 0.7382 | 0.7057 | -0.03254 | 9/5 |
| coordinate_coverage | first 10 game minutes | 1 | 1 | 0 | 9/5 |
| destination_jump_diagonal_p50 | first 10 game minutes | 0.02123 | 0.02483 | 0.003593 | 9/5 |
| destination_jump_diagonal_p90 | first 10 game minutes | 0.2008 | 0.1634 | -0.03746 | 9/5 |
| destination_jump_ge_quarter_fraction | first 10 game minutes | 0.07752 | 0.05123 | -0.02629 | 9/5 |
| destination_entropy_4x4_bits | first 10 game minutes | 2.875 | 2.683 | -0.1922 | 9/5 |
| destination_cell_switch_fraction | first 10 game minutes | 0.3262 | 0.3102 | -0.01603 | 9/5 |
| rapid_destination_repeat_fraction | first 10 game minutes | 0.284 | 0.2801 | -0.003875 | 9/5 |
| dedup_core_cpm | first 10 game minutes | 67.26 | 61.69 | -5.577 | 9/5 |
| move_order_commands | first 10 game minutes | 544 | 489 | -55 | 9/5 |
| explicit_actor_commands | first 10 game minutes | 178 | 188 | 10 | 9/5 |
| explicit_actor_coverage | first 10 game minutes | 0.3327 | 0.4023 | 0.06958 | 9/5 |
| actor_pair_count | first 10 game minutes | 68 | 86 | 18 | 9/5 |
| same_actor_pair_count | first 10 game minutes | 0 | 8 | 8 | 9/5 |
| actor_group_size_median | first 10 game minutes | 1 | 1 | 0 | 9/5 |
| actor_group_size_p90 | first 10 game minutes | 2 | 3 | 1 | 9/5 |
| actor_group_ge10_fraction | first 10 game minutes | 0 | 0.005319 | 0.005319 | 9/5 |
| actor_group_change_fraction | first 10 game minutes | 1 | 0.8939 | -0.1061 | 9/5 |
| actor_overlap_jaccard_median | first 10 game minutes | 0 | 0 | 0 | 9/5 |
| same_actor_gap_nominal_median_s | first 10 game minutes | 1.342 | 0.3615 | -0.9805 | 1/5 |
| same_actor_recommand_under1s_fraction | first 10 game minutes | 0 | 0.875 | 0.875 | 1/5 |
| commanded_actor_ids | first 10 game minutes | 28 | 30 | 2 | 9/5 |
| valid_target_order_fraction | first 10 game minutes | 1 | 1 | 0 | 9/5 |
| distinct_order_target_ids | first 10 game minutes | 28 | 30 | 2 | 9/5 |
| distinct_building_type_ids | first 10 game minutes | 5 | 6 | 1 | 9/5 |
| distinct_research_type_ids | first 10 game minutes | 2 | 2 | 0 | 9/5 |
| positive_de_queue_commands | first 10 game minutes | 30 | 23 | -7 | 9/5 |
| requested_queue_unit_type_ids | first 10 game minutes | 2 | 2 | 0 | 9/5 |
| explicitly_commanded_production_building_ids | first 10 game minutes | 2 | 2 | 0 | 9/5 |
| production_command_revisit_nominal_median_s | first 10 game minutes | 9.864 | 14.55 | 4.682 | 9/5 |
| positive_queue_amount_mean | first 10 game minutes | 1.032 | 1.13 | 0.09818 | 9/5 |
| build_commands_nominal_min | first 10 game minutes | 2.028 | 1.859 | -0.169 | 9/5 |
| wall_commands_nominal_min | first 10 game minutes | 0.507 | 0.507 | 0 | 9/5 |
| research_commands_nominal_min | first 10 game minutes | 0.338 | 0.338 | 0 | 9/5 |
| market_commands_nominal_min | first 10 game minutes | 0 | 0 | 0 | 9/5 |
| legacy_command_class_entropy_bits | first 10 game minutes | — | — | — | 0/0 |
| legacy_switches_per_100_commands | first 10 game minutes | — | — | — | 0/0 |
| legacy_core_silence_over5s_fraction | first 10 game minutes | — | — | — | 0/0 |
| legacy_peak_10s_nominal_cpm | first 10 game minutes | — | — | — | 0/0 |
| legacy_move_share | first 10 game minutes | — | — | — | 0/0 |
| legacy_planning_command_share | first 10 game minutes | — | — | — | 0/0 |
| legacy_queue_batch_mean | first 10 game minutes | — | — | — | 0/0 |
| legacy_queue_batch_gt1_fraction | first 10 game minutes | — | — | — | 0/0 |
| legacy_duration_game_min | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_0_5 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_5_10 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_10_15 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_15_20 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_10_20 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_reclick_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_dedup_open_cpm | first 10 game minutes | — | — | — | 0/0 |
| tatoh_reclick_whole | first 10 game minutes | — | — | — | 0/0 |
| tatoh_dedup_whole_cpm | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p50_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p90_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p99_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p99_10_20 | first 10 game minutes | — | — | — | 0/0 |
| feudal_request_game_s | first 10 game minutes | 453.8 | 403.7 | -50.1 | 8/5 |
| castle_request_game_s | first 10 game minutes | — | — | — | 0/0 |
| imperial_request_game_s | first 10 game minutes | — | — | — | 0/0 |
| all_recorded_cpm | whole available replay | 88.6 | 106.7 | 18.1 | 9/5 |
| core_cpm | whole available replay | 74.72 | 86.12 | 11.4 | 9/5 |
| noncore_action_fraction | whole available replay | 0.1237 | 0.1893 | 0.06565 | 9/5 |
| first_core_command_nominal_s | whole available replay | 1.415 | 1.292 | -0.1231 | 9/5 |
| core_gap_p10_s | whole available replay | 0.116 | 0.1231 | 0.007101 | 9/5 |
| core_gap_p50_s | whole available replay | 0.4805 | 0.3615 | -0.1189 | 9/5 |
| core_gap_p90_s | whole available replay | 1.955 | 1.677 | -0.2781 | 9/5 |
| core_gap_p99_s | whole available replay | 4.644 | 4.333 | -0.3107 | 9/5 |
| core_gap_max_s | whole available replay | 9.991 | 11.06 | 1.071 | 9/5 |
| simultaneous_core_gap_fraction | whole available replay | 0.00116 | 0.0008319 | -0.0003281 | 9/5 |
| core_gap_cv | whole available replay | 1.214 | 1.301 | 0.0875 | 9/5 |
| core_gap_burstiness | whole available replay | 0.09653 | 0.1309 | 0.03435 | 9/5 |
| command_silence_ge5s_time_fraction | whole available replay | 0.06222 | 0.05773 | -0.004484 | 9/5 |
| command_silence_ge10s_time_fraction | whole available replay | 0.005616 | 0.01867 | 0.01305 | 9/5 |
| core_count_5s_cv | whole available replay | 0.5106 | 0.5206 | 0.009992 | 9/5 |
| peak_5s_nominal_cpm | whole available replay | 216 | 216 | 0 | 9/5 |
| empty_5s_bin_fraction | whole available replay | 0.01773 | 0.01702 | -0.0007092 | 9/5 |
| core_type_entropy_bits | whole available replay | 1.241 | 0.9916 | -0.2496 | 9/5 |
| core_category_entropy_bits | whole available replay | 1.221 | 0.9761 | -0.2451 | 9/5 |
| core_type_transition_entropy_bits | whole available replay | 1.062 | 0.9083 | -0.1537 | 9/5 |
| core_type_switch_fraction | whole available replay | 0.2889 | 0.2533 | -0.0356 | 9/5 |
| core_category_switch_fraction | whole available replay | 0.2871 | 0.2525 | -0.03463 | 9/5 |
| core_same_type_triplet_fraction | whole available replay | 0.5517 | 0.6187 | 0.06696 | 9/5 |
| coordinate_coverage | whole available replay | 1 | 1 | 0 | 9/5 |
| destination_jump_diagonal_p50 | whole available replay | 0.02419 | 0.01987 | -0.004318 | 9/5 |
| destination_jump_diagonal_p90 | whole available replay | 0.2291 | 0.1679 | -0.06127 | 9/5 |
| destination_jump_ge_quarter_fraction | whole available replay | 0.08948 | 0.06245 | -0.02703 | 9/5 |
| destination_entropy_4x4_bits | whole available replay | 3.313 | 3.047 | -0.2655 | 9/5 |
| destination_cell_switch_fraction | whole available replay | 0.3347 | 0.2684 | -0.06633 | 9/5 |
| rapid_destination_repeat_fraction | whole available replay | 0.2897 | 0.3197 | 0.02994 | 9/5 |
| dedup_core_cpm | whole available replay | 55.47 | 62.5 | 7.031 | 9/5 |
| move_order_commands | whole available replay | 1736 | 1268 | -468 | 9/5 |
| explicit_actor_commands | whole available replay | 657 | 565 | -92 | 9/5 |
| explicit_actor_coverage | whole available replay | 0.3981 | 0.4117 | 0.01354 | 9/5 |
| actor_pair_count | whole available replay | 280 | 248 | -32 | 9/5 |
| same_actor_pair_count | whole available replay | 4 | 45 | 41 | 9/5 |
| actor_group_size_median | whole available replay | 2 | 2 | 0 | 9/5 |
| actor_group_size_p90 | whole available replay | 9 | 8 | -1 | 9/5 |
| actor_group_ge10_fraction | whole available replay | 0.09331 | 0.05364 | -0.03967 | 9/5 |
| actor_group_change_fraction | whole available replay | 0.9896 | 0.8171 | -0.1725 | 9/5 |
| actor_overlap_jaccard_median | whole available replay | 0 | 0 | 0 | 9/5 |
| same_actor_gap_nominal_median_s | whole available replay | 1.323 | 0.3615 | -0.9615 | 9/5 |
| same_actor_recommand_under1s_fraction | whole available replay | 0.3333 | 0.7708 | 0.4375 | 9/5 |
| commanded_actor_ids | whole available replay | 230 | 77 | -153 | 9/5 |
| valid_target_order_fraction | whole available replay | 1 | 1 | 0 | 9/5 |
| distinct_order_target_ids | whole available replay | 172 | 106 | -66 | 9/5 |
| distinct_building_type_ids | whole available replay | 16 | 12 | -4 | 9/5 |
| distinct_research_type_ids | whole available replay | 23 | 12 | -11 | 9/5 |
| positive_de_queue_commands | whole available replay | 307 | 84 | -223 | 9/5 |
| requested_queue_unit_type_ids | whole available replay | 8 | 5 | -3 | 9/5 |
| explicitly_commanded_production_building_ids | whole available replay | 20 | 5 | -15 | 9/5 |
| production_command_revisit_nominal_median_s | whole available replay | 6.578 | 12.86 | 6.284 | 9/5 |
| positive_queue_amount_mean | whole available replay | 1.007 | 1.04 | 0.03301 | 9/5 |
| build_commands_nominal_min | whole available replay | 5.75 | 3.223 | -2.527 | 9/5 |
| wall_commands_nominal_min | whole available replay | 0.3369 | 0.4381 | 0.1013 | 9/5 |
| research_commands_nominal_min | whole available replay | 1.31 | 0.9306 | -0.3796 | 9/5 |
| market_commands_nominal_min | whole available replay | 0.4538 | 0.3286 | -0.1252 | 9/5 |
| legacy_command_class_entropy_bits | whole available replay | 1.221 | 0.9761 | -0.2451 | 9/5 |
| legacy_switches_per_100_commands | whole available replay | 28.71 | 25.25 | -3.463 | 9/5 |
| legacy_core_silence_over5s_fraction | whole available replay | 0.06222 | 0.05773 | -0.004484 | 9/5 |
| legacy_peak_10s_nominal_cpm | whole available replay | 210 | 216 | 6 | 9/5 |
| legacy_move_share | whole available replay | 0.7434 | 0.7799 | 0.03657 | 9/5 |
| legacy_planning_command_share | whole available replay | 0.1101 | 0.05015 | -0.05993 | 9/5 |
| legacy_queue_batch_mean | whole available replay | 1.007 | 1.04 | 0.03301 | 9/5 |
| legacy_queue_batch_gt1_fraction | whole available replay | 0.006329 | 0.01333 | 0.007004 | 9/5 |
| legacy_duration_game_min | whole available replay | 44.9 | 25.17 | -19.72 | 9/5 |
| tatoh_cpm_0_5 | whole available replay | — | — | — | 0/0 |
| tatoh_cpm_5_10 | whole available replay | — | — | — | 0/0 |
| tatoh_cpm_10_15 | whole available replay | — | — | — | 0/0 |
| tatoh_cpm_15_20 | whole available replay | — | — | — | 0/0 |
| tatoh_cpm_10_20 | whole available replay | — | — | — | 0/0 |
| tatoh_reclick_open | whole available replay | — | — | — | 0/0 |
| tatoh_dedup_open_cpm | whole available replay | — | — | — | 0/0 |
| tatoh_reclick_whole | whole available replay | — | — | — | 0/0 |
| tatoh_dedup_whole_cpm | whole available replay | — | — | — | 0/0 |
| tatoh_gap_p50_open | whole available replay | — | — | — | 0/0 |
| tatoh_gap_p90_open | whole available replay | — | — | — | 0/0 |
| tatoh_gap_p99_open | whole available replay | — | — | — | 0/0 |
| tatoh_gap_p99_10_20 | whole available replay | — | — | — | 0/0 |
| feudal_request_game_s | whole available replay | 479.6 | 403.7 | -75.95 | 9/5 |
| castle_request_game_s | whole available replay | 1094 | 1210 | 115.7 | 9/5 |
| imperial_request_game_s | whole available replay | 2166 | 1929 | -236.6 | 6/1 |

### TheViper DE control

| Trait | Window | Early | Late | Δ | Games early/late |
|---|---|---:|---:|---:|---:|
| all_recorded_cpm | first 10 game minutes | 117 | 138.2 | 21.21 | 5/5 |
| core_cpm | first 10 game minutes | 111.4 | 102.8 | -8.619 | 5/5 |
| noncore_action_fraction | first 10 game minutes | 0.04647 | 0.2319 | 0.1854 | 5/5 |
| first_core_command_nominal_s | first 10 game minutes | 0.9231 | 0.8 | -0.1231 | 5/5 |
| core_gap_p10_s | first 10 game minutes | 0.1163 | 0.1154 | -0.0008876 | 5/5 |
| core_gap_p50_s | first 10 game minutes | 0.2426 | 0.2462 | 0.00355 | 5/5 |
| core_gap_p90_s | first 10 game minutes | 1.325 | 1.438 | 0.1136 | 5/5 |
| core_gap_p99_s | first 10 game minutes | 3.552 | 3.504 | -0.04822 | 5/5 |
| core_gap_max_s | first 10 game minutes | 7.249 | 5.892 | -1.357 | 5/5 |
| simultaneous_core_gap_fraction | first 10 game minutes | 0.01524 | 0.003221 | -0.01201 | 5/5 |
| core_gap_cv | first 10 game minutes | 1.368 | 1.34 | -0.02751 | 5/5 |
| core_gap_burstiness | first 10 game minutes | 0.1552 | 0.1453 | -0.00993 | 5/5 |
| command_silence_ge5s_time_fraction | first 10 game minutes | 0.03637 | 0.03148 | -0.004885 | 5/5 |
| command_silence_ge10s_time_fraction | first 10 game minutes | 0 | 0 | 0 | 5/5 |
| core_count_5s_cv | first 10 game minutes | 0.4652 | 0.4836 | 0.01841 | 5/5 |
| peak_5s_nominal_cpm | first 10 game minutes | 270 | 228 | -42 | 5/5 |
| empty_5s_bin_fraction | first 10 game minutes | 0.02083 | 0.02778 | 0.006944 | 5/5 |
| core_type_entropy_bits | first 10 game minutes | 0.9468 | 0.9085 | -0.03827 | 5/5 |
| core_category_entropy_bits | first 10 game minutes | 0.9327 | 0.8728 | -0.05994 | 5/5 |
| core_type_transition_entropy_bits | first 10 game minutes | 0.745 | 0.7358 | -0.009174 | 5/5 |
| core_type_switch_fraction | first 10 game minutes | 0.1939 | 0.2124 | 0.01854 | 5/5 |
| core_category_switch_fraction | first 10 game minutes | 0.1939 | 0.2109 | 0.01701 | 5/5 |
| core_same_type_triplet_fraction | first 10 game minutes | 0.6793 | 0.6879 | 0.008615 | 5/5 |
| coordinate_coverage | first 10 game minutes | 1 | 1 | 0 | 5/5 |
| destination_jump_diagonal_p50 | first 10 game minutes | 0.01735 | 0.01434 | -0.003014 | 5/5 |
| destination_jump_diagonal_p90 | first 10 game minutes | 0.2295 | 0.1588 | -0.07069 | 5/5 |
| destination_jump_ge_quarter_fraction | first 10 game minutes | 0.09346 | 0.04452 | -0.04894 | 5/5 |
| destination_entropy_4x4_bits | first 10 game minutes | 2.842 | 2.478 | -0.3638 | 5/5 |
| destination_cell_switch_fraction | first 10 game minutes | 0.2942 | 0.2633 | -0.03088 | 5/5 |
| rapid_destination_repeat_fraction | first 10 game minutes | 0.4159 | 0.4258 | 0.009877 | 5/5 |
| dedup_core_cpm | first 10 game minutes | 71.06 | 63.21 | -7.859 | 5/5 |
| move_order_commands | first 10 game minutes | 632 | 585 | -47 | 5/5 |
| explicit_actor_commands | first 10 game minutes | 191.5 | 197 | 5.5 | 5/5 |
| explicit_actor_coverage | first 10 game minutes | 0.3057 | 0.3499 | 0.04426 | 5/5 |
| actor_pair_count | first 10 game minutes | 45 | 103 | 58 | 5/5 |
| same_actor_pair_count | first 10 game minutes | 0 | 18 | 18 | 5/5 |
| actor_group_size_median | first 10 game minutes | 1 | 1 | 0 | 5/5 |
| actor_group_size_p90 | first 10 game minutes | 3 | 4 | 1 | 5/5 |
| actor_group_ge10_fraction | first 10 game minutes | 0 | 0.004348 | 0.004348 | 5/5 |
| actor_group_change_fraction | first 10 game minutes | 1 | 0.8462 | -0.1538 | 5/5 |
| actor_overlap_jaccard_median | first 10 game minutes | 0 | 0 | 0 | 5/5 |
| same_actor_gap_nominal_median_s | first 10 game minutes | — | 0.2385 | — | 0/5 |
| same_actor_recommand_under1s_fraction | first 10 game minutes | — | 1 | — | 0/5 |
| commanded_actor_ids | first 10 game minutes | 34 | 29 | -5 | 5/5 |
| valid_target_order_fraction | first 10 game minutes | 1 | 1 | 0 | 5/5 |
| distinct_order_target_ids | first 10 game minutes | 42 | 32 | -10 | 5/5 |
| distinct_building_type_ids | first 10 game minutes | 5 | 5 | 0 | 5/5 |
| distinct_research_type_ids | first 10 game minutes | 2 | 2 | 0 | 5/5 |
| positive_de_queue_commands | first 10 game minutes | 33 | 23 | -10 | 5/5 |
| requested_queue_unit_type_ids | first 10 game minutes | 3 | 2 | -1 | 5/5 |
| explicitly_commanded_production_building_ids | first 10 game minutes | 2 | 2 | 0 | 5/5 |
| production_command_revisit_nominal_median_s | first 10 game minutes | 13.79 | 14.42 | 0.629 | 5/5 |
| positive_queue_amount_mean | first 10 game minutes | 1 | 1 | 0 | 5/5 |
| build_commands_nominal_min | first 10 game minutes | 1.859 | 1.859 | 0 | 5/5 |
| wall_commands_nominal_min | first 10 game minutes | 0.676 | 0.676 | 0 | 5/5 |
| research_commands_nominal_min | first 10 game minutes | 0.507 | 0.338 | -0.169 | 5/5 |
| market_commands_nominal_min | first 10 game minutes | 0 | 0 | 0 | 5/5 |
| legacy_command_class_entropy_bits | first 10 game minutes | — | — | — | 0/0 |
| legacy_switches_per_100_commands | first 10 game minutes | — | — | — | 0/0 |
| legacy_core_silence_over5s_fraction | first 10 game minutes | — | — | — | 0/0 |
| legacy_peak_10s_nominal_cpm | first 10 game minutes | — | — | — | 0/0 |
| legacy_move_share | first 10 game minutes | — | — | — | 0/0 |
| legacy_planning_command_share | first 10 game minutes | — | — | — | 0/0 |
| legacy_queue_batch_mean | first 10 game minutes | — | — | — | 0/0 |
| legacy_queue_batch_gt1_fraction | first 10 game minutes | — | — | — | 0/0 |
| legacy_duration_game_min | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_0_5 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_5_10 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_10_15 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_15_20 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_10_20 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_reclick_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_dedup_open_cpm | first 10 game minutes | — | — | — | 0/0 |
| tatoh_reclick_whole | first 10 game minutes | — | — | — | 0/0 |
| tatoh_dedup_whole_cpm | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p50_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p90_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p99_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p99_10_20 | first 10 game minutes | — | — | — | 0/0 |
| feudal_request_game_s | first 10 game minutes | 458.3 | 400.6 | -57.61 | 4/5 |
| castle_request_game_s | first 10 game minutes | — | — | — | 0/0 |
| imperial_request_game_s | first 10 game minutes | — | — | — | 0/0 |
| all_recorded_cpm | whole available replay | 115.5 | 141.1 | 25.61 | 5/5 |
| core_cpm | whole available replay | 91.37 | 103.3 | 11.95 | 5/5 |
| noncore_action_fraction | whole available replay | 0.1967 | 0.321 | 0.1243 | 5/5 |
| first_core_command_nominal_s | whole available replay | 0.9231 | 0.8 | -0.1231 | 5/5 |
| core_gap_p10_s | whole available replay | 0.1172 | 0.1154 | -0.001775 | 5/5 |
| core_gap_p50_s | whole available replay | 0.2982 | 0.2385 | -0.05976 | 5/5 |
| core_gap_p90_s | whole available replay | 1.658 | 1.446 | -0.2119 | 5/5 |
| core_gap_p99_s | whole available replay | 4.212 | 4.085 | -0.127 | 5/5 |
| core_gap_max_s | whole available replay | 12.2 | 12.26 | 0.05799 | 5/5 |
| simultaneous_core_gap_fraction | whole available replay | 0.01574 | 0.003802 | -0.01194 | 5/5 |
| core_gap_cv | whole available replay | 1.439 | 1.444 | 0.005762 | 5/5 |
| core_gap_burstiness | whole available replay | 0.1798 | 0.1818 | 0.001933 | 5/5 |
| command_silence_ge5s_time_fraction | whole available replay | 0.07306 | 0.04863 | -0.02443 | 5/5 |
| command_silence_ge10s_time_fraction | whole available replay | 0.008774 | 0.01475 | 0.005972 | 5/5 |
| core_count_5s_cv | whole available replay | 0.5487 | 0.5644 | 0.01572 | 5/5 |
| peak_5s_nominal_cpm | whole available replay | 282 | 372 | 90 | 5/5 |
| empty_5s_bin_fraction | whole available replay | 0.01695 | 0.02 | 0.003051 | 5/5 |
| core_type_entropy_bits | whole available replay | 1.456 | 1.117 | -0.339 | 5/5 |
| core_category_entropy_bits | whole available replay | 1.421 | 1.089 | -0.3313 | 5/5 |
| core_type_transition_entropy_bits | whole available replay | 1.118 | 0.8861 | -0.2323 | 5/5 |
| core_type_switch_fraction | whole available replay | 0.2777 | 0.227 | -0.05075 | 5/5 |
| core_category_switch_fraction | whole available replay | 0.2773 | 0.227 | -0.05034 | 5/5 |
| core_same_type_triplet_fraction | whole available replay | 0.5441 | 0.6315 | 0.08741 | 5/5 |
| coordinate_coverage | whole available replay | 1 | 1 | 0 | 5/5 |
| destination_jump_diagonal_p50 | whole available replay | 0.0205 | 0.01105 | -0.009451 | 5/5 |
| destination_jump_diagonal_p90 | whole available replay | 0.2457 | 0.1568 | -0.08889 | 5/5 |
| destination_jump_ge_quarter_fraction | whole available replay | 0.09944 | 0.06142 | -0.03801 | 5/5 |
| destination_entropy_4x4_bits | whole available replay | 3.491 | 2.833 | -0.6575 | 5/5 |
| destination_cell_switch_fraction | whole available replay | 0.3133 | 0.2383 | -0.07504 | 5/5 |
| rapid_destination_repeat_fraction | whole available replay | 0.3907 | 0.4626 | 0.07192 | 5/5 |
| dedup_core_cpm | whole available replay | 60.56 | 58.28 | -2.281 | 5/5 |
| move_order_commands | whole available replay | 2140 | 1620 | -520 | 5/5 |
| explicit_actor_commands | whole available replay | 743 | 636 | -107 | 5/5 |
| explicit_actor_coverage | whole available replay | 0.3294 | 0.3903 | 0.0609 | 5/5 |
| actor_pair_count | whole available replay | 225 | 303 | 78 | 5/5 |
| same_actor_pair_count | whole available replay | 4 | 90 | 86 | 5/5 |
| actor_group_size_median | whole available replay | 1 | 1 | 0 | 5/5 |
| actor_group_size_p90 | whole available replay | 6 | 8 | 2 | 5/5 |
| actor_group_ge10_fraction | whole available replay | 0.04701 | 0.05975 | 0.01273 | 5/5 |
| actor_group_change_fraction | whole available replay | 0.9774 | 0.7588 | -0.2185 | 5/5 |
| actor_overlap_jaccard_median | whole available replay | 0 | 0 | 0 | 5/5 |
| same_actor_gap_nominal_median_s | whole available replay | 1.323 | 0.2385 | -1.085 | 5/5 |
| same_actor_recommand_under1s_fraction | whole available replay | 0.5 | 0.9 | 0.4 | 5/5 |
| commanded_actor_ids | whole available replay | 250.5 | 97 | -153.5 | 5/5 |
| valid_target_order_fraction | whole available replay | 1 | 1 | 0 | 5/5 |
| distinct_order_target_ids | whole available replay | 226 | 115 | -111 | 5/5 |
| distinct_building_type_ids | whole available replay | 16 | 12 | -4 | 5/5 |
| distinct_research_type_ids | whole available replay | 36 | 9 | -27 | 5/5 |
| positive_de_queue_commands | whole available replay | 353 | 118 | -235 | 5/5 |
| requested_queue_unit_type_ids | whole available replay | 13 | 4 | -9 | 5/5 |
| explicitly_commanded_production_building_ids | whole available replay | 28 | 4 | -24 | 5/5 |
| production_command_revisit_nominal_median_s | whole available replay | 0.1314 | 10.58 | 10.45 | 5/5 |
| positive_queue_amount_mean | whole available replay | 1 | 1 | 0 | 5/5 |
| build_commands_nominal_min | whole available replay | 6.441 | 2.751 | -3.69 | 5/5 |
| wall_commands_nominal_min | whole available replay | 0.5094 | 0.2974 | -0.212 | 5/5 |
| research_commands_nominal_min | whole available replay | 2.739 | 0.5948 | -2.144 | 5/5 |
| market_commands_nominal_min | whole available replay | 0.5093 | 0.3608 | -0.1484 | 5/5 |
| legacy_command_class_entropy_bits | whole available replay | 1.421 | 1.089 | -0.3313 | 5/5 |
| legacy_switches_per_100_commands | whole available replay | 27.73 | 22.7 | -5.034 | 5/5 |
| legacy_core_silence_over5s_fraction | whole available replay | 0.07306 | 0.04863 | -0.02443 | 5/5 |
| legacy_peak_10s_nominal_cpm | whole available replay | 252 | 324 | 72 | 5/5 |
| legacy_move_share | whole available replay | 0.6585 | 0.7474 | 0.08885 | 5/5 |
| legacy_planning_command_share | whole available replay | 0.1112 | 0.04126 | -0.06997 | 5/5 |
| legacy_queue_batch_mean | whole available replay | 1 | 1 | 0 | 5/5 |
| legacy_queue_batch_gt1_fraction | whole available replay | 0 | 0 | 0 | 5/5 |
| legacy_duration_game_min | whole available replay | 49.16 | 28.1 | -21.06 | 5/5 |
| tatoh_cpm_0_5 | whole available replay | — | — | — | 0/0 |
| tatoh_cpm_5_10 | whole available replay | — | — | — | 0/0 |
| tatoh_cpm_10_15 | whole available replay | — | — | — | 0/0 |
| tatoh_cpm_15_20 | whole available replay | — | — | — | 0/0 |
| tatoh_cpm_10_20 | whole available replay | — | — | — | 0/0 |
| tatoh_reclick_open | whole available replay | — | — | — | 0/0 |
| tatoh_dedup_open_cpm | whole available replay | — | — | — | 0/0 |
| tatoh_reclick_whole | whole available replay | — | — | — | 0/0 |
| tatoh_dedup_whole_cpm | whole available replay | — | — | — | 0/0 |
| tatoh_gap_p50_open | whole available replay | — | — | — | 0/0 |
| tatoh_gap_p90_open | whole available replay | — | — | — | 0/0 |
| tatoh_gap_p99_open | whole available replay | — | — | — | 0/0 |
| tatoh_gap_p99_10_20 | whole available replay | — | — | — | 0/0 |
| feudal_request_game_s | whole available replay | 462.5 | 400.6 | -61.81 | 5/5 |
| castle_request_game_s | whole available replay | 957.5 | 1066 | 108.7 | 4/4 |
| imperial_request_game_s | whole available replay | 1959 | 2008 | 48.56 | 4/1 |

### TaToH tournament control

| Trait | Window | Early | Late | Δ | Games early/late |
|---|---|---:|---:|---:|---:|
| all_recorded_cpm | first 10 game minutes | 106.1 | 130.5 | 24.34 | 1/13 |
| core_cpm | first 10 game minutes | 101.2 | 102.8 | 1.521 | 1/13 |
| noncore_action_fraction | first 10 game minutes | 0.04618 | 0.2091 | 0.1629 | 1/13 |
| first_core_command_nominal_s | first 10 game minutes | 0.9231 | 0.8 | -0.1231 | 1/13 |
| core_gap_p10_s | first 10 game minutes | 0.116 | 0.1154 | -0.0005917 | 1/13 |
| core_gap_p50_s | first 10 game minutes | 0.2485 | 0.2462 | -0.002367 | 1/13 |
| core_gap_p90_s | first 10 game minutes | 1.412 | 1.446 | 0.03456 | 1/13 |
| core_gap_p99_s | first 10 game minutes | 2.953 | 3.304 | 0.3503 | 1/13 |
| core_gap_max_s | first 10 game minutes | 10.11 | 6.131 | -3.976 | 1/13 |
| simultaneous_core_gap_fraction | first 10 game minutes | 0.005017 | 0.001665 | -0.003352 | 1/13 |
| core_gap_cv | first 10 game minutes | 1.371 | 1.31 | -0.06165 | 1/13 |
| core_gap_burstiness | first 10 game minutes | 0.1566 | 0.1341 | -0.02251 | 1/13 |
| command_silence_ge5s_time_fraction | first 10 game minutes | 0.06211 | 0.03386 | -0.02825 | 1/13 |
| command_silence_ge10s_time_fraction | first 10 game minutes | 0.02847 | 0 | -0.02847 | 1/13 |
| core_count_5s_cv | first 10 game minutes | 0.4923 | 0.4837 | -0.008545 | 1/13 |
| peak_5s_nominal_cpm | first 10 game minutes | 216 | 240 | 24 | 1/13 |
| empty_5s_bin_fraction | first 10 game minutes | 0.02778 | 0.01389 | -0.01389 | 1/13 |
| core_type_entropy_bits | first 10 game minutes | 0.8647 | 1.041 | 0.1764 | 1/13 |
| core_category_entropy_bits | first 10 game minutes | 0.8243 | 0.9977 | 0.1734 | 1/13 |
| core_type_transition_entropy_bits | first 10 game minutes | 0.7392 | 0.8183 | 0.07912 | 1/13 |
| core_type_switch_fraction | first 10 game minutes | 0.2007 | 0.2191 | 0.01844 | 1/13 |
| core_category_switch_fraction | first 10 game minutes | 0.2007 | 0.2191 | 0.01844 | 1/13 |
| core_same_type_triplet_fraction | first 10 game minutes | 0.6851 | 0.6436 | -0.04153 | 1/13 |
| coordinate_coverage | first 10 game minutes | 1 | 1 | 0 | 1/13 |
| destination_jump_diagonal_p50 | first 10 game minutes | 0.02595 | 0.01993 | -0.006024 | 1/13 |
| destination_jump_diagonal_p90 | first 10 game minutes | 0.171 | 0.2295 | 0.05845 | 1/13 |
| destination_jump_ge_quarter_fraction | first 10 game minutes | 0.03846 | 0.0885 | 0.05003 | 1/13 |
| destination_entropy_4x4_bits | first 10 game minutes | 2.415 | 2.68 | 0.2644 | 1/13 |
| destination_cell_switch_fraction | first 10 game minutes | 0.2832 | 0.2846 | 0.001336 | 1/13 |
| rapid_destination_repeat_fraction | first 10 game minutes | 0.3409 | 0.37 | 0.02909 | 1/13 |
| dedup_core_cpm | first 10 game minutes | 68.28 | 60.33 | -7.943 | 1/13 |
| move_order_commands | first 10 game minutes | 573 | 577 | 4 | 1/13 |
| explicit_actor_commands | first 10 game minutes | 231 | 215 | -16 | 1/13 |
| explicit_actor_coverage | first 10 game minutes | 0.4031 | 0.3804 | -0.02271 | 1/13 |
| actor_pair_count | first 10 game minutes | 96 | 111 | 15 | 1/13 |
| same_actor_pair_count | first 10 game minutes | 0 | 24 | 24 | 1/13 |
| actor_group_size_median | first 10 game minutes | 1 | 1 | 0 | 1/13 |
| actor_group_size_p90 | first 10 game minutes | 2 | 3 | 1 | 1/13 |
| actor_group_ge10_fraction | first 10 game minutes | 0 | 0.004566 | 0.004566 | 1/13 |
| actor_group_change_fraction | first 10 game minutes | 1 | 0.75 | -0.25 | 1/13 |
| actor_overlap_jaccard_median | first 10 game minutes | 0 | 0 | 0 | 1/13 |
| same_actor_gap_nominal_median_s | first 10 game minutes | — | 0.2385 | — | 0/13 |
| same_actor_recommand_under1s_fraction | first 10 game minutes | — | 0.9231 | — | 0/13 |
| commanded_actor_ids | first 10 game minutes | 34 | 33 | -1 | 1/13 |
| valid_target_order_fraction | first 10 game minutes | 1 | 1 | 0 | 1/13 |
| distinct_order_target_ids | first 10 game minutes | 30 | 37 | 7 | 1/13 |
| distinct_building_type_ids | first 10 game minutes | 5 | 7 | 2 | 1/13 |
| distinct_research_type_ids | first 10 game minutes | 0 | 4 | 4 | 1/13 |
| positive_de_queue_commands | first 10 game minutes | 29 | 26 | -3 | 1/13 |
| requested_queue_unit_type_ids | first 10 game minutes | 2 | 2 | 0 | 1/13 |
| explicitly_commanded_production_building_ids | first 10 game minutes | 2 | 2 | 0 | 1/13 |
| production_command_revisit_nominal_median_s | first 10 game minutes | 13.04 | 13.7 | 0.6609 | 1/13 |
| positive_queue_amount_mean | first 10 game minutes | 1.103 | 1 | -0.1034 | 1/13 |
| build_commands_nominal_min | first 10 game minutes | 2.873 | 2.535 | -0.338 | 1/13 |
| wall_commands_nominal_min | first 10 game minutes | 1.521 | 1.521 | 0 | 1/13 |
| research_commands_nominal_min | first 10 game minutes | 0 | 0.845 | 0.845 | 1/13 |
| market_commands_nominal_min | first 10 game minutes | 0 | 0 | 0 | 1/13 |
| legacy_command_class_entropy_bits | first 10 game minutes | — | — | — | 0/0 |
| legacy_switches_per_100_commands | first 10 game minutes | — | — | — | 0/0 |
| legacy_core_silence_over5s_fraction | first 10 game minutes | — | — | — | 0/0 |
| legacy_peak_10s_nominal_cpm | first 10 game minutes | — | — | — | 0/0 |
| legacy_move_share | first 10 game minutes | — | — | — | 0/0 |
| legacy_planning_command_share | first 10 game minutes | — | — | — | 0/0 |
| legacy_queue_batch_mean | first 10 game minutes | — | — | — | 0/0 |
| legacy_queue_batch_gt1_fraction | first 10 game minutes | — | — | — | 0/0 |
| legacy_duration_game_min | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_0_5 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_5_10 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_10_15 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_15_20 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_10_20 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_reclick_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_dedup_open_cpm | first 10 game minutes | — | — | — | 0/0 |
| tatoh_reclick_whole | first 10 game minutes | — | — | — | 0/0 |
| tatoh_dedup_whole_cpm | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p50_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p90_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p99_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p99_10_20 | first 10 game minutes | — | — | — | 0/0 |
| feudal_request_game_s | first 10 game minutes | — | 275.9 | — | 0/12 |
| castle_request_game_s | first 10 game minutes | — | 515.9 | — | 0/4 |
| imperial_request_game_s | first 10 game minutes | — | — | — | 0/0 |
| all_recorded_cpm | whole available replay | 98.11 | 118.1 | 20.01 | 1/13 |
| core_cpm | whole available replay | 77.26 | 85.58 | 8.323 | 1/13 |
| noncore_action_fraction | whole available replay | 0.2125 | 0.2755 | 0.0629 | 1/13 |
| first_core_command_nominal_s | whole available replay | 0.9231 | 0.8 | -0.1231 | 1/13 |
| core_gap_p10_s | whole available replay | 0.116 | 0.1154 | -0.0005917 | 1/13 |
| core_gap_p50_s | whole available replay | 0.3645 | 0.3615 | -0.002959 | 1/13 |
| core_gap_p90_s | whole available replay | 2.048 | 1.8 | -0.2478 | 1/13 |
| core_gap_p99_s | whole available replay | 5.103 | 4.685 | -0.4183 | 1/13 |
| core_gap_max_s | whole available replay | 10.11 | 9.492 | -0.6142 | 1/13 |
| simultaneous_core_gap_fraction | whole available replay | 0.006616 | 0.002407 | -0.004209 | 1/13 |
| core_gap_cv | whole available replay | 1.387 | 1.367 | -0.01955 | 1/13 |
| core_gap_burstiness | whole available replay | 0.1621 | 0.1552 | -0.00692 | 1/13 |
| command_silence_ge5s_time_fraction | whole available replay | 0.09392 | 0.06348 | -0.03044 | 1/13 |
| command_silence_ge10s_time_fraction | whole available replay | 0.008198 | 0 | -0.008198 | 1/13 |
| core_count_5s_cv | whole available replay | 0.5602 | 0.5371 | -0.02304 | 1/13 |
| peak_5s_nominal_cpm | whole available replay | 228 | 276 | 48 | 1/13 |
| empty_5s_bin_fraction | whole available replay | 0.02834 | 0.01515 | -0.01319 | 1/13 |
| core_type_entropy_bits | whole available replay | 1.596 | 1.353 | -0.2433 | 1/13 |
| core_category_entropy_bits | whole available replay | 1.567 | 1.313 | -0.2534 | 1/13 |
| core_type_transition_entropy_bits | whole available replay | 1.279 | 1.191 | -0.08803 | 1/13 |
| core_type_switch_fraction | whole available replay | 0.3267 | 0.3287 | 0.001998 | 1/13 |
| core_category_switch_fraction | whole available replay | 0.3267 | 0.3258 | -0.000869 | 1/13 |
| core_same_type_triplet_fraction | whole available replay | 0.4869 | 0.4957 | 0.008777 | 1/13 |
| coordinate_coverage | whole available replay | 1 | 1 | 0 | 1/13 |
| destination_jump_diagonal_p50 | whole available replay | 0.02801 | 0.02534 | -0.002666 | 1/13 |
| destination_jump_diagonal_p90 | whole available replay | 0.2564 | 0.2485 | -0.007887 | 1/13 |
| destination_jump_ge_quarter_fraction | whole available replay | 0.1027 | 0.09925 | -0.003471 | 1/13 |
| destination_entropy_4x4_bits | whole available replay | 3.448 | 3.361 | -0.08709 | 1/13 |
| destination_cell_switch_fraction | whole available replay | 0.329 | 0.3107 | -0.01827 | 1/13 |
| rapid_destination_repeat_fraction | whole available replay | 0.3074 | 0.308 | 0.0006043 | 1/13 |
| dedup_core_cpm | whole available replay | 57.16 | 59.23 | 2.069 | 1/13 |
| move_order_commands | whole available replay | 2688 | 1605 | -1083 | 1/13 |
| explicit_actor_commands | whole available replay | 1103 | 795 | -308 | 1/13 |
| explicit_actor_coverage | whole available replay | 0.4103 | 0.4822 | 0.07186 | 1/13 |
| actor_pair_count | whole available replay | 435 | 456 | 21 | 1/13 |
| same_actor_pair_count | whole available replay | 7 | 115.5 | 108.5 | 1/13 |
| actor_group_size_median | whole available replay | 2 | 2 | 0 | 1/13 |
| actor_group_size_p90 | whole available replay | 12 | 8 | -4 | 1/13 |
| actor_group_ge10_fraction | whole available replay | 0.1378 | 0.08435 | -0.05346 | 1/13 |
| actor_group_change_fraction | whole available replay | 0.9839 | 0.7325 | -0.2515 | 1/13 |
| actor_overlap_jaccard_median | whole available replay | 0 | 0 | 0 | 1/13 |
| same_actor_gap_nominal_median_s | whole available replay | 1.11 | 0.1243 | -0.9858 | 1/13 |
| same_actor_recommand_under1s_fraction | whole available replay | 0.4286 | 0.9032 | 0.4747 | 1/13 |
| commanded_actor_ids | whole available replay | 686 | 160 | -526 | 1/13 |
| valid_target_order_fraction | whole available replay | 1 | 1 | 0 | 1/13 |
| distinct_order_target_ids | whole available replay | 317 | 156 | -161 | 1/13 |
| distinct_building_type_ids | whole available replay | 16 | 14 | -2 | 1/13 |
| distinct_research_type_ids | whole available replay | 45 | 21 | -24 | 1/13 |
| positive_de_queue_commands | whole available replay | 820 | 225 | -595 | 1/13 |
| requested_queue_unit_type_ids | whole available replay | 14 | 8 | -6 | 1/13 |
| explicitly_commanded_production_building_ids | whole available replay | 55 | 12 | -43 | 1/13 |
| production_command_revisit_nominal_median_s | whole available replay | 0.2485 | 6.737 | 6.489 | 1/13 |
| positive_queue_amount_mean | whole available replay | 1.059 | 1 | -0.05854 | 1/13 |
| build_commands_nominal_min | whole available replay | 7.008 | 4.945 | -2.063 | 1/13 |
| wall_commands_nominal_min | whole available replay | 0.2433 | 0.6178 | 0.3744 | 1/13 |
| research_commands_nominal_min | whole available replay | 1.484 | 1.536 | 0.05211 | 1/13 |
| market_commands_nominal_min | whole available replay | 1.971 | 0.5428 | -1.428 | 1/13 |
| legacy_command_class_entropy_bits | whole available replay | 1.567 | 1.313 | -0.2534 | 1/13 |
| legacy_switches_per_100_commands | whole available replay | 32.67 | 32.58 | -0.0869 | 1/13 |
| legacy_core_silence_over5s_fraction | whole available replay | — | — | — | 0/0 |
| legacy_peak_10s_nominal_cpm | whole available replay | — | — | — | 0/0 |
| legacy_move_share | whole available replay | — | — | — | 0/0 |
| legacy_planning_command_share | whole available replay | 0.1386 | 0.08977 | -0.04882 | 1/13 |
| legacy_queue_batch_mean | whole available replay | 1.059 | 1 | -0.05854 | 1/13 |
| legacy_queue_batch_gt1_fraction | whole available replay | — | — | — | 0/0 |
| legacy_duration_game_min | whole available replay | 69.45 | 34.8 | -34.65 | 1/13 |
| tatoh_cpm_0_5 | whole available replay | 122.7 | 106.5 | -16.22 | 1/13 |
| tatoh_cpm_5_10 | whole available replay | 79.77 | 90.58 | 10.82 | 1/13 |
| tatoh_cpm_10_15 | whole available replay | 71.99 | 80.11 | 8.112 | 1/11 |
| tatoh_cpm_15_20 | whole available replay | 88.22 | 79.43 | -8.788 | 1/11 |
| tatoh_cpm_10_20 | whole available replay | 80.11 | 80.11 | 0 | 1/11 |
| tatoh_reclick_open | whole available replay | 0.3255 | 0.3469 | 0.02133 | 1/13 |
| tatoh_dedup_open_cpm | whole available replay | 68.28 | 60.33 | -7.943 | 1/13 |
| tatoh_reclick_whole | whole available replay | 0.2601 | 0.2777 | 0.01763 | 1/13 |
| tatoh_dedup_whole_cpm | whole available replay | 57.17 | 59.21 | 2.039 | 1/13 |
| tatoh_gap_p50_open | whole available replay | 0.2485 | 0.2462 | -0.002367 | 1/13 |
| tatoh_gap_p90_open | whole available replay | 1.377 | 1.446 | 0.06935 | 1/13 |
| tatoh_gap_p99_open | whole available replay | 2.943 | 3.304 | 0.3607 | 1/13 |
| tatoh_gap_p99_10_20 | whole available replay | 5.969 | 4.634 | -1.335 | 1/11 |
| feudal_request_game_s | whole available replay | 686.5 | 275.9 | -410.6 | 1/12 |
| castle_request_game_s | whole available replay | 888.9 | 756.3 | -132.6 | 1/11 |
| imperial_request_game_s | whole available replay | 1964 | 2107 | 143.8 | 1/6 |

### TaToH earliest verified to ranked

| Trait | Window | Early | Late | Δ | Games early/late |
|---|---|---:|---:|---:|---:|
| all_recorded_cpm | first 10 game minutes | 106.1 | 134.2 | 28.05 | 1/39 |
| core_cpm | first 10 game minutes | 101.2 | 108 | 6.76 | 1/39 |
| noncore_action_fraction | first 10 game minutes | 0.04618 | 0.1952 | 0.149 | 1/39 |
| first_core_command_nominal_s | first 10 game minutes | 0.9231 | 1.046 | 0.1231 | 1/39 |
| core_gap_p10_s | first 10 game minutes | 0.116 | 0.1154 | -0.0005917 | 1/39 |
| core_gap_p50_s | first 10 game minutes | 0.2485 | 0.2385 | -0.01006 | 1/39 |
| core_gap_p90_s | first 10 game minutes | 1.412 | 1.446 | 0.03456 | 1/39 |
| core_gap_p99_s | first 10 game minutes | 2.953 | 3.455 | 0.5012 | 1/39 |
| core_gap_max_s | first 10 game minutes | 10.11 | 6.246 | -3.86 | 1/39 |
| simultaneous_core_gap_fraction | first 10 game minutes | 0.005017 | 0.03605 | 0.03103 | 1/39 |
| core_gap_cv | first 10 game minutes | 1.371 | 1.324 | -0.04707 | 1/39 |
| core_gap_burstiness | first 10 game minutes | 0.1566 | 0.1396 | -0.01708 | 1/39 |
| command_silence_ge5s_time_fraction | first 10 game minutes | 0.06211 | 0.01998 | -0.04214 | 1/39 |
| command_silence_ge10s_time_fraction | first 10 game minutes | 0.02847 | 0 | -0.02847 | 1/39 |
| core_count_5s_cv | first 10 game minutes | 0.4923 | 0.4257 | -0.06655 | 1/39 |
| peak_5s_nominal_cpm | first 10 game minutes | 216 | 228 | 12 | 1/39 |
| empty_5s_bin_fraction | first 10 game minutes | 0.02778 | 0.01389 | -0.01389 | 1/39 |
| core_type_entropy_bits | first 10 game minutes | 0.8647 | 0.6992 | -0.1655 | 1/39 |
| core_category_entropy_bits | first 10 game minutes | 0.8243 | 0.6841 | -0.1402 | 1/39 |
| core_type_transition_entropy_bits | first 10 game minutes | 0.7392 | 0.5952 | -0.144 | 1/39 |
| core_type_switch_fraction | first 10 game minutes | 0.2007 | 0.1583 | -0.04234 | 1/39 |
| core_category_switch_fraction | first 10 game minutes | 0.2007 | 0.1583 | -0.04234 | 1/39 |
| core_same_type_triplet_fraction | first 10 game minutes | 0.6851 | 0.7399 | 0.05482 | 1/39 |
| coordinate_coverage | first 10 game minutes | 1 | 1 | 0 | 1/39 |
| destination_jump_diagonal_p50 | first 10 game minutes | 0.02595 | 0.01585 | -0.0101 | 1/39 |
| destination_jump_diagonal_p90 | first 10 game minutes | 0.171 | 0.1626 | -0.008387 | 1/39 |
| destination_jump_ge_quarter_fraction | first 10 game minutes | 0.03846 | 0.05424 | 0.01578 | 1/39 |
| destination_entropy_4x4_bits | first 10 game minutes | 2.415 | 2.54 | 0.1242 | 1/39 |
| destination_cell_switch_fraction | first 10 game minutes | 0.2832 | 0.2556 | -0.02758 | 1/39 |
| rapid_destination_repeat_fraction | first 10 game minutes | 0.3409 | 0.419 | 0.07814 | 1/39 |
| dedup_core_cpm | first 10 game minutes | 68.28 | 66.42 | -1.859 | 1/39 |
| move_order_commands | first 10 game minutes | 573 | 624 | 51 | 1/39 |
| explicit_actor_commands | first 10 game minutes | 231 | 199 | -32 | 1/39 |
| explicit_actor_coverage | first 10 game minutes | 0.4031 | 0.3169 | -0.08627 | 1/39 |
| actor_pair_count | first 10 game minutes | 96 | 87 | -9 | 1/39 |
| same_actor_pair_count | first 10 game minutes | 0 | 13 | 13 | 1/39 |
| actor_group_size_median | first 10 game minutes | 1 | 1 | 0 | 1/39 |
| actor_group_size_p90 | first 10 game minutes | 2 | 3 | 1 | 1/39 |
| actor_group_ge10_fraction | first 10 game minutes | 0 | 0 | 0 | 1/39 |
| actor_group_change_fraction | first 10 game minutes | 1 | 0.8434 | -0.1566 | 1/39 |
| actor_overlap_jaccard_median | first 10 game minutes | 0 | 0 | 0 | 1/39 |
| same_actor_gap_nominal_median_s | first 10 game minutes | — | 0.2385 | — | 0/39 |
| same_actor_recommand_under1s_fraction | first 10 game minutes | — | 0.9231 | — | 0/39 |
| commanded_actor_ids | first 10 game minutes | 34 | 32 | -2 | 1/39 |
| valid_target_order_fraction | first 10 game minutes | 1 | 1 | 0 | 1/39 |
| distinct_order_target_ids | first 10 game minutes | 30 | 28 | -2 | 1/39 |
| distinct_building_type_ids | first 10 game minutes | 5 | 5 | 0 | 1/39 |
| distinct_research_type_ids | first 10 game minutes | 0 | 3 | 3 | 1/39 |
| positive_de_queue_commands | first 10 game minutes | 29 | 23 | -6 | 1/39 |
| requested_queue_unit_type_ids | first 10 game minutes | 2 | 2 | 0 | 1/39 |
| explicitly_commanded_production_building_ids | first 10 game minutes | 2 | 2 | 0 | 1/39 |
| production_command_revisit_nominal_median_s | first 10 game minutes | 13.04 | 13.44 | 0.3994 | 1/39 |
| positive_queue_amount_mean | first 10 game minutes | 1.103 | 1.222 | 0.1188 | 1/39 |
| build_commands_nominal_min | first 10 game minutes | 2.873 | 1.69 | -1.183 | 1/39 |
| wall_commands_nominal_min | first 10 game minutes | 1.521 | 0 | -1.521 | 1/39 |
| research_commands_nominal_min | first 10 game minutes | 0 | 0.507 | 0.507 | 1/39 |
| market_commands_nominal_min | first 10 game minutes | 0 | 0 | 0 | 1/39 |
| legacy_command_class_entropy_bits | first 10 game minutes | — | — | — | 0/0 |
| legacy_switches_per_100_commands | first 10 game minutes | — | — | — | 0/0 |
| legacy_core_silence_over5s_fraction | first 10 game minutes | — | — | — | 0/0 |
| legacy_peak_10s_nominal_cpm | first 10 game minutes | — | — | — | 0/0 |
| legacy_move_share | first 10 game minutes | — | — | — | 0/0 |
| legacy_planning_command_share | first 10 game minutes | — | — | — | 0/0 |
| legacy_queue_batch_mean | first 10 game minutes | — | — | — | 0/0 |
| legacy_queue_batch_gt1_fraction | first 10 game minutes | — | — | — | 0/0 |
| legacy_duration_game_min | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_0_5 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_5_10 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_10_15 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_15_20 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_10_20 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_reclick_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_dedup_open_cpm | first 10 game minutes | — | — | — | 0/0 |
| tatoh_reclick_whole | first 10 game minutes | — | — | — | 0/0 |
| tatoh_dedup_whole_cpm | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p50_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p90_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p99_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p99_10_20 | first 10 game minutes | — | — | — | 0/0 |
| feudal_request_game_s | first 10 game minutes | — | 436.6 | — | 0/37 |
| castle_request_game_s | first 10 game minutes | — | 532.6 | — | 0/2 |
| imperial_request_game_s | first 10 game minutes | — | — | — | 0/0 |
| all_recorded_cpm | whole available replay | 98.11 | 125.8 | 27.67 | 1/40 |
| core_cpm | whole available replay | 77.26 | 91.02 | 13.76 | 1/40 |
| noncore_action_fraction | whole available replay | 0.2125 | 0.2698 | 0.05726 | 1/40 |
| first_core_command_nominal_s | whole available replay | 0.9231 | 1.046 | 0.1231 | 1/40 |
| core_gap_p10_s | whole available replay | 0.116 | 0.1154 | -0.0005917 | 1/40 |
| core_gap_p50_s | whole available replay | 0.3645 | 0.3615 | -0.002959 | 1/40 |
| core_gap_p90_s | whole available replay | 2.048 | 1.685 | -0.3632 | 1/40 |
| core_gap_p99_s | whole available replay | 5.103 | 4.085 | -1.018 | 1/40 |
| core_gap_max_s | whole available replay | 10.11 | 9.977 | -0.1296 | 1/40 |
| simultaneous_core_gap_fraction | whole available replay | 0.006616 | 0.03263 | 0.02601 | 1/40 |
| core_gap_cv | whole available replay | 1.387 | 1.34 | -0.04646 | 1/40 |
| core_gap_burstiness | whole available replay | 0.1621 | 0.1455 | -0.01663 | 1/40 |
| command_silence_ge5s_time_fraction | whole available replay | 0.09392 | 0.05577 | -0.03815 | 1/40 |
| command_silence_ge10s_time_fraction | whole available replay | 0.008198 | 0.005523 | -0.002674 | 1/40 |
| core_count_5s_cv | whole available replay | 0.5602 | 0.503 | -0.05719 | 1/40 |
| peak_5s_nominal_cpm | whole available replay | 228 | 240 | 12 | 1/40 |
| empty_5s_bin_fraction | whole available replay | 0.02834 | 0.01579 | -0.01255 | 1/40 |
| core_type_entropy_bits | whole available replay | 1.596 | 1.169 | -0.4275 | 1/40 |
| core_category_entropy_bits | whole available replay | 1.567 | 1.13 | -0.4366 | 1/40 |
| core_type_transition_entropy_bits | whole available replay | 1.279 | 1.001 | -0.2779 | 1/40 |
| core_type_switch_fraction | whole available replay | 0.3267 | 0.2737 | -0.05303 | 1/40 |
| core_category_switch_fraction | whole available replay | 0.3267 | 0.2737 | -0.05303 | 1/40 |
| core_same_type_triplet_fraction | whole available replay | 0.4869 | 0.5809 | 0.09395 | 1/40 |
| coordinate_coverage | whole available replay | 1 | 1 | 0 | 1/40 |
| destination_jump_diagonal_p50 | whole available replay | 0.02801 | 0.02284 | -0.005175 | 1/40 |
| destination_jump_diagonal_p90 | whole available replay | 0.2564 | 0.2324 | -0.02395 | 1/40 |
| destination_jump_ge_quarter_fraction | whole available replay | 0.1027 | 0.09255 | -0.01017 | 1/40 |
| destination_entropy_4x4_bits | whole available replay | 3.448 | 3.072 | -0.3761 | 1/40 |
| destination_cell_switch_fraction | whole available replay | 0.329 | 0.3059 | -0.02306 | 1/40 |
| rapid_destination_repeat_fraction | whole available replay | 0.3074 | 0.3244 | 0.01703 | 1/40 |
| dedup_core_cpm | whole available replay | 57.16 | 62.44 | 5.283 | 1/40 |
| move_order_commands | whole available replay | 2688 | 1503 | -1185 | 1/40 |
| explicit_actor_commands | whole available replay | 1103 | 598 | -505 | 1/40 |
| explicit_actor_coverage | whole available replay | 0.4103 | 0.4217 | 0.01132 | 1/40 |
| actor_pair_count | whole available replay | 435 | 307 | -128 | 1/40 |
| same_actor_pair_count | whole available replay | 7 | 80 | 73 | 1/40 |
| actor_group_size_median | whole available replay | 2 | 1 | -1 | 1/40 |
| actor_group_size_p90 | whole available replay | 12 | 7 | -5 | 1/40 |
| actor_group_ge10_fraction | whole available replay | 0.1378 | 0.02514 | -0.1127 | 1/40 |
| actor_group_change_fraction | whole available replay | 0.9839 | 0.7654 | -0.2185 | 1/40 |
| actor_overlap_jaccard_median | whole available replay | 0 | 0 | 0 | 1/40 |
| same_actor_gap_nominal_median_s | whole available replay | 1.11 | 0.2385 | -0.8716 | 1/40 |
| same_actor_recommand_under1s_fraction | whole available replay | 0.4286 | 0.8851 | 0.4566 | 1/40 |
| commanded_actor_ids | whole available replay | 686 | 105 | -581 | 1/40 |
| valid_target_order_fraction | whole available replay | 1 | 1 | 0 | 1/40 |
| distinct_order_target_ids | whole available replay | 317 | 111 | -206 | 1/40 |
| distinct_building_type_ids | whole available replay | 16 | 15 | -1 | 1/40 |
| distinct_research_type_ids | whole available replay | 45 | 16 | -29 | 1/40 |
| positive_de_queue_commands | whole available replay | 820 | 139 | -681 | 1/40 |
| requested_queue_unit_type_ids | whole available replay | 14 | 7 | -7 | 1/40 |
| explicitly_commanded_production_building_ids | whole available replay | 55 | 12 | -43 | 1/40 |
| production_command_revisit_nominal_median_s | whole available replay | 0.2485 | 6.52 | 6.272 | 1/40 |
| positive_queue_amount_mean | whole available replay | 1.059 | 1.046 | -0.01245 | 1/40 |
| build_commands_nominal_min | whole available replay | 7.008 | 4.282 | -2.726 | 1/40 |
| wall_commands_nominal_min | whole available replay | 0.2433 | 0.4608 | 0.2175 | 1/40 |
| research_commands_nominal_min | whole available replay | 1.484 | 1.15 | -0.3342 | 1/40 |
| market_commands_nominal_min | whole available replay | 1.971 | 0.4228 | -1.548 | 1/40 |
| legacy_command_class_entropy_bits | whole available replay | 1.567 | 1.13 | -0.4366 | 1/40 |
| legacy_switches_per_100_commands | whole available replay | 32.67 | 27.37 | -5.303 | 1/40 |
| legacy_core_silence_over5s_fraction | whole available replay | — | — | — | 0/0 |
| legacy_peak_10s_nominal_cpm | whole available replay | — | — | — | 0/0 |
| legacy_move_share | whole available replay | — | — | — | 0/0 |
| legacy_planning_command_share | whole available replay | 0.1386 | 0.07728 | -0.0613 | 1/40 |
| legacy_queue_batch_mean | whole available replay | 1.059 | 1.046 | -0.01245 | 1/40 |
| legacy_queue_batch_gt1_fraction | whole available replay | — | — | — | 0/0 |
| legacy_duration_game_min | whole available replay | 69.45 | 29.56 | -39.89 | 1/40 |
| tatoh_cpm_0_5 | whole available replay | 122.7 | 122 | -0.676 | 1/40 |
| tatoh_cpm_5_10 | whole available replay | 79.77 | 97.01 | 17.24 | 1/39 |
| tatoh_cpm_10_15 | whole available replay | 71.99 | 91.6 | 19.6 | 1/37 |
| tatoh_cpm_15_20 | whole available replay | 88.22 | 92.27 | 4.056 | 1/35 |
| tatoh_cpm_10_20 | whole available replay | 80.11 | 93.29 | 13.18 | 1/35 |
| tatoh_reclick_open | whole available replay | 0.3255 | 0.3989 | 0.07333 | 1/40 |
| tatoh_dedup_open_cpm | whole available replay | 68.28 | 65.91 | -2.366 | 1/40 |
| tatoh_reclick_whole | whole available replay | 0.2601 | 0.3022 | 0.04212 | 1/40 |
| tatoh_dedup_whole_cpm | whole available replay | 57.17 | 62.4 | 5.234 | 1/40 |
| tatoh_gap_p50_open | whole available replay | 0.2485 | 0.2385 | -0.01006 | 1/40 |
| tatoh_gap_p90_open | whole available replay | 1.377 | 1.438 | 0.06166 | 1/40 |
| tatoh_gap_p99_open | whole available replay | 2.943 | 3.434 | 0.4909 | 1/40 |
| tatoh_gap_p99_10_20 | whole available replay | 5.969 | 3.841 | -2.128 | 1/35 |
| feudal_request_game_s | whole available replay | 686.5 | 436.6 | -249.9 | 1/39 |
| castle_request_game_s | whole available replay | 888.9 | 908 | 19.07 | 1/33 |
| imperial_request_game_s | whole available replay | 1964 | 2043 | 79.69 | 1/13 |

### TaToH provisional 2019

| Trait | Window | Early | Late | Δ | Games early/late |
|---|---|---:|---:|---:|---:|
| all_recorded_cpm | first 10 game minutes | 108.7 | 134.2 | 25.53 | 1/39 |
| core_cpm | first 10 game minutes | 108.7 | 108 | -0.6652 | 1/39 |
| noncore_action_fraction | first 10 game minutes | 0 | 0.1952 | 0.1952 | 1/39 |
| first_core_command_nominal_s | first 10 game minutes | 1.488 | 1.046 | -0.4416 | 1/39 |
| core_gap_p10_s | first 10 game minutes | 0.3032 | 0.1154 | -0.1878 | 1/39 |
| core_gap_p50_s | first 10 game minutes | 0.32 | 0.2385 | -0.08154 | 1/39 |
| core_gap_p90_s | first 10 game minutes | 1.516 | 1.446 | -0.06964 | 1/39 |
| core_gap_p99_s | first 10 game minutes | 4.627 | 3.455 | -1.172 | 1/39 |
| core_gap_max_s | first 10 game minutes | 10.31 | 6.246 | -4.061 | 1/39 |
| simultaneous_core_gap_fraction | first 10 game minutes | 0.2545 | 0.03605 | -0.2185 | 1/39 |
| core_gap_cv | first 10 game minutes | 1.535 | 1.324 | -0.211 | 1/39 |
| core_gap_burstiness | first 10 game minutes | 0.2112 | 0.1396 | -0.0716 | 1/39 |
| command_silence_ge5s_time_fraction | first 10 game minutes | 0.1027 | 0.01998 | -0.08267 | 1/39 |
| command_silence_ge10s_time_fraction | first 10 game minutes | 0.0306 | 0 | -0.0306 | 1/39 |
| core_count_5s_cv | first 10 game minutes | 0.4859 | 0.4257 | -0.06017 | 1/39 |
| peak_5s_nominal_cpm | first 10 game minutes | 240 | 228 | -12 | 1/39 |
| empty_5s_bin_fraction | first 10 game minutes | 0.02941 | 0.01389 | -0.01552 | 1/39 |
| core_type_entropy_bits | first 10 game minutes | 0.6277 | 0.6992 | 0.0715 | 1/39 |
| core_category_entropy_bits | first 10 game minutes | 0.6277 | 0.6841 | 0.05647 | 1/39 |
| core_type_transition_entropy_bits | first 10 game minutes | 0.5427 | 0.5952 | 0.05249 | 1/39 |
| core_type_switch_fraction | first 10 game minutes | 0.1461 | 0.1583 | 0.01219 | 1/39 |
| core_category_switch_fraction | first 10 game minutes | 0.1461 | 0.1583 | 0.01219 | 1/39 |
| core_same_type_triplet_fraction | first 10 game minutes | 0.7599 | 0.7399 | -0.01995 | 1/39 |
| coordinate_coverage | first 10 game minutes | 1 | 1 | 0 | 1/39 |
| destination_jump_diagonal_p50 | first 10 game minutes | 0.01695 | 0.01585 | -0.001095 | 1/39 |
| destination_jump_diagonal_p90 | first 10 game minutes | 0.1778 | 0.1626 | -0.01516 | 1/39 |
| destination_jump_ge_quarter_fraction | first 10 game minutes | 0.0453 | 0.05424 | 0.008935 | 1/39 |
| destination_entropy_4x4_bits | first 10 game minutes | 2.597 | 2.54 | -0.05724 | 1/39 |
| destination_cell_switch_fraction | first 10 game minutes | 0.2567 | 0.2556 | -0.001072 | 1/39 |
| rapid_destination_repeat_fraction | first 10 game minutes | 0.4094 | 0.419 | 0.009652 | 1/39 |
| dedup_core_cpm | first 10 game minutes | 65.19 | 66.42 | 1.223 | 1/39 |
| move_order_commands | first 10 game minutes | — | 624 | — | 0/39 |
| explicit_actor_commands | first 10 game minutes | — | 199 | — | 0/39 |
| explicit_actor_coverage | first 10 game minutes | — | 0.3169 | — | 0/39 |
| actor_pair_count | first 10 game minutes | — | 87 | — | 0/39 |
| same_actor_pair_count | first 10 game minutes | — | 13 | — | 0/39 |
| actor_group_size_median | first 10 game minutes | — | 1 | — | 0/39 |
| actor_group_size_p90 | first 10 game minutes | — | 3 | — | 0/39 |
| actor_group_ge10_fraction | first 10 game minutes | — | 0 | — | 0/39 |
| actor_group_change_fraction | first 10 game minutes | — | 0.8434 | — | 0/39 |
| actor_overlap_jaccard_median | first 10 game minutes | — | 0 | — | 0/39 |
| same_actor_gap_nominal_median_s | first 10 game minutes | — | 0.2385 | — | 0/39 |
| same_actor_recommand_under1s_fraction | first 10 game minutes | — | 0.9231 | — | 0/39 |
| commanded_actor_ids | first 10 game minutes | — | 32 | — | 0/39 |
| valid_target_order_fraction | first 10 game minutes | — | 1 | — | 0/39 |
| distinct_order_target_ids | first 10 game minutes | — | 28 | — | 0/39 |
| distinct_building_type_ids | first 10 game minutes | — | 5 | — | 0/39 |
| distinct_research_type_ids | first 10 game minutes | — | 3 | — | 0/39 |
| positive_de_queue_commands | first 10 game minutes | — | 23 | — | 0/39 |
| requested_queue_unit_type_ids | first 10 game minutes | — | 2 | — | 0/39 |
| explicitly_commanded_production_building_ids | first 10 game minutes | — | 2 | — | 0/39 |
| production_command_revisit_nominal_median_s | first 10 game minutes | — | 13.44 | — | 0/39 |
| positive_queue_amount_mean | first 10 game minutes | — | 1.222 | — | 0/39 |
| build_commands_nominal_min | first 10 game minutes | — | 1.69 | — | 0/39 |
| wall_commands_nominal_min | first 10 game minutes | — | 0 | — | 0/39 |
| research_commands_nominal_min | first 10 game minutes | — | 0.507 | — | 0/39 |
| market_commands_nominal_min | first 10 game minutes | — | 0 | — | 0/39 |
| legacy_command_class_entropy_bits | first 10 game minutes | — | — | — | 0/0 |
| legacy_switches_per_100_commands | first 10 game minutes | — | — | — | 0/0 |
| legacy_core_silence_over5s_fraction | first 10 game minutes | — | — | — | 0/0 |
| legacy_peak_10s_nominal_cpm | first 10 game minutes | — | — | — | 0/0 |
| legacy_move_share | first 10 game minutes | — | — | — | 0/0 |
| legacy_planning_command_share | first 10 game minutes | — | — | — | 0/0 |
| legacy_queue_batch_mean | first 10 game minutes | — | — | — | 0/0 |
| legacy_queue_batch_gt1_fraction | first 10 game minutes | — | — | — | 0/0 |
| legacy_duration_game_min | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_0_5 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_5_10 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_10_15 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_15_20 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_cpm_10_20 | first 10 game minutes | — | — | — | 0/0 |
| tatoh_reclick_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_dedup_open_cpm | first 10 game minutes | — | — | — | 0/0 |
| tatoh_reclick_whole | first 10 game minutes | — | — | — | 0/0 |
| tatoh_dedup_whole_cpm | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p50_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p90_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p99_open | first 10 game minutes | — | — | — | 0/0 |
| tatoh_gap_p99_10_20 | first 10 game minutes | — | — | — | 0/0 |
| feudal_request_game_s | first 10 game minutes | — | 436.6 | — | 0/37 |
| castle_request_game_s | first 10 game minutes | — | 532.6 | — | 0/2 |
| imperial_request_game_s | first 10 game minutes | — | — | — | 0/0 |
| all_recorded_cpm | whole available replay | 92.67 | 125.8 | 33.11 | 1/40 |
| core_cpm | whole available replay | 91.54 | 91.02 | -0.5196 | 1/40 |
| noncore_action_fraction | whole available replay | 0.01224 | 0.2698 | 0.2576 | 1/40 |
| first_core_command_nominal_s | whole available replay | 1.488 | 1.046 | -0.4416 | 1/40 |
| core_gap_p10_s | whole available replay | 0.3032 | 0.1154 | -0.1878 | 1/40 |
| core_gap_p50_s | whole available replay | 0.6063 | 0.3615 | -0.2448 | 1/40 |
| core_gap_p90_s | whole available replay | 1.888 | 1.685 | -0.2034 | 1/40 |
| core_gap_p99_s | whole available replay | 4.817 | 4.085 | -0.7323 | 1/40 |
| core_gap_max_s | whole available replay | 10.31 | 9.977 | -0.3304 | 1/40 |
| simultaneous_core_gap_fraction | whole available replay | 0.242 | 0.03263 | -0.2094 | 1/40 |
| core_gap_cv | whole available replay | 1.373 | 1.34 | -0.03228 | 1/40 |
| core_gap_burstiness | whole available replay | 0.1571 | 0.1455 | -0.01162 | 1/40 |
| command_silence_ge5s_time_fraction | whole available replay | 0.07264 | 0.05577 | -0.01688 | 1/40 |
| command_silence_ge10s_time_fraction | whole available replay | 0.009277 | 0.005523 | -0.003754 | 1/40 |
| core_count_5s_cv | whole available replay | 0.5191 | 0.503 | -0.01612 | 1/40 |
| peak_5s_nominal_cpm | whole available replay | 240 | 240 | 0 | 1/40 |
| empty_5s_bin_fraction | whole available replay | 0.02242 | 0.01579 | -0.006632 | 1/40 |
| core_type_entropy_bits | whole available replay | 1.245 | 1.169 | -0.07629 | 1/40 |
| core_category_entropy_bits | whole available replay | 1.215 | 1.13 | -0.08478 | 1/40 |
| core_type_transition_entropy_bits | whole available replay | 1.049 | 1.001 | -0.0478 | 1/40 |
| core_type_switch_fraction | whole available replay | 0.2893 | 0.2737 | -0.01557 | 1/40 |
| core_category_switch_fraction | whole available replay | 0.2875 | 0.2737 | -0.0138 | 1/40 |
| core_same_type_triplet_fraction | whole available replay | 0.5357 | 0.5809 | 0.04514 | 1/40 |
| coordinate_coverage | whole available replay | 1 | 1 | 0 | 1/40 |
| destination_jump_diagonal_p50 | whole available replay | 0.02071 | 0.02284 | 0.002127 | 1/40 |
| destination_jump_diagonal_p90 | whole available replay | 0.1799 | 0.2324 | 0.05252 | 1/40 |
| destination_jump_ge_quarter_fraction | whole available replay | 0.06861 | 0.09255 | 0.02393 | 1/40 |
| destination_entropy_4x4_bits | whole available replay | 3.124 | 3.072 | -0.05205 | 1/40 |
| destination_cell_switch_fraction | whole available replay | 0.2376 | 0.3059 | 0.06832 | 1/40 |
| rapid_destination_repeat_fraction | whole available replay | 0.3628 | 0.3244 | -0.03833 | 1/40 |
| dedup_core_cpm | whole available replay | 60.7 | 62.44 | 1.742 | 1/40 |
| move_order_commands | whole available replay | — | 1503 | — | 0/40 |
| explicit_actor_commands | whole available replay | — | 598 | — | 0/40 |
| explicit_actor_coverage | whole available replay | — | 0.4217 | — | 0/40 |
| actor_pair_count | whole available replay | — | 307 | — | 0/40 |
| same_actor_pair_count | whole available replay | — | 80 | — | 0/40 |
| actor_group_size_median | whole available replay | — | 1 | — | 0/40 |
| actor_group_size_p90 | whole available replay | — | 7 | — | 0/40 |
| actor_group_ge10_fraction | whole available replay | — | 0.02514 | — | 0/40 |
| actor_group_change_fraction | whole available replay | — | 0.7654 | — | 0/40 |
| actor_overlap_jaccard_median | whole available replay | — | 0 | — | 0/40 |
| same_actor_gap_nominal_median_s | whole available replay | — | 0.2385 | — | 0/40 |
| same_actor_recommand_under1s_fraction | whole available replay | — | 0.8851 | — | 0/40 |
| commanded_actor_ids | whole available replay | — | 105 | — | 0/40 |
| valid_target_order_fraction | whole available replay | — | 1 | — | 0/40 |
| distinct_order_target_ids | whole available replay | — | 111 | — | 0/40 |
| distinct_building_type_ids | whole available replay | — | 15 | — | 0/40 |
| distinct_research_type_ids | whole available replay | — | 16 | — | 0/40 |
| positive_de_queue_commands | whole available replay | — | 139 | — | 0/40 |
| requested_queue_unit_type_ids | whole available replay | — | 7 | — | 0/40 |
| explicitly_commanded_production_building_ids | whole available replay | — | 12 | — | 0/40 |
| production_command_revisit_nominal_median_s | whole available replay | — | 6.52 | — | 0/40 |
| positive_queue_amount_mean | whole available replay | — | 1.046 | — | 0/40 |
| build_commands_nominal_min | whole available replay | — | 4.282 | — | 0/40 |
| wall_commands_nominal_min | whole available replay | — | 0.4608 | — | 0/40 |
| research_commands_nominal_min | whole available replay | — | 1.15 | — | 0/40 |
| market_commands_nominal_min | whole available replay | — | 0.4228 | — | 0/40 |
| legacy_command_class_entropy_bits | whole available replay | — | 1.13 | — | 0/40 |
| legacy_switches_per_100_commands | whole available replay | — | 27.37 | — | 0/40 |
| legacy_core_silence_over5s_fraction | whole available replay | — | — | — | 0/0 |
| legacy_peak_10s_nominal_cpm | whole available replay | — | — | — | 0/0 |
| legacy_move_share | whole available replay | — | — | — | 0/0 |
| legacy_planning_command_share | whole available replay | — | 0.07728 | — | 0/40 |
| legacy_queue_batch_mean | whole available replay | — | 1.046 | — | 0/40 |
| legacy_queue_batch_gt1_fraction | whole available replay | — | — | — | 0/0 |
| legacy_duration_game_min | whole available replay | — | 29.56 | — | 0/40 |
| tatoh_cpm_0_5 | whole available replay | — | 122 | — | 0/40 |
| tatoh_cpm_5_10 | whole available replay | — | 97.01 | — | 0/39 |
| tatoh_cpm_10_15 | whole available replay | — | 91.6 | — | 0/37 |
| tatoh_cpm_15_20 | whole available replay | — | 92.27 | — | 0/35 |
| tatoh_cpm_10_20 | whole available replay | — | 93.29 | — | 0/35 |
| tatoh_reclick_open | whole available replay | — | 0.3989 | — | 0/40 |
| tatoh_dedup_open_cpm | whole available replay | — | 65.91 | — | 0/40 |
| tatoh_reclick_whole | whole available replay | — | 0.3022 | — | 0/40 |
| tatoh_dedup_whole_cpm | whole available replay | — | 62.4 | — | 0/40 |
| tatoh_gap_p50_open | whole available replay | — | 0.2385 | — | 0/40 |
| tatoh_gap_p90_open | whole available replay | — | 1.438 | — | 0/40 |
| tatoh_gap_p99_open | whole available replay | — | 3.434 | — | 0/40 |
| tatoh_gap_p99_10_20 | whole available replay | — | 3.841 | — | 0/35 |
| feudal_request_game_s | whole available replay | — | 436.6 | — | 0/39 |
| castle_request_game_s | whole available replay | — | 908 | — | 0/33 |
| imperial_request_game_s | whole available replay | — | 2043 | — | 0/13 |

## Unavailable or limited families

- Economy, production uptime, combat efficiency, projectile dodges, visibility-conditioned response and multiple-front interference: world-state/visibility decoding is not completed.
- Recent actor-group measurements: available for six player-game observations, but no historical state-command baseline exists.
- Working-memory capacity, perceptual reaction time and compensation: not directly measured by any included table.
- Rating/peer trends: existing snapshot data are separate competitive outcomes, not earliest-game cognitive traits.

## Reproduction

Run expand_all_tatoh_features.py, expand_tatoh_details.py, then compare_all_traits.py. Inputs include raw replay files, the existing validated detail tables, and the quarantined 2019 candidate. Tables record weighting, sample counts, ranges, definitions and restrictions; no significance tests are claimed.
