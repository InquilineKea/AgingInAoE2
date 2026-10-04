"""Native macOS command-detail reanalysis. No engine state or cognitive scores.

Uses the existing validated, deduplicated manifest and re-reads the raw body.
Only explicitly encoded actor lists are used; missing/reused selections are
not filled from other commands. Target positions are not camera positions.
"""
from pathlib import Path
import collections, gzip, hashlib, json, math
import numpy as np
import pandas as pd
from mgz import fast

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reanalysis-v2'
OUT.mkdir(exist_ok=True)
CORE = {'MOVE', 'ORDER', 'BUILD', 'RESEARCH', 'DELETE', 'BUY', 'SELL', 'WALL'}
FIELDS = ['x', 'y', 'object_ids', 'target_id', 'building_id', 'technology_id',
          'unit_id', 'amount', 'resource_id', 'sequence']


def med(a):
    return float(np.median(a)) if len(a) else None


def frac(a):
    return float(np.mean(a)) if len(a) else None


def features(actions, meta, number, end):
    a = [x for x in actions if x.get('player') == number and x['t'] < end]
    c = [x for x in a if x['type'] in CORE]
    minutes = end / meta['speed'] / 60
    m = [x for x in a if x['type'] in ('MOVE', 'ORDER')]
    explicit = [x for x in m if x.get('object_ids')]
    sizes = [len(x['object_ids']) for x in explicit]
    pairs = [(x,y) for x,y in zip(m,m[1:]) if x.get('object_ids') and y.get('object_ids')]
    same = [(x,y) for x,y in pairs if set(x['object_ids']) == set(y['object_ids'])]
    group_changes = [set(x['object_ids']) != set(y['object_ids']) for x,y in pairs]
    overlaps = [len(set(x['object_ids']) & set(y['object_ids'])) /
                len(set(x['object_ids']) | set(y['object_ids'])) for x,y in pairs]
    coords = [(x['x'], x['y']) for x in m if x.get('x') is not None and x.get('y') is not None
              and 0 <= x['x'] < meta['dimension'] and 0 <= x['y'] < meta['dimension']]
    jumps = [math.hypot(x[0]-y[0],x[1]-y[1]) / (meta['dimension'] * math.sqrt(2))
             for x,y in zip(coords,coords[1:])]
    orders = [x for x in a if x['type'] == 'ORDER']
    target_orders = [x for x in orders if x.get('target_id') not in (None,0,4294967295)]
    builds = [x for x in a if x['type'] == 'BUILD']
    research = [x for x in a if x['type'] == 'RESEARCH']
    queue = [x for x in a if x['type'] == 'DE_QUEUE' and x.get('amount',0) > 0]
    # Commands directed to production buildings, not completed production.
    buildings = collections.defaultdict(list)
    for q in queue:
        for oid in q.get('object_ids',[]): buildings[oid].append(q['t'])
    revisit = [(y-x)/meta['speed'] for times in buildings.values()
               for x,y in zip(times,times[1:])]
    rates = {f'{name}_commands_nominal_min':sum(x['type'] in types for x in a)/minutes
             for name,types in [('build',{'BUILD'}),('wall',{'WALL'}),
                                ('research',{'RESEARCH'}),('market',{'BUY','SELL'})]}
    return dict(
        core_cpm_nominal=len(c)/minutes,
        move_order_commands=len(m), explicit_actor_commands=len(explicit),
        explicit_actor_coverage=len(explicit)/len(m) if m else None,
        actor_pair_count=len(pairs), same_actor_pair_count=len(same),
        actor_group_size_median=med(sizes),
        actor_group_size_p90=float(np.percentile(sizes,90)) if sizes else None,
        actor_group_ge10_fraction=frac([n>=10 for n in sizes]),
        actor_group_change_fraction=frac(group_changes),
        actor_overlap_jaccard_median=med(overlaps),
        same_actor_gap_nominal_median_s=med([(y['t']-x['t'])/meta['speed'] for x,y in same]),
        same_actor_recommand_under1s_fraction=frac([(y['t']-x['t'])/meta['speed']<1 for x,y in same]),
        commanded_actor_ids=len({oid for x in explicit for oid in x['object_ids']}),
        destination_coordinate_coverage=len(coords)/len(m) if m else None,
        destination_jump_diagonal_median=med(jumps),
        destination_jump_ge_quarter_diagonal_fraction=frac([j>=.25 for j in jumps]),
        valid_target_order_fraction=len(target_orders)/len(orders) if orders else None,
        distinct_order_target_ids=len({x['target_id'] for x in target_orders}),
        distinct_building_type_ids=len({x['building_id'] for x in builds if x.get('building_id') is not None}),
        distinct_research_type_ids=len({x['technology_id'] for x in research if x.get('technology_id') is not None}),
        positive_de_queue_commands=len(queue) if meta['save_version']>=20 else None,
        requested_queue_unit_type_ids=len({x['unit_id'] for x in queue}) if queue else None,
        explicitly_commanded_production_building_ids=len(buildings) if queue else None,
        production_command_revisit_nominal_median_s=med(revisit),
        positive_queue_amount_mean=float(np.mean([x['amount'] for x in queue])) if queue else None,
        **rates)


