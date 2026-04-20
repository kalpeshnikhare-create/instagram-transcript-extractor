# transcriber.py

import whisper

# Load once (important for performance)
model = whisper.load_model("base")  # change to "small" if needed


def transcribe_with_timestamps(audio_path: str) -> dict:
    """
    Returns:
    {
        "full_text": "...",
        "segments": [
            {"start": 0.0, "end": 2.1, "text": "..."},
            ...
        ],
        "second_by_second": [
            {"second": 0, "text": "..."},
            {"second": 1, "text": "..."}
        ]
    }
    """

    result = model.transcribe(audio_path)

    segments = result.get("segments", [])

    # 🔹 Build second-by-second transcript
    second_map = {}

    for seg in segments:
        start = int(seg["start"])
        end   = int(seg["end"])
        text  = seg["text"].strip()

        for sec in range(start, end + 1):
            if sec not in second_map:
                second_map[sec] = text
            else:
                second_map[sec] += " " + text

    second_by_second = [
        {"second": sec, "text": second_map[sec]}
        for sec in sorted(second_map.keys())
    ]

    return {
        "full_text": result.get("text", ""),
        "segments": segments,
        "second_by_second": second_by_second
    }
