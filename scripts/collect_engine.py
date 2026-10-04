"""Local replay-only collector for the published LibreMatch CadeRemote protocol.

Uses existing anaconda Python/grpc. TLS verifies the vendor protocol certificate;
the client certificate is the public protocol fixture, not a user credential.
No GUI input, account login, or external network endpoints are used.
"""
import argparse
import gzip
import json
from pathlib import Path
import struct
import sys
import time
import signal
import threading

import grpc

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'engine-pass/proto'))
import cade_api_pb2 as pb


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--info', action='store_true')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--seconds', type=int, default=120)
    parser.add_argument('--host', choices=['127.0.0.1', '[::1]'], default='127.0.0.1')
    args = parser.parse_args()
    certs = ROOT / 'tools/delta-play-replay/crates/uncage-client/cert'
    creds = grpc.ssl_channel_credentials(
        (certs / 'certificate-authority.pem').read_bytes(),
        (certs / 'cade-client.key').read_bytes(),
        (certs / 'cade-client.pem').read_bytes(),
    )
    channel = grpc.secure_channel(args.host + ':4341', creds, options=[
        ('grpc.ssl_target_name_override', 'ca-game-api'),
        ('grpc.max_receive_message_length', 128 * 1024 * 1024),
    ])
    info_call = channel.unary_unary('/cade_api.rpc.CadeRemote/Info',
        request_serializer=pb.InfoRequest.SerializeToString,
        response_deserializer=pb.InfoResponse.FromString)
    try:
        info = info_call(pb.InfoRequest(), timeout=10)
    except grpc.RpcError as exc:
        failure = {'state': 'connection_failed', 'frames': 0,
                   'grpc_code': exc.code().name, 'error': exc.details(),
                   'complete_match_verified': False}
        print(json.dumps(failure), flush=True)
        if args.output:
            args.output.mkdir(parents=True, exist_ok=True)
            (args.output / 'status.json').write_text(json.dumps(failure, indent=2) + '\n')
        channel.close()
        sys.exit(1)
    metadata = {'game_version': info.gameVersion, 'api_version': info.apiVersion,
                'sequences': 0, 'frames': 0, 'commands': 0, 'events': 0,
                'chat_events_removed': 0, 'first_time_ms': None, 'last_time_ms': None,
                'state': 'connected', 'complete_match_verified': False}
    metadata.update(time_steps_skipped=0, maximum_frames_queued=0, resign_commands=0)
    print(json.dumps(metadata), flush=True)
    if args.info:
        return
    if args.output is None:
        parser.error('--output is required when collecting')
    args.output.mkdir(parents=True, exist_ok=True)
    status_path = args.output / 'status.json'
    def status():
        tmp = status_path.with_suffix('.tmp')
        tmp.write_text(json.dumps(dict(metadata), indent=2) + '\n')
        tmp.replace(status_path)
    status()
    stream_call = channel.unary_stream('/cade_api.rpc.CadeRemote/Frames',
        request_serializer=pb.FramesRequest.SerializeToString,
        response_deserializer=pb.FrameSequence.FromString)
    start = time.monotonic()
    metadata['state'] = 'collecting'
    # Preserve default temporal resolution until it is measured and validated.
    request = pb.FramesRequest(disableCommands=False, disableParticles=False,
                               disableParticleCulling=True)
    stream = stream_call(request, timeout=args.seconds)
    signal.signal(signal.SIGTERM, lambda *_: stream.cancel())
    stop_status = threading.Event()
    def publish_status():
        while not stop_status.wait(1):
            status()
    status_thread = threading.Thread(target=publish_status, daemon=True)
    status_thread.start()
    try:
        with gzip.open(args.output / 'frames.pb.gz', 'xb') as out:
            for seq in stream:
                for frame in seq.frame:
                    kept = [e for e in frame.event if e.WhichOneof('event') != 'playerChat']
                    metadata['chat_events_removed'] += len(frame.event) - len(kept)
                    del frame.event[:]
                    frame.event.extend(kept)
                    if metadata['first_time_ms'] is None:
                        metadata['first_time_ms'] = frame.time
                        (args.output / 'initial-patch.bin').write_bytes(frame.patch)
                    metadata['last_time_ms'] = frame.time
                    metadata['commands'] += len(frame.command)
                    metadata['events'] += len(frame.event)
                    metadata['time_steps_skipped'] += frame.timeStepsSkipped
                    metadata['resign_commands'] += sum(c.WhichOneof('command') == 'resign' for c in frame.command)
                data = seq.SerializeToString()
                out.write(struct.pack('<I', len(data)))
                out.write(data)
                metadata['sequences'] += 1
                metadata['frames'] += len(seq.frame)
                metadata['elapsed_seconds'] = round(time.monotonic() - start, 2)
                metadata['maximum_frames_queued'] = max(metadata['maximum_frames_queued'], seq.numberOfFramesQueued)
        metadata['state'] = 'stream_ended_unverified'
    except grpc.RpcError as exc:
        metadata['state'] = 'stopped'
        metadata['grpc_code'] = exc.code().name
        metadata['error'] = exc.details()
    finally:
        stop_status.set()
        status_thread.join(timeout=2)
        status()
        channel.close()
    print(json.dumps(metadata), flush=True)


if __name__ == '__main__':
    main()
