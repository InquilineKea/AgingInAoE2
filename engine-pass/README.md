# Replay processing — live local run

The game is now responding and replay playback is verified. The native Python collector uses the game’s local CadeRemote API (game build 185872, API22). CaptureAge itself is not required to remain open for this collection. These files are custom protobuf captures, not `.caderec` files.

`status.json` is the live queue state. The current run contains ten recent recordings: five DauT and five TheViper games, all recorded on build 185872. The controller loads them sequentially, verifies source hashes and both player names, checks that collection starts before the first recorded command, and stops if a check fails.

The first verified capture is `full-c7d3588daf74-attempt-2`: 108,792 frames, 2,506 commands, no reported skipped simulation steps, an exact final game timestamp of 1,416,480 ms, and the final resign command. The initial state is at 104 ms, before the first recorded command at 416 ms. The second match was subsequently loaded and identity-checked. Counts in this document are a startup snapshot; consult the live status for current progress.

An end-of-match progress-reporting bug initially made the first capture appear stalled. The final saved data proved the match complete; progress is now published periodically even when no new frame arrives. Failed attempts remain preserved and clearly marked as incomplete.

Each closed full capture is checked for readable protobuf framing and a monotonic clock, then exports `commands.jsonl.gz` and `command-summary.json`. Known PlayerChat events are removed. Newly added event types remain unclassified; the 2024 binary state decoder is not compatible with the current state schema. No onager dodges, reaction times, working-memory capacities or compensation effects have been classified.

The queue uses local API calls and does not operate the desktop mouse or keyboard. Leave AoE2DE open; the game may be minimized while you use other applications. Background resource use and playback speed depend on the machine.

Twenty-seven historical recordings remain outside this current-build run: fourteen older DE recordings need engine compatibility checks, and thirteen classic recordings need a compatible classic engine.

To stop the queue, run `../Stop replay processing.command`, or create an `engine-pass/STOP` file. The controller checks this marker and stops collection; it does not delete recordings.
