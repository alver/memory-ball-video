# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Memory Ball Video Maker — a Python script that creates 480x480 MP4 slideshow videos with transitions for the Memory Ball device (UM-ER-02). Uses FFmpeg for all video/audio processing via subprocess calls. No third-party Python packages required (stdlib only).

## Running

```bash
python create_video.py --photos ./photos [--output output.mp4] [--duration 5] [--transition 1] \
    [--music ./music] [--first photo1.jpg photo2.jpg] [--mode crop|pad|blur|stretch]
```

All parameters use `--key value` format (order doesn't matter). Only `--photos` is required. Run `python create_video.py --help` for full usage info.

**Requirements:** Python 3.12+, FFmpeg and ffprobe in PATH.

## Architecture

Single-file project (`create_video.py`, ~360 lines) with a 3-stage pipeline:

1. **Photo → Clip**: Each image becomes a 480x480 H.264 video clip (30fps, ultrafast preset, CRF 23)
2. **Merge with transitions**: Clips are merged pairwise in rounds (binary reduction) using random `xfade` transitions — not sequential concatenation
3. **Add audio**: Music files are looped via FFmpeg concat demuxer to match video duration, then muxed in

Key functions:
- `get_scale_filter(mode)` — returns FFmpeg `-vf` filter string for the 4 scaling modes (crop/pad/blur/stretch)
- `create_video_from_images(...)` — main pipeline orchestrator, uses a temp directory cleaned up in `finally`
- `get_video_duration(path)` — wraps ffprobe for duration queries

## Important Details

- Filter chain order matters: scale filter must come before `fps=30,format=yuv420p,setsar=1` (see line 145 comment)
- The pairwise merge strategy means transition order depends on merge rounds, not just photo sequence order
- All intermediate files go into a `tempfile.mkdtemp()` directory, cleaned up even on failure
- CLI uses `argparse`; all parameters are named (`--key value`), no positional args
