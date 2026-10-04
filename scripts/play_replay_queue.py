"""Sequential replay capture through the game's local API; no desktop input."""
import hashlib
import gzip
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import time

import grpc
import collect_engine as c

ROOT = c.ROOT
OUT = ROOT / 'engine-pass'
PYTHON = sys.executable


def varint(n):
    b = bytearray()
    while n > 127:
        b.append((n & 127) | 128)
        n >>= 7
    b.append(n)
    return bytes(b)


def save(path, data):
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, indent=2) + '\n')
    tmp.replace(path)


def main():
    certs = ROOT / 'tools/delta-play-replay/crates/uncage-client/cert'
    channel = grpc.secure_channel('127.0.0.1:4341', grpc.ssl_channel_credentials(
        (certs / 'certificate-authority.pem').read_bytes(),
        (certs / 'cade-client.key').read_bytes(),
        (certs / 'cade-client.pem').read_bytes()), options=[
        ('grpc.ssl_target_name_override', 'ca-game-api')])
    def rpc(name, data):
        return channel.unary_unary('/cade_api.rpc.CadeRemote/' + name)(data, timeout=20)
    queue = json.loads((OUT / 'queue.json').read_text())
    # Current-patch recordings first; historical engine compatibility is separate.
    plan_path = OUT / 'capture-plan.json'
    plan = json.loads(plan_path.read_text()) if plan_path.exists() else None
    selected = [q for q in queue if q['year'] == 2026 and (plan is None or q['game_id'] in plan['game_ids'])]
    if plan:
        selected.sort(key=lambda q: plan['game_ids'].index(q['game_id']))
    state = {'state': 'running', 'pid': os.getpid(), 'games_planned': len(selected),
             'games_captured': 0, 'current_game': None, 'results': [],
             'historical_games_pending': sum(q['year'] != 2026 for q in queue),
             'recent_games_deferred': sum(q['year'] == 2026 for q in queue) - len(selected), 'batch_running': True}
    manifest = json.loads((ROOT / 'results/manifest.json').read_text())
    identities = {x['game_id']: x['player_names'] for x in manifest if x['status'] == 'parsed'}
    process = None
    try:
        for game in selected:
            if (OUT / 'STOP').exists():
                state['state'] = 'stopped_by_request'
                break
            source = ROOT / game['file']
            if hashlib.sha256(source.read_bytes()).hexdigest() != game['sha256']:
                raise RuntimeError('Replay source hash changed')
            verified = []
            for previous in sorted(OUT.glob('full-' + game['game_id'] + '*')):
                p = previous / 'status.json'
                if p.exists() and json.loads(p.read_text()).get('complete_match_verified'):
                    verified.append(previous)
            if verified:
                previous = verified[-1]
                stats = json.loads((previous / 'status.json').read_text())
                state['results'].append({'game_id': game['game_id'], 'folder': previous.name,
                    'frames': stats['frames'], 'commands': stats['commands'],
                    'last_time_ms': stats['last_time_ms']})
                state['games_captured'] += 1
                continue
            folder = OUT / ('full-' + game['game_id'])
            attempt = 1
            while folder.exists():
                attempt += 1
                folder = OUT / ('full-' + game['game_id'] + '-attempt-' + str(attempt))
            state['current_game'] = game
            state['phase'] = 'loading'
            save(OUT / 'status.json', state)
            rpc('Pause', c.pb.PauseRequest(paused=True).SerializeToString())
            path = ('Z:' + str(source).replace('/', '\\')).encode()
            nested = b'\x0a' + varint(len(path)) + path
            # API22 LoadGameRequest.LoadReplay: union field 2; filePath field 1.
            rpc('LoadGame', b'\x12' + varint(len(nested)) + nested)
            folder.mkdir()
            save(folder / 'source.json', game)
            log = open(folder / 'collector.log', 'xb')
            process = subprocess.Popen([PYTHON, str(ROOT / 'scripts/collect_engine.py'),
                '--output', str(folder), '--seconds', '7200'], stdout=log, stderr=log)
            log.close()
            start = time.monotonic()
            stats = {}
            startup_unpaused = False
            while time.monotonic() - start < 45:
                p = folder / 'status.json'
                if p.exists():
                    stats = json.loads(p.read_text())
                    if stats.get('frames', 0):
                        break
                if time.monotonic() - start > 5:
                    # Stream is connected before release; first-frame validation still required.
                    rpc('Pause', c.pb.PauseRequest(paused=False).SerializeToString())
                    startup_unpaused = True
                if process.poll() is not None:
                    raise RuntimeError('Collector exited during load')
                time.sleep(1)
            decoded = json.load(gzip.open(ROOT / 'results/decoded' / (game['sha256'] + '.json.gz'), 'rt'))
            first_command_ms = min(x['t'] for x in decoded['actions']) * 1000
            first_time = stats.get('first_time_ms')
            if not stats.get('frames') or first_time is None or first_time > min(250, first_command_ms):
                raise RuntimeError('Replay capture began after the first recorded command; stopping')
            initial = (folder / 'initial-patch.bin').read_bytes()
            names = identities[game['game_id']]
            if not all(name.encode() in initial for name in names):
                raise RuntimeError('Initial-state player names do not match the source replay')
            save(folder / 'start-validation.json', {'first_state_time_ms': first_time,
                'first_recorded_command_time_ms': first_command_ms,
                'source_hash_verified': True, 'player_names_verified': names,
                'capture_began_before_first_recorded_command': True})
            # Published API uses enum EXTRA_FAST=3, not a float multiplier.
            rpc('SetGameSpeed', b'\x08\x03')
            rpc('Pause', c.pb.PauseRequest(paused=False).SerializeToString())
            state['phase'] = 'capturing'
            expected_ms = game['duration_game_min'] * 60_000
            last_time = 0
            changed_at = time.monotonic()
            complete = False
            while process.poll() is None:
                time.sleep(3)
                stats = json.loads((folder / 'status.json').read_text())
                t = stats.get('last_time_ms') or 0
                if t != last_time:
                    changed_at = time.monotonic()
                    last_time = t
                state['capture'] = stats
                state['progress_fraction'] = min(1, t / expected_ms)
                save(OUT / 'status.json', state)
                if (OUT / 'STOP').exists():
                    state['state'] = 'stopped_by_request'
                    break
                # End verification requires an actual resign event and expected duration.
                if t >= expected_ms - 3000 and stats.get('resign_commands', 0) > 0:
                    complete = True
                    break
                if time.monotonic() - changed_at > 60:
                    raise RuntimeError('Replay clock stalled before verified completion')
            rpc('Pause', c.pb.PauseRequest(paused=True).SerializeToString())
            process.terminate()
            process.wait(timeout=20)
            process = None
            stats = json.loads((folder / 'status.json').read_text())
            stats['complete_match_verified'] = complete
            stats['expected_duration_ms'] = expected_ms
            save(folder / 'status.json', stats)
            if not complete:
                raise RuntimeError('Replay ended without verified full-match capture')
            subprocess.run([PYTHON, str(ROOT / 'scripts/summarize_engine_capture.py'),
                            str(folder)], check=True, stdout=subprocess.DEVNULL)
            state['results'].append({'game_id': game['game_id'], 'folder': folder.name,
                                     'frames': stats['frames'], 'commands': stats['commands'],
                                     'last_time_ms': stats['last_time_ms']})
            state['games_captured'] += 1
            state['capture'] = stats
            state['phase'] = 'finished'
            save(OUT / 'status.json', state)
        else:
            state['state'] = 'recent_queue_complete'
    except Exception as exc:
        state['state'] = 'needs_attention'
        state['error'] = str(exc)
        try:
            rpc('Pause', c.pb.PauseRequest(paused=True).SerializeToString())
        except Exception:
            pass
    finally:
        if process is not None and process.poll() is None:
            process.terminate()
            process.wait(timeout=20)
        state['batch_running'] = False
        save(OUT / 'status.json', state)
        channel.close()
    print(json.dumps(state), flush=True)


if __name__ == '__main__':
    main()
