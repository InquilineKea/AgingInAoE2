"""Tournament-Elo peer comparison (aoe-elo.com pages saved in tatoh/elo-*.html).

For each focal player: yearly median Elo rank among the 9-player peer set,
gap to the best peer, Elo change since 2022, and series record against the
other 8 peers vs everyone else. Writes tatoh/peer_comparison.txt.
"""
import json, collections, statistics as st, io, contextlib
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]; T=ROOT/'tatoh'
def chart(path):
    s=path.read_text(); i=s.find('{"bands"'); d=0
    for j in range(i,len(s)):
        d+=(s[j]=='{')-(s[j]=='}')
        if d==0: break
    c=json.loads(s[i:j+1]); n=list(c['footers'])[0]; f=c['footers'][n]; ev=c['events'][n]; out=[]
    for k,r in c['series'][0]['data']:
        if k>=len(f) or not f[k]: continue
        e=BeautifulSoup(ev.get(str(k),''),'html.parser').get_text(' ',strip=True).lower()
        opp=e.split('against',1)[1].strip().split()[0] if 'against' in e else None
        out.append(dict(year=int(f[k][-4:]),elo=r,win='victory' in e,loss='defeat' in e,opp=opp))
    return n,out
peers=dict(chart(T/f'elo-{n}.html') for n in ['tatoh','viper','daut','hera','liereyy','mbl','yo','nicov','accm'])
names=sorted(peers); low={n.lower():n for n in names}
med={(n,y):st.median([r['elo'] for r in peers[n] if r['year']==y]) for n in names for y in range(2015,2027) if any(r['year']==y for r in peers[n])}
buf=io.StringIO()
with contextlib.redirect_stdout(buf):
    print('Peer set:',', '.join(names))
    for focal in ['DauT','TheViper','TaToH']:
        print(f'\n== {focal}')
        print('  year  median  rank  gap-to-best  best-peer      vs-peers W-L     vs-others W-L')
        for y in range(2015,2027):
            if (focal,y) not in med: continue
            m={n:med[(n,y)] for n in names if (n,y) in med}
            order=sorted(m,key=lambda n:-m[n]); best=order[0] if order[0]!=focal else (order[1] if len(order)>1 else focal)
            vp=[r for r in peers[focal] if r['year']==y and r['opp'] in low and low[r['opp']]!=focal]
            vo=[r for r in peers[focal] if r['year']==y and not (r['opp'] in low)]
            pw,pl=sum(r['win'] for r in vp),sum(r['loss'] for r in vp); ow,ol=sum(r['win'] for r in vo),sum(r['loss'] for r in vo)
            pct=lambda w,l: f'{100*w/(w+l):3.0f}%' if w+l else '  - '
            print(f"  {y}  {m[focal]:6.0f}  {order.index(focal)+1}/{len(m)}   {m[focal]-max(v for n,v in m.items() if n!=focal):+6.0f}     {best:10}   {pw:2d}-{pl:<2d} {pct(pw,pl)}     {ow:3d}-{ol:<3d} {pct(ow,ol)}")
    print('\n== Change in yearly median Elo, 2021->2026 and 2022->2026')
    for n in sorted(names,key=lambda n:-(med[(n,2026)]-med[(n,2022)])):
        print(f"  {n:9} 2021->26 {med[(n,2026)]-med[(n,2021)]:+5.0f}   2022->26 {med[(n,2026)]-med[(n,2022)]:+5.0f}   peak year {max((y for y in range(2015,2027) if (n,y) in med),key=lambda y:med[(n,y)])}")
out=buf.getvalue(); print(out); (T/'peer_comparison.txt').write_text(out)
