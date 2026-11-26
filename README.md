# reel-srt

Turn a plain reel script into timed **SRT captions** for Instagram Reels, YouTube Shorts and other short videos. Works with **English, Hindi (Devanagari) and Hinglish**. Pure Python, no dependencies.

## Usage

```bash
python3 reel_srt.py script.txt -o captions.srt               # 2.5 words/sec
python3 reel_srt.py script.txt --duration 30 -o captions.srt # fit into a 30s reel
python3 reel_srt.py script.txt --max-words 3                 # shorter captions
```

Captions are split into short chunks (4 words by default) and never cross a sentence end (`.`, `!`, `?` or the Hindi danda `।`).

Import the `.srt` into CapCut, Premiere, DaVinci Resolve, or burn it in with ffmpeg:

```bash
ffmpeg -i reel.mp4 -vf subtitles=captions.srt out.mp4
```

## Tests

```bash
python3 -m unittest
```

## License

MIT
