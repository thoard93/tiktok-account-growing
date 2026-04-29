# JesusAI Sound Library

Drop trending TikTok audio files here. Each generated JesusAI video gets a
random sound from this folder muxed in by FFmpeg.

## Where to put files

- `assets/sounds/trending/` — primary location for trending sounds (uploaded
  via the dashboard's **🎵 Sounds** tab go here automatically).
- `assets/sounds/` — also scanned recursively, so any subfolder works.

## Supported formats

- `.mp3`, `.wav`, `.m4a`, `.ogg`
- Any duration (FFmpeg auto-crops to video length, default 5-6s)
- 128kbps+ recommended

## How to get a trending sound

1. Find a TikTok using the audio you want
2. Copy the video URL
3. Use ssstik.io or tiktokio.com → "Audio only" / MP3
4. Drop the file in via the **🎵 Sounds** tab in the dashboard, or place it
   in `assets/sounds/trending/` directly.

The first available file is picked randomly per generation. No manual
configuration needed.
