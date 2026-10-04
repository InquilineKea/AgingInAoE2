"""Offline report for the native command reanalysis and Mac compatibility checks."""
from pathlib import Path
import base64, html, json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reanalysis-v2'
df=pd.read_csv(OUT/'game_features.csv')
summary=pd.read_csv(OUT/'period_summary.csv')
validation=json.loads((OUT/'validation.json').read_text())
assert validation['unique_games']==37 and validation['player_game_observations']==44
opening=df[df.window=='first 10 game minutes']
fig,axs=plt.subplots(2,2,figsize=(11,7),constrained_layout=True)
rng=np.random.default_rng(29)
for row,player in enumerate(['DauT','TheViper']):
    for col,(key,label,mult) in enumerate([
        ('core_cpm_nominal','Core commands per nominal minute',1),
        ('destination_jump_ge_quarter_diagonal_fraction','Large destination jumps (%)',100)]):
        ax=axs[row,col]
        for i,year in enumerate([2011,2012,2021,2026]):
            x=opening[(opening.player==player)&(opening.year==year)][key].dropna()*mult
            if len(x):
                ax.scatter(i+rng.uniform(-.12,.12,len(x)),x,s=25,color='#397c9c',alpha=.65)
                ax.plot([i-.2,i+.2],[x.median()]*2,color='#b65723',lw=3)
                ax.annotate(f'n={len(x)}',(i,float(x.max())),xytext=(0,7),textcoords='offset points',ha='center',fontsize=9)
        ax.set_xticks(range(4),['2011','2012','2021','2026']);ax.set_xlim(-.5,3.5)
        ax.set_title(player+' — first 10 game minutes');ax.set_ylabel(label)
        ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15)
fig.suptitle('Different maps and match settings; descriptive samples, no aging effect identified',fontsize=12)
fig.savefig(OUT/'new_features.png',dpi=170);plt.close(fig)

cols=['player','year','context','n_games','n_clusters','core_cpm_nominal',
      'destination_jump_ge_quarter_diagonal_fraction','build_commands_nominal_min',
      'wall_commands_nominal_min','research_commands_nominal_min','explicit_actor_coverage']
table=summary[(summary.year>=2021)&(summary.window=='first 10 game minutes')][cols].copy()
table=table.round(4)
body="""# Mac setup and expanded replay analysis

CaptureAge was downloaded from the official vendor, extracted into a dedicated
CrossOver Windows 10 bottle, and tested on this Apple-silicon Mac. The existing
CrossOver license ZIP was found in Documents, installed using the existing
signed files, and verified by CrossOver opening its normal main window.
The license itself is not included in this report or its analysis bundle.

## What works, and what remains incomplete

- The dedicated bottle is `tools/bottles/AoE2Analysis64`. Its graphics backend
  is D3DMetal. The existing SteamAgainstStorm64 bottle was not modified.
- The 32-bit CaptureAge installer crashed in the first compatibility test.
  The official offline archive was extracted instead; its 64-bit CaptureAge
  executable starts under the licensed CrossOver runtime.
- Free Wine 11.0 failed to create the Direct3D device in this test.
- CrossOver with D3DMetal progressed through renderer creation and shader
  loading, then failed at image/asset loading with `80070003: Path not found`.
  Its configured AoE2DE directory does not contain the game.
- Full rendering and replay playback have not been validated. **Zero target
  games have been analyzed through CaptureAge or an engine state stream.**
- A native ARM64 LibreMatch initial-state-patch exporter was built. It decodes
  the upstream published fixture into a 120×120 map, 2 players, 2,278 entities,
  resource/population attributes, and a 2,106,524 ms world timestamp.
  The fixture is Rin_ versus LemmiWingx, not DauT or TheViper. This is a test of
  the 2024 reverse-engineered schema, not proof of current game compatibility
  or a complete `.caderec` converter.

The original `.aoe2record` files require AoE2DE to simulate playback before
game-state deltas can be collected. CaptureAge recordings can later play without
the game running, but CaptureAge still needs installed game assets. The old
2011/2012 classic recordings additionally need a compatible classic engine;
AoE2DE cannot be assumed to simulate those files.

## Completed native reanalysis

All 37 distinct target-player games were re-read from their raw bodies, producing
44 player-game observations and 88 whole-game/opening rows. Hashes, full-body
consumption, command times/types/ownership, replay clocks, and original core
command rates agree. The earlier report and bundle have been preserved.

The additional details include explicit commanded unit IDs, encoded group sizes,
command targets, command destination distances, building/research type diversity,
production-building command revisits, and construction/research/market rates.
The full feature table contains 30 measures and denominator/coverage fields.

**Interpretation boundaries:** destinations are command targets, not the camera,
attention, or observed threats. Queue commands are requests, not completed units.
Production-command revisits are not building idle time. Re-command intervals are
not reaction time. Explicit actor lists cover only about 29–40% of opening
move/order commands in the 2021/2026 samples; the rest often use compressed
selection reuse markers. No selection was imputed. Group-change and same-group
interval measures therefore cannot support longitudinal conclusions here.

## Opening comparison, 2021 versus 2026

The table uses medians over the first 10 game minutes in each recording.
Rates use game clock divided by nominal game speed, not measured real time.
2021 consists of tournament series; 2026 consists of small ranked-session
samples. Map, civilization, opponent, patch and setting differ.

"""
body+=table.to_markdown(index=False)+"\n\n"
body+="""DauT's large destination-jump fraction decreased from 7.75% to 5.12%, and
TheViper's from 9.35% to 4.45%. A jump means at least one-quarter of the map
diagonal between consecutive valid move/order destinations. This is a command
distribution difference; maps and opening strategies can explain it.

The earlier command-rate pattern is reproduced: DauT's opening median goes
from 95.82 to 84.84 nominal commands/minute, and TheViper's from 122.19 to 102.75.
Whole-game rates move upward, so the sample does not show a simple general
command-speed decline. Neither result identifies reaction time, working-memory
capacity, aging, or cognitive compensation.

## Reproduction and files

- `game_features.csv`: all 44 observations × 2 windows, including coverage.
- `period_summary.csv`: medians and sample/cluster counts across periods.
- `comparison_2021_2026.csv`: feature-wise descriptive changes.
- `detailed_actions.jsonl.gz`: target commands and retained payload details;
  no chats or unknown binary payloads.
- `validation.json`: checks for all 37 games.
- `../tools/native-decoder-validation.json`: native fixture scope/checks.
- `../tools/captureage-downloads.json`: official source URLs, sizes and hashes.
- `../tools/native-source-changes.patch`: modifications to the AGPL source.
- `../Launch CaptureAge.command`: uses the installed licensed CrossOver.
- `../Analyze replays.command`: reruns command features and this report locally.

Source code: `../scripts/reanalyze_v2.py`, `../scripts/report_v2.py`, and the
downloaded LibreMatch source under `../tools/delta-play-replay/`. Rebuild the
native exporter there with `cargo build -p uncage-model --example export_patch
--locked`, then supply a decoded initial patch and a new JSON output path.
This exporter does not accept `.aoe2record` files or arbitrary `.caderec` files.

## Primary references

- [CaptureAge download and game requirement](https://captureage.com/cade/get)
- [CaptureAge recordings and asset requirement](https://captureage.com/cade/docs/cade-latest/caderecs)
- [CaptureAge performance guidance](https://captureage.com/cade/docs/cade-latest/overview)
- [LibreMatch delta/state tools](https://github.com/librematch/delta-play-replay)
- [LibreMatch replay gRPC service](https://librematch.github.io/wiki/grpc/main.html)

Next dependency: install a legitimately owned AoE2DE copy in a compatible
Windows environment, verify one recent replay end to end, and compare a few
state measurements with CaptureAge before interpreting longitudinal trends.
Older DE recordings may require their original engine patch.
"""
if (OUT/'FOLLOWUP.md').exists():
    body+='\n'+(OUT/'FOLLOWUP.md').read_text()
(OUT/'REPORT.md').write_text(body)
image=base64.b64encode((OUT/'new_features.png').read_bytes()).decode()
page='''<!doctype html><meta charset="utf-8"><title>Mac replay analysis</title>
<style>body{font:16px/1.6 system-ui;max-width:1150px;margin:40px auto;padding:0 25px;color:#172a39}h1{line-height:1.2}img{max-width:100%}table{border-collapse:collapse;font-size:13px}td,th{padding:6px;border-bottom:1px solid #ddd;text-align:right}pre{white-space:pre-wrap;background:#f5f7f9;padding:20px}input{padding:8px;width:80%}.scroll{overflow-x:auto}</style>
<h1>Mac setup and expanded replay analysis</h1>
<p><b>CrossOver license installed; CaptureAge needs AoE2DE assets before replay playback can be tested.</b></p>
<p>Completed: native command reanalysis of 37 games / 44 player-game observations. No CaptureAge state measurements from the target games.</p>
'''
page+=f'<img src="data:image/png;base64,{image}" alt="Per-game opening command rates and destination jumps across periods">'
page+='<h2>2021 versus 2026 opening medians</h2><div class="scroll">'+table.to_html(index=False)+'</div>'
page+='<h2>Search the per-game features</h2><input id="search" placeholder="Player, year, context or game ID"><div class="scroll">'+df.round(4).to_html(index=False,table_id='games')+'</div>'
page+='<h2>Methods, status and limits</h2><pre>'+html.escape(body)+'</pre>'
page+='''<script>document.querySelector('#search').addEventListener('input',function(){const q=this.value.toLowerCase();document.querySelectorAll('#games tbody tr').forEach(r=>r.style.display=r.textContent.toLowerCase().includes(q)?'':'none')})</script>'''
(OUT/'report.html').write_text(page)
print('Report written:',OUT/'report.html')
