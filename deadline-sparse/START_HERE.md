# Start here: full earliest-to-latest replay analysis

- PLAYER_FINDINGS.md: the individual behavioral findings and limits.
- all_traits.html: searchable table of all comparisons.
- ALL_TRAITS_ANALYSIS.md: full period tables and definitions of scope.
- all_trait_comparisons.csv: 82 defined measurements/coverage fields across seven comparisons, with missing values retained.
- single_game_endpoint_comparisons.csv and comparison_endpoints.json: literal earliest/latest file contrasts.
- trait_dictionary.csv: source implementation, units and definition cautions.
- catalog_comparison_status.csv: status of each of the 255 candidate measurements/controls.
- behavior_features_all.csv and tatoh_detail_features_all.csv: expanded raw feature rows.
- engine_actor_features.csv: six recent player-game observations; no historical engine baseline.
- sample_outcome_summary.csv and competitive_rating_*.csv: separate match outcomes and previously collected rating snapshots.

The verified command dataset contains 98 player-game observations, with 195 phase/window rows. One short TaToH recording has no ten-minute opening row. The 2019 community-attributed FeudalVoy recording remains provisional and is not pooled into the verified baseline. Missing state/visibility metrics, reaction time, working-memory capacity and compensation are not invented.

Series/session days receive equal weight; games share each cluster's weight. Observed ranges are not confidence intervals. No causal aging effect or population significance test is claimed.

All source replay files used for these observations are included by SHA-256. Different recordings of the same match can have different hashes/viewpoint data, so file count is not match count. Full compressed engine-state streams remain in engine-pass outside this ZIP; command summaries and capture validation are included.

Use the existing repository environment to reproduce: expand_all_tatoh_features.py, expand_tatoh_details.py, compare_all_traits.py, compare_outcomes_snapshot.py, then bundle_all_traits.py. The ZIP contains input replay files and source feature tables but preserves repository-relative reproduction paths in provenance.
