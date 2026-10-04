"""Apply documented replay speed to the current running sparse queue."""
import json,time,grpc
import collect_engine as c
p=c.ROOT/'tools/delta-play-replay/crates/uncage-client/cert'
ch=grpc.secure_channel('127.0.0.1:4341',grpc.ssl_channel_credentials((p/'certificate-authority.pem').read_bytes(),(p/'cade-client.key').read_bytes(),(p/'cade-client.pem').read_bytes()),options=[('grpc.ssl_target_name_override','ca-game-api')])
seen=set();start=time.monotonic()
while time.monotonic()-start<10800:
 s=json.loads((c.ROOT/'engine-pass/status.json').read_text())
 if not s.get('batch_running'): break
 gid=(s.get('current_game') or {}).get('game_id')
 if s.get('phase')=='capturing' and gid and gid not in seen:
  reply=ch.unary_unary('/cade_api.rpc.CadeRemote/SetGameSpeed')(b'\x08\x03',timeout=10)
  print(json.dumps({'game_id':gid,'speed':'EXTRA_FAST','response_hex':reply.hex()}),flush=True);seen.add(gid)
 time.sleep(5)
ch.close()
