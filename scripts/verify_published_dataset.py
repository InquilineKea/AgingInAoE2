"""Verify published table coverage, capture counts and restored source hashes."""
import csv, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def rows(name):
    with (ROOT / 'deadline-sparse' / name).open() as stream:
        return list(csv.DictReader(stream))

def main():
    features = rows('behavior_features_all.csv')
    observations = {(r['game_id'], r['player']) for r in features}
    comparisons = rows('all_trait_comparisons.csv')
    assert len(observations) == 98 and len(features) == 195
    assert len(comparisons) == 1148 and len({r['trait'] for r in comparisons}) == 82
    assert len(rows('catalog_comparison_status.csv')) == 255
    complete = [c for c in json.loads((ROOT / 'engine-pass/capture-inventory.json').read_text()) if c['status'].get('complete_match_verified')]
    assert len(complete) == 4
    assert sum(c['status']['frames'] for c in complete) == 362011
    assert sum(c['status']['commands'] for c in complete) == 12368
    assert all(c['status']['time_steps_skipped'] == 0 for c in complete)
    provenance = json.loads((ROOT / 'deadline-sparse/all_source_replays.json').read_text())
    sources = {r['sha256']: r for r in provenance}
    assert len(sources) == 91
    missing = []
    for digest, entry in sources.items():
        source = ROOT / entry['file']
        if not source.exists(): missing.append(entry['file']); continue
        assert hashlib.sha256(source.read_bytes()).hexdigest() == digest, entry['file']
    report = {'verified_player_game_observations': len(observations), 'window_rows': len(features), 'comparison_rows': len(comparisons), 'trait_definitions': 82, 'candidate_metrics_controls': 255, 'complete_engine_matches': 4, 'complete_engine_frames': 362011, 'complete_engine_commands': 12368, 'unique_source_replay_files': len(sources), 'restored_source_files_missing': len(missing), 'all_restored_source_hashes_verified': not missing}
    print(json.dumps(report, indent=2))
    if missing: raise SystemExit('Restore release inputs to verify source replay hashes.')

if __name__ == '__main__': main()
