"""Summarize only verified closed captures; stop when the local queue stops."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'engine-pass'
os.nice(10)
completed = []
while True:
    for folder in sorted(OUT.glob('full-*')):
        status = folder / 'status.json'
        if not status.exists():
            continue
        data = json.loads(status.read_text())
        if data.get('complete_match_verified') and folder.name not in completed:
            if not (folder / 'command-summary.json').exists():
                with open(folder / 'summary.log', 'xb') as log:
                    subprocess.run([sys.executable, str(ROOT / 'scripts/summarize_engine_capture.py'),
                                    str(folder)], check=True, stdout=log, stderr=log)
            completed.append(folder.name)
    queue = json.loads((OUT / 'status.json').read_text())
    result = {'state': 'running' if queue.get('batch_running') else 'stopped',
              'verified_captures_summarized': completed,
              'onager_dodges_classified': 0, 'state_schema_decoded': False}
    tmp = OUT / 'analysis-progress.tmp'
    tmp.write_text(json.dumps(result, indent=2) + '\n')
    tmp.replace(OUT / 'analysis-progress.json')
    if not queue.get('batch_running'):
        break
    time.sleep(5)
