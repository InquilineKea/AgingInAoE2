# AgingInAoE2

Replay-based behavioral analysis of **DauT, TheViper, TaToH and MembTV**. Longitudinal comparisons use the earliest verified recordings recovered for the first three players and recent 2026 games. MembTV is a separately labeled recent cohort whose historical replay baseline remains unavailable. This is an exploratory convenience sample, not evidence of a causal aging effect.

Start with **[individual player findings](deadline-sparse/PLAYER_FINDINGS.md)** and the **[full measured-trait comparison](deadline-sparse/ALL_TRAITS_ANALYSIS.md)**. Download [the searchable HTML report](deadline-sparse/all_traits.html) to open it locally.

## Demand, game phase and observed-session follow-up

The [new stamina analysis](stamina/REPORT.md) tests the same 98 observations using fixed game-clock intervals, per-game opening baselines, 29 qualifying 45+ player-game observations (19 DE), research-request anchors, and 12 recent observed-session/context groups with at least three complete openings. It reports raw gap denominators, burst definitions, first/last opening contrasts, and session-break sensitivities. The separate synchronization-counter audit is exploratory: its semantics are not validated and it does not measure useful output or cognitive capacity.

- [Long-game paired changes](stamina/long_game_paired_changes.csv)
- [Observed-session changes and slopes](stamina/session_first_last_and_slopes.csv)
- [Counter-proxy audit and coverage](stamina/sync_counter_paired_audit.csv)
- [Validation](stamina/validation.json)

## MembTV extension

The [MembTV report](memb/REPORT.md) adds an older player, age 49, using a fixed newest-first sample of public replays. His displayed RM 1v1 rating of 1810 does not establish recent ranked activity: the latest retrieved ranked log is from May 2026 and the tested recordings are unavailable. Recent recovered recordings are primarily unranked Rage Forest team games, with separate ranked team-map contexts. These are not pooled with professional 1v1 periods.

The extension retains the original 82-field dictionary, pairs long-game phases within each recording, and compares opening command patterns across observed sessions. The proposed age 42–49 DE series remains a potential collection range, not measured coverage. Historical endpoints and archive access failures are documented rather than replaced with inferred aging results.

- [Memb per-game traits](memb/original_82_trait_metrics.csv) and [all-player comparison table](memb/all_players_trait_comparisons.csv), including explicitly unavailable Memb historical contrasts.
- [Memb long-game results](memb/long_game_summary.csv) and [paired measurements](memb/long_game_paired_changes.csv).
- [Memb observed-session results](memb/session_comparisons.csv) and [individual openings](memb/session_opening_metrics.csv).
- [Source inventory](memb/game_inventory.csv), [excluded short aborts](memb/excluded_recordings.json), [validation](memb/validation.json), and [combined coverage](memb/integration_validation.json).
- [Memb release inputs and analysis](https://github.com/InquilineKea/AgingInAoE2/releases/tag/memb-v1).

Restore this extension's replay inputs without overwriting differing files:

```sh
gh release download memb-v1 --repo InquilineKea/AgingInAoE2 --pattern memb-analysis.zip --pattern SHA256SUMS-memb.txt
shasum -a 256 -c SHA256SUMS-memb.txt
python scripts/restore_memb_inputs.py memb-analysis.zip
python scripts/analyze_memb.py
python scripts/report_memb.py
```

## What is measured in the original three-player analysis

| Artifact | Coverage |
|---|---|
| Verified command dataset | 98 player-game observations; 195 opening/whole-replay rows |
| Measured definitions and coverage fields | 82, including distinct legacy definitions; not 82 independent cognitive traits |
| Period comparisons | Seven comparison sets; 1,148 rows, of which 808 have numbers for both periods |
| Candidate metric/control catalog | 255 entries; implementation status is recorded explicitly |
| Recent complete engine captures | Four matches; 362,011 frames and 12,368 commands; zero reported skipped simulation steps |
| Source archive | 91 distinct verified source replay files, plus one provisional 2019 candidate |

Available measures include command rates, command-gap distributions, burstiness, silence intervals, command-category and type diversity, destination changes, approximate repeated orders, approximate deduplicated rates, production requests and first age-up research requests. [The trait dictionary](deadline-sparse/trait_dictionary.csv) describes definitions and coverage limits.

**Reaction time, working-memory capacity, cognitive compensation, enemy visibility, and onager-dodge success have not been measured.** API version 22 engine-state payloads are captured but not decoded into validated unit-state trajectories. A native decoder test succeeded on a separate 2024 fixture; that is not validation on these player replays.

## Earliest recovered baselines

| Player | Earliest verified replay period | Latest verified recording |
|---|---|---|
| DauT | November 2011, classic AoE2 | September 25, 2026 UTC |
| TheViper | January 2012, classic AoE2 | September 30, 2026 UTC |
| TaToH | March 2021, partial Hidden Cup 4 recording | October 3, 2026 UTC |

These are the earliest available verified files in this study, not the players' first career games. The community-attributed 2019 TaToH candidate has an unverified identity and unusual challenge settings; it remains separate. See [literal recording endpoints](deadline-sparse/comparison_endpoints.json).

Command-rate changes differ by player, period, phase and definition. Whole-replay core command rates are higher in the 2026 samples than the earliest recovered samples for all three players, but that does not demonstrate faster reactions or preserved cognition. Classic versus DE encoding, team versus 1v1 games, map, opponents, settings and partial recordings limit comparisons. For the 2021-to-2026 DE comparison, opening core rates decrease for DauT and TheViper while whole-replay rates increase; TaToH's tournament opening core rate is similar to the single recovered 2021 baseline.

## Read the results

- [Player findings and limitations](deadline-sparse/PLAYER_FINDINGS.md)
- [All period comparison tables](deadline-sparse/ALL_TRAITS_ANALYSIS.md) and [CSV](deadline-sparse/all_trait_comparisons.csv)
- [Literal earliest/latest file contrasts](deadline-sparse/single_game_endpoint_comparisons.csv)
- [All per-game command features](deadline-sparse/behavior_features_all.csv)
- [TaToH detailed features](deadline-sparse/tatoh_detail_features_all.csv)
- [Candidate metric implementation status](deadline-sparse/catalog_comparison_status.csv)
- [Consistency and command efficiency](CONSISTENCY_AND_EFFICIENCY.md)
- [Source replay provenance](deadline-sparse/all_source_replays.json)
- [Capture inventory, including incomplete attempts](engine-pass/capture-inventory.json)

Series/session days receive equal total weight, and games share their cluster's weight. Weighted median ties at half the total weight use the midpoint. Game medians and observed ranges are also retained. Ranges are not confidence intervals; no population significance or causal aging test is reported. Separate [rating history](deadline-sparse/competitive_rating_years.csv) and [sample outcomes](deadline-sparse/sample_outcome_summary.csv) measure competitive results rather than cognitive constructs.

## Download the inputs and reproduce

The [analysis-v1 release](https://github.com/InquilineKea/AgingInAoE2/releases/tag/analysis-v1) contains the replay/analysis archive, the recent engine-state archive, and checksums. Large archives are release assets rather than Git files. Original replay recordings can contain public match chat; derived command exports omit it, and the engine collector removes PlayerChat events.

```sh
gh release download analysis-v1 --repo InquilineKea/AgingInAoE2 --pattern '*.zip' --pattern 'SHA256SUMS.txt'
shasum -a 256 -c SHA256SUMS.txt
python3 scripts/restore_release_inputs.py submission-all-traits.zip
python3 scripts/verify_published_dataset.py
```

The local replay-parser environment uses Python 3.9.13 and the inspected parser versions in [requirements.txt](requirements.txt). The existing NumPy, pandas, matplotlib, beautifulsoup4 and requests versions are also recorded there. Optional engine-collection dependencies are in `requirements-engine.txt`. Reproduction of the current tables from restored replays and preserved input feature tables uses:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/expand_all_tatoh_features.py
.venv/bin/python scripts/expand_tatoh_details.py
.venv/bin/python scripts/compare_all_traits.py
.venv/bin/python scripts/compare_outcomes_snapshot.py
```

Earlier pilot scripts and reports are retained for provenance. The current results are in `deadline-sparse/PLAYER_FINDINGS.md` and `deadline-sparse/ALL_TRAITS_ANALYSIS.md`; older reports describe earlier coverage. The reproduction commands above reuse preserved baseline feature tables; they do not imply a newly decoded historical engine-state baseline. Rebuilding every baseline feature table from raw recordings also requires the earlier decode/analysis stages.

## Engine collection and third-party software

State streams use the local AoE2 DE game API through the published LibreMatch CadeRemote protocol. Collection requires the game running with a compatible replay, gRPC/protobuf, and protocol definitions. CrossOver and owned AoE2 DE/CaptureAge installations are not distributed here. Correct extra-fast playback used the `EXTRA_FAST=3` enum and advanced about five game seconds per wall-clock second without reported simulation-step skips.

See [third-party provenance](THIRD_PARTY.md). Protocol client certificate/key fixtures, installed applications, account credentials, local environments and system configuration files are not distributed. No license is asserted over original game recordings or third-party works.
