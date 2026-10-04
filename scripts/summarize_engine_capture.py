"""Export decoded commands from a closed capture; preserve scope limitations."""
import collections
import gzip
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'engine-pass/proto'))
import cade_api_pb2 as pb
from google.protobuf.json_format import MessageToDict


def main(folder):
    folder = Path(folder)
    command_counts = collections.Counter()
    events = collections.Counter()
    players = collections.Counter()
    unit_commands = explicit = human = 0
    first = last = None
    frames = skipped = 0
    with gzip.open(folder / 'frames.pb.gz', 'rb') as source, gzip.open(
            folder / 'commands.jsonl.gz', 'wt') as dest:
        while True:
            prefix = source.read(4)
            if not prefix:
                break
            if len(prefix) != 4:
                raise ValueError('Truncated frame length')
            size = struct.unpack('<I', prefix)[0]
            if size > 128 * 1024 * 1024:
                raise ValueError('Frame size exceeds collector limit')
            data = source.read(size)
            if len(data) != size:
                raise ValueError('Truncated protobuf frame')
            seq = pb.FrameSequence.FromString(data)
            for frame in seq.frame:
                frames += 1
                skipped += frame.timeStepsSkipped
                if first is None:
                    first = frame.time
                if last is not None and frame.time < last:
                    raise ValueError('Replay clock moved backwards in capture')
                last = frame.time
                for event in frame.event:
                    events[event.WhichOneof('event') or 'unparsed_new_event'] += 1
                for command in frame.command:
                    typ = command.WhichOneof('command')
                    command_counts[typ or 'unparsed_new_command'] += 1
                    if typ:
                        obj = getattr(command, typ)
                        fields = obj.DESCRIPTOR.fields_by_name
                        if 'unitIds' in fields:
                            unit_commands += 1
                            explicit += bool(obj.unitIds)
                        if 'humanOrder' in fields:
                            human += obj.humanOrder
                        if 'commPlayerId' in fields:
                            players[obj.commPlayerId] += 1
                        dest.write(json.dumps({'game_time_ms': frame.time,
                            'type': typ, 'payload': MessageToDict(obj)}) + '\n')
    result = {'frames': frames, 'first_game_time_ms': first, 'last_game_time_ms': last,
              'time_steps_skipped': skipped, 'command_types': dict(command_counts),
              'event_types': dict(events), 'comm_player_command_counts': dict(players),
              'commands_with_unit_list_field': unit_commands,
              'commands_with_explicit_unit_ids': explicit, 'human_order_true_count': human,
              'onager_dodges_classified': 0, 'state_schema_decoded': False,
              'limitations': ['Current binary state schema is not yet decoded.',
                  'New event types are retained as protobuf data but not classified.',
                  'Commands alone do not identify onager dodges or reaction time.']}
    (folder / 'command-summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main(sys.argv[1])
