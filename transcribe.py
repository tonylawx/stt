#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import av
from faster_whisper import WhisperModel
from tqdm import tqdm


SUPPORTED_VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".mkv",
    ".avi",
    ".m4v",
    ".webm",
}

MODEL_ALIASES = {
    "turbo": "large-v3-turbo",
}


def is_apple_silicon() -> bool:
    return sys.platform == "darwin" and platform.machine() == "arm64"


def recommended_cpu_threads() -> int:
    cpu_count = os.cpu_count() or 4
    if is_apple_silicon():
        return max(4, cpu_count - 2)
    return max(2, cpu_count - 1)


def resolve_runtime_defaults(args: argparse.Namespace) -> argparse.Namespace:
    if args.device == "auto":
        args.device = "cpu" if is_apple_silicon() else "auto"

    if args.compute_type == "auto":
        args.compute_type = "int8" if is_apple_silicon() else "auto"

    if args.cpu_threads is None:
        args.cpu_threads = recommended_cpu_threads()

    args.model = MODEL_ALIASES.get(args.model, args.model)

    return args


@dataclass
class SubtitleSegment:
    index: int
    start: float
    end: float
    text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe a local video/audio file into subtitles."
    )
    parser.add_argument("input", type=Path, help="Path to an input mp4/video/audio file")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for output files. Defaults to the input file directory.",
    )
    parser.add_argument(
        "--model",
        default="turbo",
        help="Whisper model size, e.g. tiny/base/small/medium/large-v3 or turbo. Default: turbo.",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="Optional language code like zh, en, ja. Default: auto detect.",
    )
    parser.add_argument(
        "--device",
        default="auto",
        choices=["auto", "cpu", "cuda"],
        help="Inference device. Default: auto.",
    )
    parser.add_argument(
        "--compute-type",
        default="auto",
        help="Model compute type, e.g. auto/int8/float16/float32.",
    )
    parser.add_argument(
        "--beam-size",
        type=int,
        default=5,
        help="Beam size for decoding. Higher is slower but can improve accuracy.",
    )
    parser.add_argument(
        "--cpu-threads",
        type=int,
        default=None,
        help="Number of CPU threads for inference. Default: auto-tuned for your machine.",
    )
    parser.add_argument(
        "--task",
        default="transcribe",
        choices=["transcribe", "translate"],
        help="Use transcribe for same-language subtitles, translate for English output.",
    )
    return parser.parse_args()


def validate_input_file(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Input file not found: {resolved}")
    if not resolved.is_file():
        raise ValueError(f"Input path is not a file: {resolved}")
    if resolved.suffix.lower() not in SUPPORTED_VIDEO_EXTENSIONS and resolved.suffix.lower() not in {
        ".mp3",
        ".wav",
        ".m4a",
        ".flac",
        ".aac",
        ".ogg",
    }:
        raise ValueError(
            "Unsupported file type. Use a common video/audio file like mp4, mov, mkv, mp3, wav."
        )
    return resolved


def format_timestamp(seconds: float) -> str:
    total_milliseconds = max(0, round(seconds * 1000))
    hours, remainder = divmod(total_milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, milliseconds = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


def write_srt(path: Path, segments: Iterable[SubtitleSegment]) -> None:
    with path.open("w", encoding="utf-8") as file:
        for segment in segments:
            file.write(f"{segment.index}\n")
            file.write(
                f"{format_timestamp(segment.start)} --> {format_timestamp(segment.end)}\n"
            )
            file.write(f"{segment.text}\n\n")


def write_txt(path: Path, segments: Iterable[SubtitleSegment]) -> None:
    with path.open("w", encoding="utf-8") as file:
        for segment in segments:
            file.write(f"[{format_timestamp(segment.start)}] {segment.text}\n")


def normalize_segment_text(text: str) -> str:
    return " ".join(text.strip().split())


def get_media_duration_seconds(path: Path) -> float | None:
    container = av.open(str(path))
    try:
        if container.duration is None:
            return None
        return float(container.duration / av.time_base)
    finally:
        container.close()


def transcribe(
    args: argparse.Namespace, duration_seconds: float | None
) -> tuple[list[SubtitleSegment], str | None]:
    model = WhisperModel(
        args.model,
        device=args.device,
        compute_type=args.compute_type,
        cpu_threads=args.cpu_threads,
    )
    raw_segments, info = model.transcribe(
        str(args.input),
        language=args.language,
        beam_size=args.beam_size,
        task=args.task,
        vad_filter=True,
    )

    segments: list[SubtitleSegment] = []
    with tqdm(
        total=duration_seconds,
        unit="s",
        desc="Transcribing",
        dynamic_ncols=True,
        disable=duration_seconds is None,
    ) as progress_bar:
        last_progress = 0.0
        segment_index = 0

        for segment in raw_segments:
            if duration_seconds is not None:
                current_progress = min(segment.end, duration_seconds)
                progress_bar.update(max(0.0, current_progress - last_progress))
                last_progress = current_progress

            text = normalize_segment_text(segment.text)
            if not text:
                continue

            segment_index += 1
            segments.append(
                SubtitleSegment(
                    index=segment_index,
                    start=segment.start,
                    end=segment.end,
                    text=text,
                )
            )

        if duration_seconds is not None and last_progress < duration_seconds:
            progress_bar.update(duration_seconds - last_progress)

    return segments, info.language


def build_output_paths(input_path: Path, output_dir: Path | None) -> tuple[Path, Path]:
    destination = output_dir.expanduser().resolve() if output_dir else input_path.parent
    destination.mkdir(parents=True, exist_ok=True)
    base_name = input_path.stem
    return destination / f"{base_name}.srt", destination / f"{base_name}.txt"


def main() -> int:
    args = resolve_runtime_defaults(parse_args())

    try:
        input_path = validate_input_file(args.input)
        args.input = input_path
        srt_path, txt_path = build_output_paths(input_path, args.output_dir)

        print(f"Input file: {input_path}")
        print(f"Model: {args.model}")
        print(f"Device: {args.device}")
        print(f"Compute type: {args.compute_type}")
        print(f"CPU threads: {args.cpu_threads}")
        print("Loading model and transcribing. The first run may take time to download the model...")

        duration_seconds = get_media_duration_seconds(input_path)
        if duration_seconds is not None:
            print(f"Duration: {duration_seconds:.1f}s")

        segments, detected_language = transcribe(args, duration_seconds)
        if not segments:
            raise RuntimeError("No speech segments were detected in the input file.")

        write_srt(srt_path, segments)
        write_txt(txt_path, segments)

        if detected_language:
            print(f"Detected language: {detected_language}")
        print(f"SRT saved to: {srt_path}")
        print(f"TXT saved to: {txt_path}")
        return 0
    except KeyboardInterrupt:
        print("\nCancelled by user.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
