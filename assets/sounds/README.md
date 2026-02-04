# TikTok Sound Assets

Place your TikTok trend sounds here for FFmpeg to mux into generated videos.

## Required File

- **teamwork_trend.mp3** - The teamwork trend sound (download from TikTok downloader site)

## How to Get the Sound

1. Find a TikTok using the teamwork trend sound
2. Copy the video URL
3. Go to ssstik.io or tiktokio.com
4. Paste URL, select "Audio only" or MP3
5. Download and rename to `teamwork_trend.mp3`
6. Place in this folder
7. Git add/commit/push

## File Requirements

- Format: MP3 (AAC also works)
- Duration: Any length (FFmpeg auto-crops to video length)
- Quality: 128kbps+ recommended

## Multiple Sounds

You can add multiple sound files and modify `video_generator.py` to randomly select:

```python
sounds = ["teamwork_trend.mp3", "motivation_beat.mp3", "inspiring_music.mp3"]
sound_path = base_path / "assets" / "sounds" / random.choice(sounds)
```
