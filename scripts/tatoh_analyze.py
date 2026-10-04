"""TaToH replay and rating analysis (descriptive; no cognitive measures).

Inputs: tatoh/raw (from fetch_tatoh.py), tatoh/aoe2companion_matches_*.json,
tatoh/elo-*.html (aoe-elo.com pages), reanalysis-v2/detailed_actions.jsonl.gz
(DauT/TheViper reference). Outputs: tatoh/game_metrics.csv, tatoh/results.txt.

Identity: TaToH is located by profile 197388 (2026) or the HC4 alias "Le Loi"
(alias reveal on the ageofnotes HC4 page). Files without TaToH are excluded.
Games under 5 game minutes are treated as restarts and excluded.
Weighting: each series/session-day gets equal weight inside a period; each
game inside a cluster gets equal weight (weighted medians).
"""
import sys, json, gzip, csv, math, io, contextlib, collections, statistics as st
from pathlib import Path
import numpy as np
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]
T = ROOT/'tatoh'
sys.path.insert(0, str(ROOT/'scripts'))
import decode as D
from mgz import fast

_orig = D.de_prefix
def _prefix(data, save):
    # 68.0 recordings carry the same per-player trailing empty string as 68.9;
    # the existing asserts (empty string, slot numbers, colors) still apply.
    return _orig(data, 68.9 if 68.0 <= save < 68.9 else save)
D.de_prefix = _prefix

CORE = {'MOVE','ORDER','BUILD','RESEARCH','DELETE','BUY','SELL','WALL'}
FIELDS = ['x','y','object_ids','target_id','building_id','technology_id','unit_id','amount']
TATOH = 197388

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

def wmed(vals, w):
    pairs = sorted((v, x) for v, x in zip(vals, w) if v == v and v is not None)
    if not pairs: return float('nan')
    tot = sum(x for _, x in pairs); c = 0
    for v, x in pairs:
        c += x
        if c >= tot/2: return v

def metrics(acts, num, speed, dur):
    A = sorted([a for a in acts if a['player'] == num], key=lambda a: a['t'])
    C = [a for a in A if a['type'] in CORE]
    def cpm(t0, t1):
        if dur < t1: return float('nan')
        return sum(t0 <= a['t'] < t1 for a in C) / ((t1-t0)/speed/60)
    def gaps(t0, t1):
        ts = [a['t'] for a in C if t0 <= a['t'] < t1]
        return np.diff(ts)/speed
    def reclick(t0, t1):
        mo = [a for a in C if a['type'] in ('MOVE','ORDER') and t0 <= a['t'] < t1 and a.get('x') is not None]
        n = sum(1 for a, b in zip(mo, mo[1:]) if (b['t']-a['t'])/speed <= .5 and
                (math.hypot(a['x']-b['x'], a['y']-b['y']) <= 2 or
                 (a.get('target_id', -1) not in (None, -1) and a.get('target_id') == b.get('target_id'))))
        core = sum(t0 <= a['t'] < t1 for a in C)
        return (n/core if core else float('nan')), (core-n)/((t1-t0)/speed/60)
    first = lambda tech: next((a['t'] for a in A if a['type'] == 'RESEARCH' and a.get('technology_id') == tech), None)
    g10 = gaps(0, 600); g1020 = gaps(600, 1200) if dur >= 1200 else np.array([])
    rs, dd = reclick(0, 600)
    rsw, ddw = reclick(0, dur+1)
    out = dict(open_cpm=cpm(0, 600), cpm_0_5=cpm(0, 300), cpm_5_10=cpm(300, 600), cpm_10_15=cpm(600, 900),
               cpm_15_20=cpm(900, 1200), cpm_10_20=cpm(600, 1200),
               whole_cpm=len(C)/(dur/speed/60), reclick_open=rs, dedup_open_cpm=dd,
               reclick_whole=rsw, dedup_whole_cpm=ddw,
               gap_p50_open=float(np.percentile(g10, 50)) if len(g10) else float('nan'),
               gap_p90_open=float(np.percentile(g10, 90)) if len(g10) else float('nan'),
               gap_p99_open=float(np.percentile(g10, 99)) if len(g10) else float('nan'),
               gap_p99_10_20=float(np.percentile(g1020, 99)) if len(g1020) else float('nan'),
               feudal_s=first(101), castle_s=first(102), imperial_s=first(103))
    return out

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    listing = json.loads(next(T.glob('aoe2companion_matches_*.json')).read_text())
    won = {}
    for lb, ms in listing.items():
        for m in ms:
            for t in m['teams']:
                for p in t['players']:
                    if p['profileId'] == TATOH: won[str(m['matchId'])] = p.get('won')
    rows, excluded = [], []
    for path in sorted(T.glob('raw/*/*')):
        if path.suffix not in ('.aoe2record', '.mgz'): continue
        name = path.parent.name
        try:
            meta, _ = D.decode(path)
        except Exception as e:
            excluded.append((name, 'decode failed: '+type(e).__name__)); continue
        ps = meta['players']
        me = [p for p in ps if p.get('profile_id') == TATOH or p['name'] == 'Le Loi']
        if not me: excluded.append((name, 'TaToH not a player: '+', '.join(p['name'] for p in ps))); continue
        if len(ps) != 2: excluded.append((name, 'not 1v1')); continue
        if meta['duration_s'] < 300: excluded.append((name, f"restart ({meta['duration_s']/60:.1f} min)")); continue
        me = me[0]; opp = [p for p in ps if p is not me][0]
        acts = body(path, meta)
        mid = name.split('_')[-1]
        if name.startswith('hc4'):
            period, cluster, date, result = '2021 tournament', 'HC4 Ro16 vs Hera', '2021-03', 'loss (series)'
        else:
            period = '2026 tournament' if name.startswith('lobby') else '2026 ranked'
            date = meta.get('date_utc', '')[:16]
            cluster = (f"vs {opp['name']}" if period == '2026 tournament' else 'day '+date[:10])
            result = {True: 'win', False: 'loss', None: '?'}[won.get(mid)]
        partial = 'PARTIAL' in path.name
        for who, p in [('TaToH', me), ('opponent', opp)]:
            m = metrics(acts, p['number'], meta['speed'], meta['duration_s'])
            rows.append(dict(game=name, period=period, cluster=cluster, date=date, who=who, name=p['name'],
                             opponent=opp['name'] if who == 'TaToH' else me['name'], result=result,
                             dur_min=round(meta['duration_s']/60, 1), partial=partial,
                             save=meta['save_version'], **m))
    with open(T/'game_metrics.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

    print('== Excluded files'); [print('  ', n, '-', r) for n, r in excluded]
    me = [r for r in rows if r['who'] == 'TaToH']
    print('\n== Included TaToH games');
    for per in ['2021 tournament', '2026 tournament', '2026 ranked']:
        G = [r for r in me if r['period'] == per]
        cl = collections.Counter(r['cluster'] for r in G)
        print(f"  {per}: {len(G)} games, {len(cl)} clusters, W-L {sum(r['result']=='win' for r in G)}-{sum(r['result']=='loss' for r in G)}  {dict(cl)}")

    keys = [('open_cpm','opening CPM'),('cpm_5_10','CPM 5-10'),('cpm_10_20','CPM 10-20'),('whole_cpm','whole CPM'),
            ('reclick_open','re-click share open'),('dedup_open_cpm','dedup open CPM'),('dedup_whole_cpm','dedup whole CPM'),
            ('gap_p50_open','gap p50 open s'),('gap_p90_open','gap p90 open s'),('gap_p99_10_20','gap p99 10-20 s'),
            ('feudal_s','Feudal click s'),('castle_s','Castle click s')]
    print('\n== TaToH, cluster-weighted medians (each series/day equal weight)')
    print('  metric'.ljust(26)+''.join(f'{p:>18}' for p in ['2021 tournament','2026 tournament','2026 ranked']))
    for k, lab in keys:
        line = '  '+lab.ljust(24)
        for per in ['2021 tournament', '2026 tournament', '2026 ranked']:
            G = [r for r in me if r['period'] == per]
            cl = collections.Counter(r['cluster'] for r in G)
            v = wmed([r[k] if r[k] is not None else float('nan') for r in G], [1/cl[r['cluster']] for r in G])
            line += f'{v:18.2f}' if v == v else f"{'-':>18}"
        print(line)

    print('\n== Same-game paired difference, TaToH minus opponent (median over games)')
    for per in ['2021 tournament', '2026 tournament', '2026 ranked']:
        diffs = collections.defaultdict(list)
        for g in {r['game'] for r in rows if r['period'] == per}:
            a = next(r for r in rows if r['game'] == g and r['who'] == 'TaToH'); b = next(r for r in rows if r['game'] == g and r['who'] == 'opponent')
            for k in ['open_cpm', 'cpm_10_20', 'dedup_open_cpm', 'feudal_s']:
                if a[k] is not None and b[k] is not None and a[k] == a[k] and b[k] == b[k]: diffs[k].append(a[k]-b[k])
        print(f"  {per:16}"+'  '.join(f"{k}={st.median(v):+.1f} (n{len(v)})" for k, v in diffs.items()))

    print('\n== Fixed matchup anchor: TaToH vs Hera, 2021 HC4 g1 vs 2026 ranked (Sep 22)')
    for g in ['hc4_tatoh_vs_hera', 'ranked_508468284']:
        a = next(r for r in rows if r['game'] == g and r['who'] == 'TaToH'); b = next(r for r in rows if r['game'] == g and r['who'] == 'opponent')
        print(f"  {g:20} dur={a['dur_min']:5.1f}  TaToH open {a['open_cpm']:6.1f} / 10-20 {a['cpm_10_20']:6.1f} / dedup open {a['dedup_open_cpm']:5.1f} / feudal {a['feudal_s'] or float('nan'):5.0f}s"
              f"   Hera open {b['open_cpm']:6.1f} / 10-20 {b['cpm_10_20']:6.1f} / dedup open {b['dedup_open_cpm']:5.1f} / feudal {b['feudal_s'] or float('nan'):5.0f}s   ratio T/H open {a['open_cpm']/b['open_cpm']:.2f}")

    print('\n== Reference: DauT / TheViper (same metric code on reanalysis-v2 commands), medians')
    acts = collections.defaultdict(list); meta = {}
    man = {g['game_id']: g for g in json.load(open(ROOT/'results/manifest.json'))}
    gm = {(r['game_id'], r['player']): r for r in csv.DictReader(open(ROOT/'results/game_metrics.csv'))}
    for l in gzip.open(ROOT/'reanalysis-v2/detailed_actions.jsonl.gz', 'rt'):
        a = json.loads(l); acts[(a['game_id'], a['target_player'])].append(a)
    ref = collections.defaultdict(list)
    for (gid, pl), A in acts.items():
        r = gm[(gid, pl)]
        if r['year'] not in ('2021', '2026'): continue
        num = A[0]['player']
        ref[(pl, r['year'])].append(metrics(A, num, man[gid]['speed'], float(r['duration_game_min'])*60))
    for (pl, y), M in sorted(ref.items()):
        print(f"  {pl:8} {y} n={len(M)}  open {st.median([m['open_cpm'] for m in M]):6.1f}  10-20 {np.nanmedian([m['cpm_10_20'] for m in M]):6.1f}  dedup open {st.median([m['dedup_open_cpm'] for m in M]):5.1f}  reclick {st.median([m['reclick_open'] for m in M]):.2f}  feudal {np.nanmedian([m['feudal_s'] or np.nan for m in M]):4.0f}s")

    print('\n== Tournament Elo (aoe-elo.com) yearly medians and TaToH rank among 9 peers')
    def chart(path):
        s = Path(path).read_text(); i = s.find('{"bands"'); d = 0
        for j in range(i, len(s)):
            d += (s[j] == '{') - (s[j] == '}')
            if d == 0: break
        c = json.loads(s[i:j+1]); n = list(c['footers'])[0]; f = c['footers'][n]; ev = c['events'][n]; out = []
        for k, r in c['series'][0]['data']:
            if k >= len(f) or not f[k]: continue
            e = BeautifulSoup(ev.get(str(k), ''), 'html.parser').get_text(' ', strip=True)
            out.append(dict(player=n, year=int(f[k][-4:]), elo=r, ev=e))
        return out
    peers = {}
    for n in ['tatoh', 'viper', 'daut', 'hera', 'liereyy', 'mbl', 'yo', 'nicov', 'accm']:
        rs = chart(T/f'elo-{n}.html'); peers[rs[0]['player']] = rs
    names = sorted(peers)
    print('  year '+''.join(f'{n:>9}' for n in names)+'  TaToH rank  TaToH-best')
    for y in range(2018, 2027):
        meds = {n: st.median([r['elo'] for r in peers[n] if r['year'] == y]) for n in names if any(r['year'] == y for r in peers[n])}
        rank = sorted(meds, key=lambda n: -meds[n]).index('TaToH')+1
        print(f'  {y} '+''.join(f"{meds.get(n, float('nan')):9.0f}" for n in names)+f'  {rank}/{len(meds)}  {meds["TaToH"]-max(meds.values()):+6.0f}')
    print('\n== TaToH tournament series record vs these 8 peers, by year')
    peer_names = {n.lower() for n in names if n != 'TaToH'} | {'theviper', 'viper'}
    rec = collections.defaultdict(lambda: [0, 0])
    for r in peers['TaToH']:
        e = r['ev'].lower()
        if 'against' not in e: continue
        opp = e.split('against', 1)[1].strip().split()[0]
        if opp in peer_names:
            rec[r['year']][0 if 'victory' in e else 1] += 1 if ('victory' in e or 'defeat' in e) else 0
    allw = collections.defaultdict(lambda: [0, 0])
    for r in peers['TaToH']:
        e = r['ev'].lower()
        if 'victory' in e: allw[r['year']][0] += 1
        elif 'defeat' in e: allw[r['year']][1] += 1
    for y in range(2018, 2027):
        w, l = rec[y]; aw, al = allw[y]
        print(f"  {y}: vs peers {w}-{l}" + (f" ({100*w/(w+l):.0f}%)" if w+l else '') + f"   all series {aw}-{al} ({100*aw/max(aw+al,1):.0f}%)")

out = buf.getvalue(); print(out); (T/'results.txt').write_text(out)
