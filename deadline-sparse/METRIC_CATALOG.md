# Cross-game measurement catalog

This is a broad candidate registry, not a claim that all metrics have been implemented or validated. Behavioral features do not directly measure working-memory capacity, perception, reaction time or aging.

C = command-derived, S = requires decoded state, V = requires visibility/camera evidence, O = outcome metadata. Current API22 state streams are captured but not decoded. Historical state streams remain unavailable.

## Command volume

Data required: Commands; timestamped attributed actions.

- Replay-derived APM
- Core command rate
- Phase-specific command rate
- Command-type shares
- Movement-command rate
- Interaction-command rate
- Build-command rate
- Wall-command rate
- Research-command rate
- Market-command rate
- Queue-command rate
- Cancel-command rate
- Patrol-command rate
- Formation-command rate
- Stop-command rate
- Garrison-command rate
- Ungarrison-command rate
- Delete-command rate
- Attack-move-command rate
- Repair-command rate

## Timing and consistency

Data required: Commands; adequate timestamp resolution.

- Median positive command gap
- p90 command gap
- p99 command gap
- Maximum command gap
- Zero-gap command share
- Gap coefficient of variation
- Gap burstiness
- Five-second action-count variation
- Peak five-second action rate
- Peak ten-second action rate
- Empty five-second bin share
- Command-silence time above five seconds
- Command-silence time above ten seconds
- First-command delay
- Rate slope within matched phase
- Rate change after minute ten
- Early-versus-late gap change
- Across-game coefficient of variation
- Across-session trend
- Back-to-back game fatigue slope

## Command organization

Data required: Commands; command semantics and payload coverage.

- Command-type diversity
- Command-type entropy
- Command-category entropy
- Type transition entropy
- Type switch rate
- Category switch rate
- Same-type streak length
- Same-type triplet share
- Repeated-command share
- Approximate deduplicated command rate
- Commands per requested action
- Actor-list coverage
- Explicit actor-group size
- Explicit actor-group size p90
- Large explicit-group share
- Explicit-group overlap
- Explicit-group change rate
- Same explicit-group revisit interval
- Explicit production-building revisit interval
- Number of distinct commanded actor IDs

## Spatial command organization

Data required: Commands; coordinate coverage and map dimensions.

- Median destination jump
- p90 destination jump
- Large destination-jump share
- Destination entropy across map cells
- Destination-cell switch rate
- Destination concentration
- Distance between consecutive build requests
- Commanded-region count
- Within-region burst length
- Destination-return interval
- Spatial command alternation
- Direction-reversal share
- Repeated nearby destination share
- Commanded target diversity
- Target-change rate
- Cross-map command density

## Economy

Data required: Decoded state; ownership; resources; queues; unit activity.

- Town-center idle time
- Villager idle time
- Idle production-building time
- Villager count at matched minutes
- Villager growth rate
- Resource stockpile trajectories
- Resource float area under curve
- Resource imbalance
- Worker allocation shares
- Worker allocation changes
- Resource income per minute
- Gather efficiency per villager
- Villager losses per exposed villager-minute
- House-block duration
- House-block incident rate
- Farm reseed downtime
- Gatherer walking time
- Builder-minutes per completed structure
- Trade efficiency
- Market transaction cost
- Resource collection before age-up
- Economy recovery after raid

## Production and planning

Data required: Commands for requests; decoded state for completion and opportunity.

- First Feudal research request
- First Castle research request
- First Imperial research request
- Actual age-up completion
- Upgrade timing relative to army
- Production-building count
- Production uptime
- Queue depth
- Queue emptiness duration
- Requested queue batch size
- Actual production batch size
- Queue-cancel rate
- Research-cancel rate
- Building-cancel rate
- Build completion delay
- Construction abandonment
- Technology-choice diversity
- Unit-production diversity
- Production composition entropy
- Production switching delay
- Supply added before cap
- Unspent resources despite affordable production

## Combat efficiency

Data required: Decoded state; ownership; unit values and combat exposure.

- Resource-weighted kill-loss ratio
- Unit survival time
- Army resource value over time
- Damage per army-value minute
- Damage taken per exposed unit-minute
- Overkill fraction
- Target priority by unit value
- Focus-fire concentration
- Fight initiation at favorable value ratio
- Retreat latency after unfavorable exchange
- Low-health unit rescue rate
- Idle army time during engagement
- Pathing congestion time
- Reinforcement travel time
- Army regrouping time
- Unit cohesion
- Formation spread
- Conversion success per attempt
- Monk losses per conversion
- Repair value saved
- Friendly-fire losses
- Siege survival time
- Siege escort distance
- Raid damage per raider-value minute

## Projectile and precise micro

Data required: Decoded state; projectile trajectories; unit paths; command actors; visibility.

- Projectile-threat opportunity count
- Visible-threat-to-command latency
- Command-to-motion latency
- Preemptive dodge fraction
- Dodge success rate
- Dodge distance perpendicular to trajectory
- Dodge angle
- Units hit per projectile
- Expected damage avoided
- Army split count
- Split separation distance
- Regroup time after dodge
- Commands per successful dodge
- Dodge performance under simultaneous threats
- False-positive dodge rate
- Kiting attack-cycle efficiency
- Stutter-step lost attack time
- Melee surround completion time
- Target-switch latency after target death
- Conversion-response latency
- Villager quickwall latency
- Quickwall completion before contact
- Garrison latency after visible raid
- Missed visible threat rate

## Multiple-task interference

Data required: Decoded state plus commands; predefined simultaneous tasks.

- Number of concurrently active fronts
- Task-switch interval
- Return-to-task delay
- Economy-command gap during battle
- Economy idle time during battle
- Production idle time during battle
- Secondary-front loss during main battle
- Unattended-raid loss rate
- Threat-response latency by concurrent-front count
- Micro outcome by concurrent-front count
- Two-front performance decrement
- Army control while expanding economy
- Task completion before interruption
- Resumption error rate
- Cross-front resource imbalance

## Scouting and information

Data required: Decoded player visibility; exploration; ideally original camera stream.

- Explored map fraction
- Time to locate opponent
- Time to locate each resource
- Scout survival
- Relevant opponent structure discovery time
- Scouting revisit frequency
- Information age at strategy decision
- Response delay after observed tech reveal
- Response delay after observed army reveal
- Revealed-threat miss rate
- Army orders into known danger
- Fog-of-war exposure
- Camera revisit interval
- Camera-command distance
- Visible-event response conditional on camera

## Strategy and adaptation

Data required: State; commands; opponent and map context; strategy labels.

- Opening sequence
- Opening diversity across games
- Build-order deviation timing
- Resource investment split
- Military composition versus visible enemy
- Counter-unit production delay
- Technology adaptation delay
- Expansion timing
- Defensive investment timing
- Walling timing relative to threat
- Distance of defensive structures to threatened economy
- Map-control share
- Choke-point control
- Safe-resource access
- Relic acquisition timing
- Objective capture timing
- Strategic transition frequency
- Strategy persistence after failed attack
- Army-value advantage converted to damage
- Economy advantage converted to army
- Comeback conversion probability

## Outcomes and relative performance

Data required: Match metadata; ratings; series and opponent context.

- Win share
- Opponent-adjusted win probability
- Tournament Elo
- Relative peer rank
- Gap to peer median
- Gap to best peer
- Series win share against fixed peers
- Game length
- Resign timing relative to deficit
- Close-game conversion rate
- Performance by civilization
- Performance by map
- Performance by matchup
- Performance against repeated opponent
- Within-series adaptation
- Game-to-game recovery after loss

## Coverage and controls

Data required: Source provenance; timestamps; replay metadata; capture validation.

- Timestamp quantization
- Nominal replay speed
- Measured simulation throughput
- Skipped simulation steps
- Partial replay duration
- Attributed command coverage
- Coordinate coverage
- Explicit actor coverage
- Entity-state coverage
- Player identity confidence
- Map identity
- Civilization identity
- Patch and engine version
- Match setting and start age
- Opponent strength
- Series or session cluster
- Time of day
- Session game order
- Opportunity count per metric
- At-risk unit-minutes

## Recommended aging-sensitive comparisons

1. Matched visible-threat opportunity latency and missed-threat probability, conditional on projectile speed, distance, army size and simultaneous threats. This is game-response latency, not proven perceptual reaction time.
2. Successful dodges per threatened unit and damage avoided per opportunity.
3. Economy/production idle time increase during matched combat, conditional on concurrent fronts.
4. Long command-gap tails, burst variability, command repetition and deduplicated rates within matched phases.
5. Task-resumption delay and cross-front interference with explicit task definitions.
6. Efficiency preserved while action volume changes, using resource-weighted combat and economy outcomes. That could motivate a compensation hypothesis; it does not establish one.

## Normalization and design

Use first ten minutes, fixed later bins and event-aligned windows; do not average survivor-selected late bins without labeling their coverage. Count opportunities, at-risk units and exposure time. Normalize distances to map dimensions, army output to resource value and micro to matchup. Compare timestamp resolution before interpreting latency differences. Stratify by engine/patch, map, civilization, opponent and tournament/ranked settings. Treat series and session days as clusters. A few players and two games per stratum cannot identify causal aging.
