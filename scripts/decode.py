"""Local replay decoder. mgz 1.8.51 body parser; bounded DE lobby-prefix reader.

The prefix reader follows mgz/fast/header.py parse_de through active players,
without attempting unsupported 68.9 inactive-player/scenario/object sections.
No header-byte searching or inferred player ownership is used for DE.
"""
from pathlib import Path
import struct, datetime, collections
from mgz.fast.header import decompress, parse_version, de_string
from mgz.util import unpack, Version
from mgz import fast


def de_prefix(data, save):
    build=unpack('<I',data) if save>=25.22 else None
    timestamp=unpack('<I',data) if save>=26.16 else None
    data.read(12)
    dlc=[unpack('<I',data) for _ in range(unpack('<I',data))]
    data.read(4)
    dim_or_difficulty=unpack('<I',data)
    dimension=dim_or_difficulty if save>=61.5 else None
    data.read(4);map_id=unpack('<I',data);data.read(4)
    victory,resources,start_age,end_age=[unpack('<I',data) for _ in range(4)]
    data.read(12);speed=unpack('<f',data)
    treaty,population,num_players=[unpack('<I',data) for _ in range(3)]
    assert num_players in range(1,9) and 0.5<=speed<=3 and population<=1000
    data.read(14)
    if save>=61.5:data.read(1)
    data.read(3);data.read(10);data.read(12)
    if save>=25.06:data.read(1)
    if save>50:data.read(1)
    players=[]
    for _ in range(num_players):
        data.read(4);color=unpack('<i',data);data.read(2);team=unpack('<b',data);data.read(9)
        civ=unpack('<I',data)
        if save>=61.5:
            custom_count=unpack('<I',data)
            assert custom_count<100
            if save>=63 and custom_count:data.read(4*custom_count)
        de_string(data);data.read(1);de_string(data)
        if save>=66.3:de_string(data)
        name=de_string(data).decode('utf-8')
        typ=unpack('<I',data);profile,number=unpack('<I4xi',data)
        if save<25.22:data.read(8)
        data.read(2)
        if save>=25.06:data.read(8)
        if save>=64.3:data.read(4)
        if save>=68.9:
            # New trailing DE string observed in each active lobby record.
            # Require its marker/length; do not guess the next player offset.
            trailing=de_string(data)
            assert trailing==b''
        assert 1<=number<=8 and len(name)<100 and color in range(8)
        players.append(dict(number=number,name=name,profile_id=profile,civilization_id=civ,color_id=color,team_id=team))
    assert len(set(p['number'] for p in players))==num_players
    return dict(players=players,speed=speed,dimension=dimension,map_id=map_id,build=build,timestamp=timestamp,population=population,start_age=start_age)


def decode(path):
    path=Path(path)
    with path.open('rb') as handle:
        header=decompress(handle);version,game,save,log=parse_version(header,handle)
        body_start=handle.tell()
        if version is Version.DE:
            meta=de_prefix(header,save)
            if save<68:
                # Independent full header parser establishes map dimension and
                # agrees on every active-player identity/slot/profile/civ/speed.
                from mgz.fast.header import parse
                handle.seek(0)
                try:
                    full=parse(handle)
                    fp={p['number']:p for p in full['de']['players']}
                    for p in meta['players']:
                        for key in ['number','profile_id','civilization_id']:
                            assert p[key]==fp[p['number']][key],key
                        assert p['name']==fp[p['number']]['name'].decode('utf-8')
                    meta['dimension']=full['map']['dimension']
                    meta['restore_time']=full['map']['restore_time']
                    assert abs(meta['speed']-full['de']['speed'])<1e-5
                    meta['header_parser']='mgz fast full header'
                except RuntimeError:
                    # Supported 2021 files with fast-player-search failures:
                    # use the official construct parser, not guessed offsets.
                    import mgz
                    handle.seek(0);full=mgz.header.parse_stream(handle)
                    fp={p.player_number:p for p in full.de.players}
                    for p in meta['players']:
                        q=fp[p['number']]
                        assert p['name']==q.name.value.decode('utf-8')
                        assert p['profile_id']==q.profile_id
                        assert p['civilization_id']==q.civ_id
                    meta['dimension']=full.map_info.size_x
                    meta['restore_time']=full.initial.restore_time
                    assert abs(meta['speed']-full.replay.game_speed_float)<1e-5
                    meta['header_parser']='mgz construct full header fallback'
            meta['decoder']='mgz-body + validated DE active-player prefix'
        else:
            # Official construct header parser supports classic/userpatch files.
            import mgz
            handle.seek(0);full=mgz.header.parse_stream(handle)
            body_start=handle.tell()
            ps=[dict(number=i,name=p.attributes.player_name.decode('latin-1'),civilization_id=p.attributes.civilization,color_id=p.attributes.player_color) for i,p in enumerate(full.initial.players) if i>0]
            meta=dict(players=ps,speed=full.replay.game_speed_float,dimension=full.map_info.size_x,map_id=full.scenario.game_settings.map_id,timestamp=None,restore_time=full.initial.restore_time,decoder='mgz construct classic header + mgz body')
        handle.seek(body_start)
        fast.meta(handle);ts=0;actions=[];chats=[];counts=collections.Counter();sync_checks=0;resigned=[]
        while True:
            pos=handle.tell()
            if pos==path.stat().st_size:break
            try:op,payload=fast.operation(handle)
            except EOFError:
                raise RuntimeError(f'Truncated/undecodable operation at {pos}; size {path.stat().st_size}')
            counts[op.name]+=1
            if op is fast.Operation.SYNC:
                increment,checksum,stats=payload;assert 0<=increment<=600000
                ts+=increment
                if stats:
                    assert abs(stats['current_time']-ts)<=1000, f"Replay clock mismatch: body sync {stats['current_time']} ms vs accumulated {ts} ms; header restore {meta.get('restore_time', 'unavailable')} ms"
                    sync_checks+=1
            elif op is fast.Operation.ACTION:
                typ,p=payload
                # Keep only replay action metadata, not chat or platform account ids.
                action=dict(t=ts/1000,type=typ.name,player=p.get('player_id'),x=p.get('x'),y=p.get('y'),amount=p.get('amount'),unit_id=p.get('unit_id'),technology_id=p.get('technology_id'))
                actions.append(action)
                if typ is fast.Action.RESIGN:resigned.append(p.get('player_id'))
        assert ts>0 and len(actions)>20
        meta.update(duration_s=ts/1000,save_version=save,game_version=game,log_version=log,sync_checks=sync_checks,operations=dict(counts),body_start=body_start,body_end=handle.tell(),resigned=resigned)
        if meta['timestamp']:meta['date_utc']=datetime.datetime.fromtimestamp(meta['timestamp'],datetime.timezone.utc).isoformat()
        return meta,actions
