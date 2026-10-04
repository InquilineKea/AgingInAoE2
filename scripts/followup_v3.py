"""Follow-up descriptive analysis of the reanalysis-v2 command log (matched game-time
bins, DE timing tails, rapid re-clicks, age-up timing, same-era player ratio,
exact permutation tests) plus tournament and ladder rating summaries.
Writes reanalysis-v2/followup_results.txt. Run with the artifact .venv python."""
import gzip,json,csv,collections,itertools,math,io,contextlib,statistics as st
from pathlib import Path
import numpy as np
B=str(Path(__file__).resolve().parents[1])+'/'
_buf=io.StringIO(); _ctx=contextlib.redirect_stdout(_buf); _ctx.__enter__()
man={g['game_id']:g for g in json.load(open(B+'results/manifest.json'))}
meta={(r['game_id'],r['player']):r for r in csv.DictReader(open(B+'results/game_metrics.csv'))}
acts=collections.defaultdict(list)
for l in gzip.open(B+'reanalysis-v2/detailed_actions.jsonl.gz','rt'):
    a=json.loads(l); acts[(a['game_id'],a['target_player'])].append(a)
CORE={'MOVE','ORDER','BUILD','RESEARCH','DELETE','BUY','SELL','WALL'}
games=[]
for k,A in acts.items():
    A.sort(key=lambda a:(a['t'],a['sequence']))
    r=meta[k]; g=man[k[0]]
    games.append(dict(gid=k[0],p=k[1],y=int(r['year']),ctx=r['context'],cl=r['cluster'],sp=g['speed'],
        dur=float(r['duration_game_min'])*60,win=r['winner'],date=r['date'],A=A,
        core=[a for a in A if a['type'] in CORE]))
def med(x): x=[v for v in x if v==v]; return float(np.median(x)) if x else float('nan')
def grp(p,y): return [g for g in games if g['p']==p and g['y']==y]
PY=[('DauT',2011),('DauT',2012),('DauT',2021),('DauT',2026),('TheViper',2012),('TheViper',2021),('TheViper',2026)]
def cpm(g,t0,t1):
    n=sum(1 for a in g['core'] if t0<=a['t']<t1); return n/((t1-t0)/g['sp']/60)
print('== 0. sanity: opening core CPM (nominal) medians')
for p,y in PY: print(p,y,round(med([cpm(g,0,600) for g in grp(p,y)]),2))

print('\n== 1. matched game-time bins: median core CPM (n games reaching bin end)')
bins=[(0,5),(5,10),(10,15),(15,20),(20,25),(25,30),(30,40)]
for p,y in PY:
    row=[]
    for b0,b1 in bins:
        G=[g for g in grp(p,y) if g['dur']>=b1*60]
        row.append(f"{b0}-{b1}:{med([cpm(g,b0*60,b1*60) for g in G]):6.1f}(n{len(G)})" if G else f"{b0}-{b1}:   -  ")
    print(f"{p:8} {y}  "+'  '.join(row))
print('   duration (game min) per game:')
for p,y in PY: print('  ',p,y,sorted(round(g['dur']/60) for g in grp(p,y)))
# per-game: final-5-min CPM vs rest (end-game flurry?)
print('\n== 1b. CPM in last 5 game-min vs game minutes 10-20, per game (DE)')
for p,y in [('DauT',2021),('DauT',2026),('TheViper',2021),('TheViper',2026)]:
    L=[];M=[]
    for g in grp(p,y):
        if g['dur']>=25*60: L.append(cpm(g,g['dur']-300,g['dur'])); M.append(cpm(g,600,1200))
    print(' ',p,y,'last5',[round(x) for x in L],'min10-20',[round(x) for x in M])

print('\n== 2. DE timing distribution of core commands (nominal s), windows 0-10 and 10-20 game min')
def gaps(g,t0,t1):
    ts=[a['t'] for a in g['core'] if t0<=a['t']<t1]
    return np.diff(ts)/g['sp']
def lapse(g,t0,t1,w=5.0):
    # fraction of nominal-w-second windows with no core command
    ts=np.array([a['t'] for a in g['core'] if t0<=a['t']<t1])/g['sp']
    edges=np.arange(t0/g['sp'],t1/g['sp'],w); h=np.histogram(ts,bins=np.append(edges,t1/g['sp']))[0]
    return float(np.mean(h==0))
def burst(g,t0,t1,w=10.0):
    ts=np.array([a['t'] for a in g['core'] if t0<=a['t']<t1])/g['sp']
    j=np.searchsorted(ts,ts+w); return float(np.max(j-np.arange(len(ts))))*60/w if len(ts) else float('nan')
for (t0,t1) in [(0,600),(600,1200)]:
    print(f' window {t0//60}-{t1//60} game min')
    for p,y in [('DauT',2021),('DauT',2026),('TheViper',2021),('TheViper',2026)]:
        G=[g for g in grp(p,y) if g['dur']>=t1]
        q=lambda f: med([f(g) for g in G])
        print(f"  {p:8} {y} n={len(G)}  gap p50={q(lambda g:np.percentile(gaps(g,t0,t1),50)):.3f}  p90={q(lambda g:np.percentile(gaps(g,t0,t1),90)):.2f}  p99={q(lambda g:np.percentile(gaps(g,t0,t1),99)):.2f}  pos-gap p10={q(lambda g:np.percentile([x for x in gaps(g,t0,t1) if x>0],10)):.3f}  silent5s={q(lambda g:lapse(g,t0,t1)):.3f}  peak10s_cpm={q(lambda g:burst(g,t0,t1)):.0f}")

print('\n== 3. rapid re-clicks: MOVE/ORDER within <=0.5 nominal s of previous MOVE/ORDER and destination <=2 tiles (or same target)')
def reclick(g,t0,t1):
    mo=[a for a in g['core'] if a['type'] in('MOVE','ORDER') and t0<=a['t']<t1 and 'x' in a]
    n=0
    for a,b in zip(mo,mo[1:]):
        if (b['t']-a['t'])/g['sp']<=0.5 and (math.hypot(a['x']-b['x'],a['y']-b['y'])<=2 or (a.get('target_id',-1)>=0 and a.get('target_id')==b.get('target_id'))): n+=1
    core=sum(1 for a in g['core'] if t0<=a['t']<t1)
    return n/core, (core-n)/((t1-t0)/g['sp']/60)
for (t0,t1,lab) in [(0,600,'0-10'),(0,None,'whole')]:
    for p,y in PY:
        G=grp(p,y)
        R=[reclick(g,t0,t1 or g['dur']+1) for g in G]
        print(f"  {lab:5} {p:8} {y}  reclick share={med([r[0] for r in R]):.3f}  dedup CPM={med([r[1] for r in R]):6.1f}  raw CPM={med([cpm(g,t0,t1 or g['dur']+1) for g in G]):6.1f}")

print('\n== 4. milestones (game time mm:ss; first click) ')
def fmt(s): return '  -  ' if s is None else f"{int(s//60):2d}:{int(s%60):02d}"
def first(g,pred):
    for a in g['A']:
        if pred(a): return a['t']
VIL={83,293}
for p,y in PY:
    print(f' {p} {y}')
    for g in sorted(grp(p,y),key=lambda g:g['date']):
        f=first(g,lambda a:a['type']=='RESEARCH' and a.get('technology_id')==101)
        c=first(g,lambda a:a['type']=='RESEARCH' and a.get('technology_id')==102)
        i=first(g,lambda a:a['type']=='RESEARCH' and a.get('technology_id')==103)
        mil={12:'rax',87:'range',101:'stable'}
        fm=[(a['t'],mil[a['building_id']]) for a in g['A'] if a['type']=='BUILD' and a.get('building_id') in mil]
        fm=fm[0] if fm else (None,'')
        print(f"   {g['gid'][:6]} win={g['win'] or '?':5} dur={g['dur']/60:5.1f}  feudal {fmt(f)}  castle {fmt(c)}  imp {fmt(i)}  1st mil bldg {fmt(fm[0])} {fm[1]:6}")

print('\n== 5. 2026 session order')
for p in ['DauT','TheViper']:
    for n,g in enumerate(sorted(grp(p,2026),key=lambda g:g['date']),1):
        print(f"  {p} game{n} {g['date'][11:16]}  open CPM={cpm(g,0,600):6.1f}  10-20 CPM={cpm(g,600,1200) if g['dur']>=1200 else float('nan'):6.1f}  win={g['win']}")

print('\n== 6. Viper/DauT opening CPM ratio, same era')
for y in [2012,2021,2026]:
    d=med([cpm(g,0,600) for g in grp('DauT',y)]); v=med([cpm(g,0,600) for g in grp('TheViper',y)])
    print(f'  {y}: DauT {d:.1f}  Viper {v:.1f}  ratio {v/d:.2f}')
pair=[(g, h) for g in grp('DauT',2012) for h in grp('TheViper',2012) if g['gid']==h['gid']]
print('  2012 same-game pairs ratio:',[round(cpm(h,0,600)/cpm(g,0,600),2) for g,h in pair])

print('\n== 7. exact permutation test 2021 vs 2026 (game-level; ignores series clustering -> anti-conservative)')
def perm(a,b):
    obs=np.median(b)-np.median(a); x=np.array(a+b); n=len(a); cnt=tot=0
    for idx in itertools.combinations(range(len(x)),n):
        m=np.zeros(len(x),bool); m[list(idx)]=True
        d=np.median(x[~m])-np.median(x[m]); tot+=1; cnt+= abs(d)>=abs(obs)-1e-9
    # cliff's delta
    cd=np.mean([np.sign(j-i) for i in a for j in b])
    return obs,cnt/tot,cd
for p in ['DauT','TheViper']:
    A=grp(p,2021);Bb=grp(p,2026)
    for lab,f in [('open CPM',lambda g:cpm(g,0,600)),('min10-20 CPM',lambda g:cpm(g,600,1200) if g['dur']>=1200 else None),('whole CPM',lambda g:cpm(g,0,g['dur']+1))]:
        a=[f(g) for g in A if f(g) is not None]; b=[f(g) for g in Bb if f(g) is not None]
        o,pv,cd=perm(a,b); print(f'  {p:8} {lab:13} n={len(a)}v{len(b)}  median diff={o:+6.1f}  p={pv:.3f}  cliffs_delta={cd:+.2f}')

print('\n== 8. tournament Elo (aoe-elo.com series data, results/tournament_years.csv)')
for r in csv.DictReader(open(B+'results/tournament_years.csv')):
    if int(r['year'])>=2019: print(f"  {r['player']:8} {r['year']}  series={r['series']:>3}  median={float(r['elo_median']):6.0f}  max={r['elo_max']}  last={r['elo_last']}  win%={100*float(r['series_win_fraction']):.0f}")
print('\n== 9. RM 1v1 ladder rating (aoe2companion snapshot 2026-10-04, reanalysis-v2/ladder_rm1v1_history.csv)')
L=collections.defaultdict(lambda:collections.defaultdict(list))
for r in csv.DictReader(open(B+'reanalysis-v2/ladder_rm1v1_history.csv')): L[r['player']][r['date_utc'][:4]].append(int(r['rating']))
for p,by in L.items():
    allr=[(y,v) for y in by for v in by[y]]
    print(f"  {p}: peak {max(v for _,v in allr)}, latest {list(by.values())[-1][-1]}")
    for y,v in sorted(by.items()): print(f"    {y}: n={len(v):4d}  median={st.median(v):6.0f}  max={max(v)}  year-end={v[-1]}")
_ctx.__exit__(None,None,None)
out=_buf.getvalue(); print(out)
(Path(B)/'reanalysis-v2'/'followup_results.txt').write_text(out)
