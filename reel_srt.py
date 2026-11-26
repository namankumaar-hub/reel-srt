#!/usr/bin/env python3
"""reel-srt: turn a plain reel script into timed SRT captions.

Works with English, Hindi (Devanagari) and Hinglish text. No dependencies.

Usage:
    python3 reel_srt.py script.txt -o captions.srt
    python3 reel_srt.py script.txt --duration 30 --max-words 4
"""
import argparse
import re
import sys

SENTENCE_END = re.compile(r"(?<=[.!?।])\s+")  # । = Hindi danda


def fmt_time(seconds):
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def chunk_script(text, max_words=4):
    """Split text into short caption chunks, never crossing a sentence end."""
    chunks = []
    for sentence in SENTENCE_END.split(text.strip()):
        words = sentence.split()
        for i in range(0, len(words), max_words):
            chunks.append(" ".join(words[i:i + max_words]))
    return [c for c in chunks if c]


def build_srt(text, duration=None, wps=2.5, max_words=4):
    """Return SRT text. Timing is proportional to word count.

    duration: total seconds to fit captions into (e.g. 30 for a 30s reel).
    wps: words per second, used when duration is not given.
    """
    chunks = chunk_script(text, max_words)
    if not chunks:
        return ""
    counts = [len(c.split()) for c in chunks]
    total_words = sum(counts)
    per_word = (duration / total_words) if duration else (1.0 / wps)
    out, t = [], 0.0
    for i, (chunk, n) in enumerate(zip(chunks, counts), 1):
        start, t = t, t + n * per_word
        out.append(f"{i}\n{fmt_time(start)} --> {fmt_time(t)}\n{chunk}\n")
    return "\n".join(out)


def main(argv=None):
    p = argparse.ArgumentParser(description="Turn a reel script into SRT captions.")
    p.add_argument("script", help="text file with the script ('-' for stdin)")
    p.add_argument("-o", "--output", help="output .srt file (default: stdout)")
    p.add_argument("--duration", type=float, help="fit captions into N seconds")
    p.add_argument("--wps", type=float, default=2.5, help="words per second (default 2.5)")
    p.add_argument("--max-words", type=int, default=4, help="max words per caption (default 4)")
    a = p.parse_args(argv)
    text = sys.stdin.read() if a.script == "-" else open(a.script, encoding="utf-8").read()
    srt = build_srt(text, a.duration, a.wps, a.max_words)
    if a.output:
        with open(a.output, "w", encoding="utf-8") as f:
            f.write(srt)
    else:
        sys.stdout.write(srt)


if __name__ == "__main__":
    main()
