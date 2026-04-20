# transcriber.py
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def transcribe_with_timestamps(audio_path: str) -> dict:
    """
    Uses OpenAI Whisper API (whisper-1).
    Returns:
    {
        "full_text": "...",
        "segments": [{"start": 0.0, "end": 2.1, "text": "..."}, ...],
        "second_by_second": [{"second": 0, "text": "..."}, ...]
    }
    """
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )

    segments = result.segments or []

    # Build second-by-second transcript
    second_map = {}
    for seg in segments:
        start = int(seg.start)
        end   = int(seg.end)
        text  = seg.text.strip()
        # Only assign text to the starting second to avoid duplication
        if start not in second_map:
            second_map[start] = text
        else:
            second_map[start] += " " + text

    second_by_second = [
        {"second": sec, "text": second_map[sec]}
        for sec in sorted(second_map.keys())
    ]

    return {
        "full_text": result.text or "",
        "segments": [
            {"start": s.start, "end": s.end, "text": s.text.strip()}
            for s in segments
        ],
        "second_by_second": second_by_second
    }
