from __future__ import annotations

import json
import os
from pathlib import Path

import requests


def ensure_output_dirs(base_dir: str) -> dict[str, Path]:
    base = Path(base_dir)
    paths = {
        "base": base,
        "transcripts": base / "transcripts",
        "recordings": base / "recordings",
        "metadata": base / "metadata",
        "logs": base / "logs",
        "bug_analysis": base / "bug_analysis",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def save_text(path: Path, content: str) -> None:
    path.write_text(content or "", encoding="utf-8")


def save_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def download_file(url: str, target_path: Path) -> Path:
    with requests.get(url, stream=True, timeout=120) as resp:
        resp.raise_for_status()
        with target_path.open("wb") as f:
            for chunk in resp.iter_content(chunk_size=1024 * 64):
                if chunk:
                    f.write(chunk)
    return target_path


def save_call_artifacts(
    *,
    output_dir: str,
    call_id: str,
    call_data: dict,
    scenario: dict,
) -> dict[str, str | None]:
    dirs = ensure_output_dirs(output_dir)

    transcript_path = dirs["transcripts"] / f"{call_id}.txt"
    metadata_path = dirs["metadata"] / f"{call_id}.json"
    public_log_path = dirs["logs"] / f"{call_id}_public_log.txt"

    transcript = call_data.get("transcript") or ""
    save_text(transcript_path, transcript)

    combined_metadata = {
        "call_id": call_id,
        "scenario": scenario,
        "call_data": call_data,
    }
    save_json(metadata_path, combined_metadata)

    public_log_url = call_data.get("public_log_url")
    if public_log_url:
        try:
            download_file(public_log_url, public_log_path)
        except Exception:
            public_log_path = None  # type: ignore[assignment]
    else:
        public_log_path = None  # type: ignore[assignment]

    recording_url = (
        call_data.get("recording_url")
        or call_data.get("scrubbed_recording_url")
        or call_data.get("recording_multi_channel_url")
        or call_data.get("scrubbed_recording_multi_channel_url")
    )

    saved_recording_path: Path | None = None
    saved_mp3_path: str | None = None

    if recording_url:
        ext = os.path.splitext(recording_url.split("?")[0])[1] or ".wav"
        raw_recording_path = dirs["recordings"] / f"{call_id}{ext}"
        try:
            saved_recording_path = download_file(recording_url, raw_recording_path)

            if saved_recording_path.suffix.lower() == ".wav":
                mp3_path = saved_recording_path.with_suffix(".mp3")
                saved_mp3_path = wav_to_mp3(
                    str(saved_recording_path),
                    str(mp3_path)
                )

        except Exception:
            saved_recording_path = None

    return {
        "transcript_path": str(transcript_path),
        "metadata_path": str(metadata_path),
        "public_log_path": str(public_log_path) if public_log_path else None,
        "recording_path": str(saved_recording_path) if saved_recording_path else None,
        "mp3_path": str(saved_mp3_path) if saved_mp3_path else None,
    }

import subprocess

def wav_to_mp3(wav_path: Path, mp3_path: Path) -> Path:
    """
    Convert wav → mp3 using ffmpeg (no python audio)
    """

    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(wav_path),
        "-codec:a", "libmp3lame",
        "-qscale:a", "2",
        str(mp3_path)
    ]

    subprocess.run(cmd, check=True)

    return mp3_path