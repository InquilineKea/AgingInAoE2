# Expanded metric analysis and earlier-game check

The registry contains 255 candidate measurements and control variables. These are not 255 completed features. Thirty-one command-based numeric features were calculated for 49 player-game observations in opening and whole-available-replay windows. All 88 overlapping DauT/TheViper window command rates agree with the previously validated analysis. Actor-group metrics were additionally calculated for six recent player-game observations, with incomplete match coverage labeled.

## Earlier-game coverage

DauT: four 2011 recordings and seven 2012 team games are included in the expanded command analysis. TheViper: nine 2012 observations are included. Their classic-engine timestamp and ownership differences preclude direct high-resolution timing comparisons with DE. There is no newly verified sample before these earliest periods.

TaToH: the 2019 archive contains a fully consumed 32.983-minute replay with +Zaid versus feudalVoy. Its uploader title and description explicitly attribute it to TaToH. This supports community attribution, not independent account identity. The replay appears to concern the Feudal-only challenge, so it is quarantined from the main unrestricted-play comparison. Its attributed opening replay command rate is 108.66 per nominal minute, but 20.9% of all replay actions have no player ownership and are omitted from player-specific rates. Do not interpret it as a verified basic-input APM baseline. See 2019_provisional_features.csv and 2019_provisional_provenance.json.

The 2021 TaToH pack was retried with a cache refresh and byte-range request. It still returned exactly 524,288 bytes, and the range beyond that returned HTTP 416 with total size 524,288. Aocrecs failed TLS verification; certificate verification was retained. Archive search found the 2019 candidate but no additional verified earlier TaToH replay. Logs are included.

## Completed state capture

Four full matches are complete, containing 362011 frames in total and zero reported skipped simulation steps. TheViper versus TaToH supplies data for both players. State-command summaries and actor-group features are included; raw state frames remain in engine-pass. Binary world state, projectile paths and player visibility have not been decoded, so this is not an onager-dodge analysis.

## New features and interpretation

Command volume, positive gap percentiles, longest gap, simultaneous command fraction, gap variation, burstiness, five-second activity variation, empty bins, time in long command silences, command-type/category entropy, transition entropy, category switches, repeated triplets, spatial destination entropy and jumps, and approximate deduplicated command rate are in behavior_features.csv. Whole-game and phase-specific values have different exposure and survivor composition. Classic timing fields are flagged as incomparable with DE.

Engine actor features use explicit unit sets in humanOrder=true commands with an explicit player ID. Exact group size, overlap and revisit behavior describe command organization; they do not identify semantic tasks, attention or memory capacity. Flag fields are reported literally.

For an aging study, prioritize opportunity-normalized visible-threat response, dodge success/damage avoidance, economy idle time during matched battle, and performance loss with simultaneous fronts. These need validated world state, player visibility and comparable repeated sessions. APM alone cannot isolate age effects.

## Reproduce

Use the repository environment and run deadline_sparse.py, extend_tatoh_submission.py, behavior_metrics.py, metric_catalog.py, earlier_candidate.py, engine_actor_features.py, then finalize_expanded_bundle.py. Raw data paths and source hashes are retained. No significance test or causal aging claim is presented.
