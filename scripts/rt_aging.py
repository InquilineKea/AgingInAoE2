"""Reaction-time-like and other aging-relevant proxies from raw replay commands.

No game state is available, so every measure is a command-timing proxy:

1. Age-up response latency (anticipated stimulus). Arrival = first Feudal/Castle
   research click + 130/160 game s (classic and DE). Response = first command that
   the game only permits after arrival (Feudal: build range/stable/blacksmith/market,
   research Double-Bit Axe/Horse Collar/Man-at-Arms, queue archer/skirm/spear/scout;
   Castle: build TC/castle/monastery/siege workshop/university, research Bow Saw/
   Crossbowman, queue knight/cavalry archer). Latencies <0 (civ age-up bonuses or a
   different first click) or >30 s (TC queue delay / strategic wait) are excluded.
   Persians and Malay games are excluded.
2. Attack-onset response latency. Stimulus = another player's ORDER whose target_id
   is one of the focal player's recently commanded objects, after >=20 s without
   such orders. Response = focal player's first command that names that object or
   whose destination is within 10 tiles of the stimulus location (cap 30 s).
   Includes attacker travel time and the game's alert delay; not pure RT.
3. Switch costs (DE only, timestamps ~0.12 s): median gap after a far spatial jump
   (>= quarter map diagonal) minus after a near command (< 5 tiles); median gap
   after a command-class change minus within the same class. Gaps > 5 s dropped.
4. Corrective re-orders: same explicit unit set re-ordered within 1 s to a point
   > 5 tiles away, per 100 explicit move/orders (DE).
5. Fatigue: core CPM in game minutes 30-40 / minutes 10-20 (games >= 40 min).

All latencies in nominal seconds (game time / recorded speed). Each player is also
measured against the opponent in the same 1v1 game (same map, patch, engine).
"""
import sys, json, csv, math, io, contextlib, collections, statistics as st
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT/'scripts'))
import decode as D
from mgz import fast
_orig = D.de_prefix
D.de_prefix = lambda data, save: _orig(data, 68.9 if 68.0 <= save < 68.9 else save)

CORE = {'MOVE','ORDER','BUILD','RESEARCH','DELETE','BUY','SELL','WALL'}
FIELDS = ['x','y','object_ids','target_id','building_id','technology_id','unit_id','amount']
FEUDAL = dict(BUILD={87,101,103,84}, RESEARCH={202,14,222}, DE_QUEUE={4,7,93,448})
CASTLE = dict(BUILD={621,82,104,49,209}, RESEARCH={203,100}, DE_QUEUE={38,39})
EXCLUDE_CIVS = {8, 29}  # Persians, Malay (age-up / TC speed bonuses)
CLASS = {'MOVE':'unit','ORDER':'unit','BUILD':'build','WALL':'build','RESEARCH':'prod',
         'DE_QUEUE':'prod','BUY':'market','SELL':'market','DELETE':'other'}

def body(path, meta):
    acts, ts = [], 0
    with path.open('rb') as f:
        f.seek(meta['body_start']); fast.meta(f); size = path.stat().st_size
        while f.tell() < size:
            try: op, p = fast.operation(f)
            except EOFError: break
            if op is fast.Operation.SYNC: ts += p[0]
            elif op is fast.Operation.ACTION:
                typ, pl = p
                acts.append(dict(t=ts/1000, type=typ.name, player=pl.get('player_id'),
                                 **{k: pl[k] for k in FIELDS if k in pl}))
    return acts

def gated_latency(A, click_tech, dur_s, gate, speed):
    click = next((a['t'] for a in A if a['type'] == 'RESEARCH' and a.get('technology_id') == click_tech), None)
    if click is None: return None
    arrive = click + dur_s
    first = next((a['t'] for a in A if a['t'] >= click and a.get(
        {'BUILD':'building_id','RESEARCH':'technology_id','DE_QUEUE':'unit_id'}.get(a['type'], '_')) in gate.get(a['type'], ())), None)
    if first is None: return None
    lat = (first - arrive)/speed
    return lat if 0 <= lat <= 30 else ('out', lat)

def attack_onsets(acts, me, speed):
    mine = [a for a in acts if a['player'] == me]
    others = [a for a in acts if a['player'] not in (me, None) and a['type'] == 'ORDER'
              and a.get('target_id') not in (None, -1)]
    last_seen = {}; i = 0; out = []; last_hit = -1e9
    mine_sorted = sorted(mine, key=lambda a: a['t'])
    for s in sorted(others, key=lambda a: a['t']):
        while i < len(mine_sorted) and mine_sorted[i]['t'] <= s['t']:
            for o in mine_sorted[i].get('object_ids') or []: last_seen[o] = mine_sorted[i]['t']
            i += 1
        tgt = s['target_id']
        if tgt not in last_seen or s['t'] - last_seen[tgt] > 180: continue
        onset = s['t'] - last_hit >= 20
        last_hit = s['t']
        if not onset or s['t'] < 120: continue
        resp = None
        for a in mine_sorted[i:]:
            if (a['t'] - s['t'])/speed > 30: break
            if a['t'] <= s['t']: continue
            if tgt in (a.get('object_ids') or []) or (a.get('x') is not None and s.get('x') is not None
                    and math.hypot(a['x']-s['x'], a['y']-s['y']) <= 10 and a['type'] in ('MOVE','ORDER','PATROL','DE_ATTACK_MOVE','BUILD','UNGARRISON','STOP')):
                resp = (a['t'] - s['t'])/speed; break
        out.append(resp)
    return out

def per_player(acts, me, speed, dur, de):
    A = sorted([a for a in acts if a['player'] == me], key=lambda a: a['t'])
    C = [a for a in A if a['type'] in CORE]
    r = {}
    r['feudal_resp'] = gated_latency(A, 101, 130, FEUDAL, speed)
    r['castle_resp'] = gated_latency(A, 102, 160, CASTLE, speed)
    on = attack_onsets(acts, me, speed)
    lat = [x for x in on if x is not None]
    r['attack_onsets'] = len(on); r['attack_resp_median'] = st.median(lat) if lat else None
    r['attack_resp_within30'] = len(lat)/len(on) if on else None
    r['attack_resp_list'] = lat
    if de:
        far, near, sw, same = [], [], [], []
        P = [a for a in A if a['type'] in CLASS]
        for a, b in zip(P, P[1:]):
            g = (b['t']-a['t'])/speed
            if g > 5: continue
            (sw if CLASS[a['type']] != CLASS[b['type']] else same).append(g)
            if a['type'] in CORE and b['type'] in CORE and a.get('x') is not None and b.get('x') is not None:
                d = math.hypot(a['x']-b['x'], a['y']-b['y'])
                if d >= 0.25*math.sqrt(2)*120: far.append(g)
                elif d < 5: near.append(g)
        r['spatial_switch_cost'] = st.median(far)-st.median(near) if len(far) > 10 and len(near) > 10 else None
        r['task_switch_cost'] = st.median(sw)-st.median(same) if len(sw) > 10 and len(same) > 10 else None
        mo = [a for a in A if a['type'] in ('MOVE','ORDER') and a.get('object_ids') and a.get('x') is not None]
        corr = sum(1 for a, b in zip(mo, mo[1:]) if set(a['object_ids']) == set(b['object_ids'])
                   and (b['t']-a['t'])/speed <= 1 and math.hypot(a['x']-b['x'], a['y']-b['y']) > 5)
        r['corrections_per100'] = 100*corr/len(mo) if len(mo) > 30 else None
    cpm = lambda t0, t1: sum(t0 <= a['t'] < t1 for a in C)/((t1-t0)/speed/60)
    r['fatigue_ratio'] = cpm(1800, 2400)/cpm(600, 1200) if dur >= 2400 and cpm(600, 1200) > 0 else None
    return r

# ---- game list
games = []
man = {g['game_id']: g for g in json.load(open(ROOT/'results/manifest.json'))}
for r in csv.DictReader(open(ROOT/'results/game_metrics.csv')):
    g = man[r['game_id']]
    games.append(dict(path=ROOT/g['file'], player=r['player'], period=f"{r['year']} {r['context']}",
                      cluster=r['cluster'], slot=int(r['player_slot']), civ=int(r['civilization_id']),
                      date=r['date'][:10]))
seen = set()
for r in csv.DictReader(open(ROOT/'tatoh/game_metrics.csv')):
    if r['who'] != 'TaToH' or r['game'] in seen: continue
    seen.add(r['game'])
    p = next(x for x in (ROOT/'tatoh/raw'/r['game']).iterdir() if x.suffix == '.aoe2record')
    games.append(dict(path=p, player='TaToH', period=r['period'], cluster=r['cluster'], slot=None, civ=None, date=r['date'][:10]))

rows = []; pooled = collections.defaultdict(list)
for g in games:
    meta, _ = D.decode(g['path'])
    acts = body(g['path'], meta)
    de = meta['save_version'] >= 20
    if g['slot'] is None:
        g['slot'] = next(p['number'] for p in meta['players'] if p.get('profile_id') == 197388 or p['name'] == 'Le Loi')
    civ = {p['number']: p.get('civilization_id') for p in meta['players']}
    nplay = len(meta['players'])
    opp = [p['number'] for p in meta['players'] if p['number'] != g['slot']][0] if nplay == 2 else None
    for who, num in [('focal', g['slot'])] + ([('opponent', opp)] if opp else []):
        r = per_player(acts, num, meta['speed'], meta['duration_s'], de)
        if (civ.get(num) or g['civ']) in EXCLUDE_CIVS: r['feudal_resp'] = r['castle_resp'] = None
        row = dict(player=g['player'], period=g['period'], cluster=g['cluster'], game=g['path'].stem[:40], who=who, de=de,
                   one_v_one=nplay == 2, dur_min=round(meta['duration_s']/60, 1))
        for k, v in r.items():
            if k == 'attack_resp_list': continue
            if isinstance(v, tuple): row[k] = None; row[k+'_excluded'] = round(v[1], 1)
            else: row[k] = v
        rows.append(row)
        if who == 'focal': pooled[(g['player'], g['period'])] += r['attack_resp_list']

keys = ['feudal_resp','castle_resp','attack_resp_median','attack_resp_within30','spatial_switch_cost',
        'task_switch_cost','corrections_per100','fatigue_ratio']
allk = sorted({k for r in rows for k in r})
with open(ROOT/'rt-proxies/rt_aging_games.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=allk); w.writeheader(); w.writerows(rows)

def wmed(G, k):
    cl = collections.Counter(r['cluster'] for r in G if r.get(k) is not None)
    pairs = sorted((r[k], 1/cl[r['cluster']]) for r in G if r.get(k) is not None)
    if not pairs: return None, 0
    tot = sum(w for _, w in pairs); c = 0
    for v, w in pairs:
        c += w
        if c >= tot/2: return v, len(pairs)

order = [('DauT','2011 1v1 challenge'),('DauT','2012 team game'),('DauT','2021 1v1 tournament'),('DauT','2026 1v1 ranked'),
         ('TheViper','2012 team game'),('TheViper','2021 1v1 tournament'),('TheViper','2026 1v1 ranked'),
         ('TaToH','2021 tournament'),('TaToH','2026 tournament'),('TaToH','2026 ranked')]
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    print('== Focal player, cluster-weighted median (n games with a value)')
    print('  '+'group'.ljust(32)+''.join(f'{k[:16]:>18}' for k in keys))
    for p, per in order:
        G = [r for r in rows if r['player'] == p and r['period'] == per and r['who'] == 'focal']
        cells = []
        for k in keys:
            v, n = wmed(G, k)
            cells.append(f"{v:12.2f} (n{n:2d})" if v is not None else f"{'-':>12} (n{n:2d})")
        print('  '+f'{p} {per}'.ljust(32)+''.join(f'{c:>18}' for c in cells))
    print('\n== Pooled attack-onset response latencies (focal, all onsets with a response)')
    for p, per in order:
        L = pooled[(p, per)]
        if L: print(f"  {p:8} {per:22} n={len(L):4d}  p25={np.percentile(L,25):5.2f}  median={np.median(L):5.2f}  p75={np.percentile(L,75):5.2f}")
    print('\n== Age-up response excluded as out of range (count)')
    for p, per in order:
        G = [r for r in rows if r['player'] == p and r['period'] == per and r['who'] == 'focal']
        print(f"  {p:8} {per:22} feudal kept {sum(r.get('feudal_resp') is not None for r in G)}/{len(G)}, out-of-range {sum('feudal_resp_excluded' in r for r in G)};"
              f" castle kept {sum(r.get('castle_resp') is not None for r in G)}, out-of-range {sum('castle_resp_excluded' in r for r in G)}")
    print('\n== Focal minus opponent, same 1v1 game (median of per-game differences)')
    for p, per in order:
        diffs = collections.defaultdict(list)
        for gname in {r['game'] for r in rows if r['player'] == p and r['period'] == per and r['one_v_one']}:
            a = next((r for r in rows if r['game'] == gname and r['player'] == p and r['who'] == 'focal'), None)
            b = next((r for r in rows if r['game'] == gname and r['player'] == p and r['who'] == 'opponent'), None)
            if not a or not b: continue
            for k in keys:
                if a.get(k) is not None and b.get(k) is not None: diffs[k].append(a[k]-b[k])
        if diffs:
            print(f"  {p:8} {per:22} " + '  '.join(f"{k.split('_')[0]}_{k.split('_')[1][:4]}={st.median(v):+.2f}(n{len(v)})" for k, v in diffs.items()))
out = buf.getvalue(); print(out); (ROOT/'rt-proxies/rt_aging_results.txt').write_text(out)
