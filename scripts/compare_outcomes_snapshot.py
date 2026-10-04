"""Competitive outcomes from existing local snapshots, separate from command traits."""
import csv,statistics as st,collections,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'deadline-sparse'
def read(p):
 with p.open() as f:return list(csv.DictReader(f))
def write(name,rs):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
main=read(ROOT/'results/game_metrics.csv');tatoh=[r for r in read(ROOT/'tatoh/game_metrics.csv') if r['who']=='TaToH'];games=[]
for r in main:games.append({'player':r['player'],'year':r['year'],'context':r['context'],'cluster':r['cluster'],'outcome':1 if r['winner']=='True' else 0 if r['winner']=='False' else None})
for r in tatoh:games.append({'player':'TaToH','year':r['period'][:4],'context':r['period'][5:],'cluster':r['cluster'],'outcome':1 if r['result']=='win' else 0 if r['result']=='loss' else None})
summary=[]
for player,year,context in sorted({(r['player'],r['year'],r['context']) for r in games}):
 rs=[r for r in games if (r['player'],r['year'],r['context'])==(player,year,context)];valid=[r for r in rs if r['outcome'] is not None];cl=collections.defaultdict(list)
 for r in valid:cl[r['cluster']].append(r['outcome'])
 summary.append({'player':player,'year':year,'context':context,'n_games':len(rs),'known_game_results':len(valid),'wins':sum(r['outcome'] for r in valid),'losses':sum(1-r['outcome'] for r in valid),'game_win_fraction':st.mean(r['outcome'] for r in valid) if valid else None,'equal_cluster_win_fraction':st.mean(st.mean(v) for v in cl.values()) if cl else None,'limit':'Small convenience sample; opponent/context differ. Team results missing. TaToH 2021 series loss does not identify this recovered game outcome.'})
write('sample_outcome_summary.csv',summary)
ratings=read(ROOT/'tatoh/tournament_elo_peers.csv');ratings=[r for r in ratings if r['player'] in ['DauT','TheViper','TaToH']]
ry=[]
for player,year in sorted({(r['player'],r['year']) for r in ratings}):
 rs=[r for r in ratings if r['player']==player and r['year']==year];values=[float(r['elo']) for r in rs]
 ry.append({'player':player,'year':year,'series':len(rs),'elo_median':st.median(values),'elo_min':min(values),'elo_max':max(values),'series_wins':sum(r['win']=='True' for r in rs),'series_losses':sum(r['loss']=='True' for r in rs),'source':'Local aoe-elo.com snapshot collected 2026-10-04; no new live rating lookup','limit':'Elo scale and player pool can change; 2026 partial year; competitive outcome not cognitive trait.'})
write('competitive_rating_years.csv',ry)
comparisons=[]
for player in ['DauT','TheViper','TaToH']:
 rs=sorted([r for r in ry if r['player']==player],key=lambda r:int(r['year']));early,late=rs[0],rs[-1];peak=max(rs,key=lambda r:r['elo_median'])
 comparisons.append({'player':player,'earliest_rating_year':early['year'],'earliest_year_series':early['series'],'earliest_year_median_elo':early['elo_median'],'latest_rating_year':late['year'],'latest_year_series':late['series'],'latest_year_median_elo':late['elo_median'],'highest_year_median_elo':peak['elo_median'],'highest_median_year':peak['year'],'latest_minus_highest_year_median':late['elo_median']-peak['elo_median'],'interpretation':'Separate rating history; earliest rating year can predate available replay. No causal aging inference.'})
write('competitive_rating_endpoints.csv',comparisons)
print(json.dumps(comparisons,indent=2))
