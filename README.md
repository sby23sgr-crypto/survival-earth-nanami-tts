---
title: Survival Earth Nanami TTS
emoji: 🌍
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# Survival Earth Nanami TTS

Small HTTP service used by the SURVIVAL EARTH Make scenario.

- Voice: `ja-JP-NanamiNeural`
- Rate: `+18%`
- Output: MP3

Send a JSON `POST` request to `/tts` with a `text` field. When the `API_KEY`
Space secret is configured, include the same value in the `x-api-key` header.

