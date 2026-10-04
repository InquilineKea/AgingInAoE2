# AgingInAoE2

Replay-based longitudinal behavioral comparisons of **DauT, TheViper and TaToH**, using the earliest verified recordings recovered for this project and recent 2026 games. This is an exploratory convenience sample, not evidence of a causal aging effect.

Start with **[individual player findings](deadline-sparse/PLAYER_FINDINGS.md)** and the **[full measured-trait comparison](deadline-sparse/ALL_TRAITS_ANALYSIS.md)**. Download [the searchable HTML report](deadline-sparse/all_traits.html) to open it locally.

## What is measured

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

The local replay-parser environment uses Python 3.9.13 and the inspected parser versions in [requirements.txt](requirements.txt). Analysis additionally uses NumPy, pandas, matplotlib, beautifulsoup4 and requests where imported. Reproduction of the current tables from restored replays and preserved input feature tables uses:

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
