import os

import edge_tts
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field


VOICE = "ja-JP-NanamiNeural"
RATE = "+18%"

app = FastAPI(title="SURVIVAL EARTH Nanami TTS", version="1.0.0")


class TTSRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


@app.get("/")
async def health() -> dict[str, str]:
    return {"status": "ok", "voice": VOICE, "rate": RATE}


@app.post("/tts")
async def create_voiceover(
    request: TTSRequest,
    x_api_key: str | None = Header(default=None),
) -> Response:
    expected_key = os.environ.get("API_KEY")
    if expected_key and x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    audio = bytearray()
    communicator = edge_tts.Communicate(request.text, VOICE, rate=RATE)
    async for chunk in communicator.stream():
        if chunk["type"] == "audio":
            audio.extend(chunk["data"])

    if not audio:
        raise HTTPException(status_code=502, detail="No audio was generated")

    return Response(
        content=bytes(audio),
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": 'attachment; filename="nanami.mp3"',
            "X-Voice-Name": VOICE,
            "X-Voice-Rate": RATE,
        },
    )

