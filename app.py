from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os

from downloader import download_instagram_audio
from transcriber import transcribe_with_timestamps

app = FastAPI()

@app.on_event("startup")
async def startup_check():
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY environment variable is not set")


@app.get("/")
def home():
    return {"status": "audio-transcription-service-running"}


@app.get("/audio-transcript")
def audio_transcript(url: str):
    """
    Pipeline:
    Instagram URL → audio → Whisper → timestamped transcript
    """

    try:
        # Step 1: Download audio
        audio_path = download_instagram_audio(url)

        # Step 2: Transcribe
        transcript_data = transcribe_with_timestamps(audio_path)

        # Optional cleanup
        try:
            os.remove(audio_path)
        except Exception:
            pass

        return JSONResponse({
            "status": "success",
            "transcript": transcript_data
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
