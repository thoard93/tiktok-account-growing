"""
Teamwork Trend Video Generator v3.0

Full pipeline:
1. Claude generates cinematic image prompt (master-level realism)
2. Nano Banana Pro 2K creates 9:16 image
3. Seedance 1.5 Pro converts to 720p 8s video (no audio)
4. FFmpeg adds centered text overlay
5. FFmpeg adds random trending sound/music
6. FFmpeg strips metadata (removes AI fingerprints)
"""

import os
import random
import subprocess
import logging
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass

from .kie_client import get_kie_client, KieTaskResult

logger = logging.getLogger(__name__)


@dataclass
class GeneratedVideo:
    """Result of video generation pipeline"""
    success: bool
    video_path: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    prompt_used: Optional[str] = None
    text_overlay: Optional[str] = None
    error: Optional[str] = None
    cost_usd: float = 0.0


# ===========================
# Teamwork Content Variations
# ===========================

# Image prompt templates (fallback if Claude is unavailable)
IMAGE_PROMPT_TEMPLATES = [
    "Photorealistic POV walking through a sun-dappled city park, golden afternoon light filtering through cherry blossom trees, a couple walking their dog in the distance, shallow depth of field, warm tones, cinematic",
    "Hyper-realistic POV stroll along a pristine sandy beach at golden hour, soft warm sunlight with lens flare, a jogger running far ahead on the shoreline, gentle ocean waves, natural film grain",
    "Photorealistic POV calm walk through vibrant downtown streets at magic hour, beautiful glass skyscraper reflections, pedestrians crossing in the background, soft bokeh city lights, premium cinematic quality",
    "Ultra-realistic POV peaceful walk through a lush forest trail, volumetric light rays through tall pine trees, a hiker with a backpack visible far ahead, rich earthy greens, shallow depth of field",
    "Photorealistic POV scenic stroll along a mountain trail overlook at sunrise, breathtaking misty valley vista, two friends sitting on rocks in the distance, warm golden light, cinematic lens flare",
    "Hyper-realistic POV gentle walk through Japanese garden path, soft morning light with subtle fog, an elderly couple admiring koi pond ahead, peaceful zen atmosphere, beautiful bokeh",
    "Photorealistic POV relaxed stroll through autumn woods, golden maple leaves falling, a person walking their golden retriever far ahead on the trail, warm soft backlight, natural film grain",
    "Ultra-realistic POV calming walk along a quiet riverside path at sunset, soft golden reflections on water, fishermen visible on the far bank, peaceful nature scene, cinematic color grading",
    "Photorealistic POV morning stroll through lavender fields in Provence, soft purple hues stretching to horizon, a woman in a sundress walking far ahead, warm golden sunlight, shallow depth of field",
    "Hyper-realistic POV evening walk through a European cobblestone street, warm café lights and street lamps, locals dining at sidewalk tables in the background, charming old town ambiance, premium cinematic quality"
]

# Text overlays for videos — Loom-style multi-line format
# Each entry is repeated 8x in a vertical column covering the screen
TEXT_OVERLAY_LINES = [
    "Moot me",
    "Teamwork trend",
    "Follow me",
    "Moot me up",
    "Teamwork ifb",
]

# Captions for TikTok posts — hashtag-focused like the Loom walkthrough
CAPTIONS = [
    "#ifb #moots? #mootmeup #fyp #glazer",
    "#ifb #moots? #teamwork #fyp #glazer",
    "#ifb #moots #mootmeup #fyp #teamworktrend",
    "#ifb #moots? #mootmeup #fyp",
]

# Hashtags — proven growth format from Loom walkthrough
HASHTAGS = "#ifb #moots? #mootmeup #fyp #glazer"

# Cinematic video motion prompts for Seedance 1.5 Pro
VIDEO_MOTION_PROMPTS = [
    "Smooth cinematic forward walking POV motion through the scene, natural gentle camera sway like a leisurely stroll, soft ambient movement with subtle parallax",
    "Premium cinematic steady forward glide, slow natural walking pace, gentle camera bob creating immersive first-person perspective, professional steadicam feel",
    "Smooth forward walking POV with cinematic depth, gentle natural breathing motion in camera, soft light rays shifting as perspective moves through the scene",
    "Ultra-smooth first-person walking motion through the environment, subtle head-turn pan exploring the surroundings, natural human walking rhythm",
    "Cinematic slow walking forward with gentle sway, soft ambient particles floating, dynamic light shifts as the camera moves through the scene naturally"
]

# =========================================
# MASTER CLAUDE SYSTEM PROMPT FOR REALISM
# =========================================

CLAUDE_IMAGE_SYSTEM_PROMPT = """You are a world-class cinematographer and prompt engineer specializing in photorealistic AI image generation. Your job is to create prompts that produce STUNNING, indistinguishable-from-real-life images.

CRITICAL REQUIREMENTS FOR EVERY PROMPT:
1. PHOTOREALISM: Must look like a real photograph, NOT AI-generated. Use terms: "photorealistic", "real photograph", "DSLR quality", "natural film grain"
2. LIGHTING: Always specify premium lighting — golden hour, volumetric light rays, soft shadows, natural lens flare, warm backlighting
3. POV PERSPECTIVE: First-person walking POV looking FORWARD at the horizon/scenery. NEVER show feet, legs, or lower body
4. PEOPLE IN BACKGROUND: Always include 1-3 people naturally placed in the scene — pedestrians walking, joggers, couples, dog walkers, someone sitting on a bench. They should be at MEDIUM TO FAR distance, adding life without being the focus
5. DEPTH: Shallow depth of field with background bokeh, creating cinematic depth layers
6. CAMERA QUALITY: Shot on Sony A7IV or Canon R5, 35mm lens, f/2.8, natural color grading, subtle film grain
7. FORMAT: 9:16 vertical composition optimized for mobile/TikTok
8. DIVERSITY: Vary locations dramatically — city parks, beaches, forests, downtown streets, mountain trails, Japanese gardens, European villages, riverside paths, lavender fields, tropical paths, desert oases, snowy alpine trails
9. ATMOSPHERE: Rich, immersive atmosphere — morning mist, evening glow, flower petals, falling leaves, light rain, snow flurries
10. COLOR: Natural color palette with warm tones, NOT oversaturated. Think Kodak Portra 400 film look

OUTPUT FORMAT: Just the prompt text, nothing else. Keep it under 300 words. Be specific and vivid."""


class VideoGenerator:
    """
    Generates teamwork trend videos using AI.
    
    Pipeline v3: Claude (master prompt) → Nano Banana Pro 2K (image) → Seedance 1.5 Pro (video) → FFmpeg (overlay + sound)
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        """Initialize video generator."""
        self.kie = get_kie_client()
        # Strip whitespace from API key to prevent hidden char issues
        raw_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.claude_api_key = raw_key.strip() if raw_key else None
        
        if self.claude_api_key:
            logger.info(f"ANTHROPIC_API_KEY loaded: {self.claude_api_key[:20]}... (len={len(self.claude_api_key)})")
        else:
            logger.warning("ANTHROPIC_API_KEY not set - will use template prompts")
        
        # Output directory for generated videos — uses Render persistent disk if available
        default_dir = "/var/data/generated_videos" if os.path.isdir("/var/data") else "./generated_videos"
        self.output_dir = Path(output_dir or os.getenv("VIDEO_OUTPUT_DIR", default_dir))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Sound directories
        self.sounds_dir = Path(__file__).parent.parent.parent / "assets" / "sounds"
        self.trending_sounds_dir = self.sounds_dir / "trending"
        self.trending_sounds_dir.mkdir(parents=True, exist_ok=True)
        
        # Track used stock clips to avoid reuse across accounts in same batch
        self._used_clips: set = set()
        
        logger.info(f"VideoGenerator v3 initialized, output: {self.output_dir}")
    
    # ===========================
    # Claude Prompt Generation
    # ===========================
    
    def generate_image_prompt_with_claude(self, style_hint: Optional[str] = None) -> str:
        """
        Use Claude to generate a cinematic, photorealistic image prompt.
        
        Args:
            style_hint: Optional hint like "beach", "forest", "city"
        
        Returns:
            Master-quality image prompt for Nano Banana Pro 2K
        """
        if not self.claude_api_key:
            # Fallback to template if no Claude API
            template = random.choice(IMAGE_PROMPT_TEMPLATES)
            if style_hint:
                template = template.replace("city park", style_hint)
            return template
        
        try:
            import httpx
            
            user_message = "Generate a unique, ultra-photorealistic POV scene prompt for a peaceful walking video. The scene should feel like a real moment captured on a premium camera."
            if style_hint:
                user_message += f" Location theme: {style_hint}"
            user_message += " Remember: include people in the background for realism."
            
            # Debug: log key presence (not the actual key)
            key_preview = self.claude_api_key[:15] + "..." if self.claude_api_key else "None"
            logger.debug(f"Using Claude API key: {key_preview}")
            
            response = httpx.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": self.claude_api_key,
                    "anthropic-version": "2023-06-01"
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 400,
                    "system": CLAUDE_IMAGE_SYSTEM_PROMPT,
                    "messages": [{"role": "user", "content": user_message}]
                },
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            prompt = result.get("content", [{}])[0].get("text", "").strip()
            
            logger.info(f"Claude generated master prompt: {prompt[:100]}...")
            return prompt
            
        except Exception as e:
            logger.warning(f"Claude prompt generation failed: {e}, using template")
            template = random.choice(IMAGE_PROMPT_TEMPLATES)
            return template
    
    def generate_video_motion_prompt(self) -> str:
        """Generate cinematic motion prompt for Seedance 1.5 Pro."""
        return random.choice(VIDEO_MOTION_PROMPTS)
    
    # ===========================
    # FFmpeg Processing
    # ===========================
    
    def add_text_overlay(
        self,
        input_video_path: str,
        output_video_path: str,
        text_line: str,
        repeat_count: int = 8,
        font_size: int = 42,
        font_color: str = "white",
        border_color: str = "black",
        border_width: int = 3
    ) -> bool:
        """
        Add Loom-style multi-line text overlay to video using FFmpeg.
        
        Repeats 'text_line' vertically 8 times in a column, covering ~60% of
        the screen height. Bold white text with black outline, left-of-center.
        Matches the proven growth strategy from the Loom walkthrough.
        
        Args:
            input_video_path: Source video
            output_video_path: Output with overlay
            text_line: Single line to repeat (e.g. "Moot me")
            repeat_count: How many times to repeat (default 8)
            font_size: Font size in pixels (default 42 for 720p)
            font_color: Text color
            border_color: Outline color
            border_width: Outline thickness
        
        Returns:
            True if successful
        """
        try:
            # Build stacked drawtext filters — one per line
            # Video is 9:16 (720x1280), so height is 1280px
            # 8 lines at font_size 42 with 12px spacing = 8 * 54 = 432px total
            # Center vertically: start_y = (1280 - 432) / 2 ≈ 424
            line_height = font_size + 12  # font + spacing
            total_height = repeat_count * line_height
            start_y = f"(h-{total_height})/2"  # dynamic centering
            
            # Escape single quotes in text for FFmpeg
            safe_text = text_line.replace("'", "'\\\''")
            
            filters = []
            for i in range(repeat_count):
                y_pos = f"{start_y}+{i * line_height}"
                drawtext = (
                    f"drawtext=text='{safe_text}':"
                    f"fontsize={font_size}:"
                    f"fontcolor={font_color}:"
                    f"borderw={border_width}:"
                    f"bordercolor={border_color}:"
                    f"x=(w-text_w)/2:"
                    f"y={y_pos}"
                )
                filters.append(drawtext)
            
            # Chain all drawtext filters with commas
            vf_string = ",".join(filters)
            
            cmd = [
                "ffmpeg", "-y",
                "-i", input_video_path,
                "-vf", vf_string,
                "-codec:a", "copy",
                output_video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                logger.info(f"Multi-line text overlay added: '{text_line}' x{repeat_count}")
                return True
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False
                
        except FileNotFoundError:
            logger.error("FFmpeg not found - text overlay skipped")
            return False
        except Exception as e:
            logger.error(f"Text overlay failed: {e}")
            return False
    
    def strip_metadata(self, input_video_path: str, output_video_path: str) -> bool:
        """
        Strip all metadata from video to remove AI generation fingerprints.
        
        This helps videos appear more "original" and can help bypass
        platform detection of AI-generated content.
        
        Args:
            input_video_path: Source video
            output_video_path: Output without metadata
        
        Returns:
            True if successful
        """
        try:
            cmd = [
                "ffmpeg", "-y",
                "-i", input_video_path,
                "-map_metadata", "-1",    # Strip all metadata
                "-fflags", "+bitexact",   # Remove encoder signatures
                "-flags:v", "+bitexact",
                "-flags:a", "+bitexact",
                "-c:v", "libx264",        # Re-encode video
                "-preset", "fast",
                "-crf", "23",
                "-c:a", "aac",            # Re-encode audio
                "-b:a", "128k",
                output_video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0:
                logger.info("Metadata stripped successfully")
                return True
            else:
                logger.error(f"Metadata strip error: {result.stderr[:200]}")
                return False
                
        except FileNotFoundError:
            logger.error("FFmpeg not found - metadata not stripped")
            return False
        except Exception as e:
            logger.error(f"Metadata strip failed: {e}")
            return False
    
    # Search queries to rotate through for variety
    SOUND_SEARCH_QUERIES = [
        "upbeat pop music",
        "trending beat",
        "catchy melody loop",
        "energetic hip hop beat",
        "viral music tiktok",
        "happy background music",
        "motivational beat drop",
        "modern trap beat",
        "chill lofi beat",
        "dance music electronic",
        "acoustic guitar happy",
        "piano emotional",
        "cinematic inspiring music",
        "funky groove beat",
        "summer vibes music"
    ]
    
    def _fetch_sounds_from_freesound(self, count: int = 5) -> int:
        """
        Fetch trending/popular sounds from Freesound.org and cache locally.
        Uses preview-hq-mp3 URLs which don't require OAuth2.
        
        Args:
            count: Number of sounds to fetch
        
        Returns:
            Number of sounds successfully downloaded
        """
        import httpx
        
        api_key = os.getenv("FREESOUND_API_KEY")
        if not api_key:
            logger.warning("FREESOUND_API_KEY not set — cannot auto-fetch sounds")
            return 0
        
        downloaded = 0
        query = random.choice(self.SOUND_SEARCH_QUERIES)
        
        try:
            # Search for music sounds, sorted by rating, filtered by duration
            params = {
                "query": query,
                "token": api_key,
                "fields": "id,name,previews,duration,avg_rating,num_downloads",
                "filter": "duration:[5 TO 30]",  # 5-30 second clips
                "sort": "rating_desc",
                "page_size": 15
            }
            
            logger.info(f"Fetching sounds from Freesound (query: '{query}')...")
            
            with httpx.Client(timeout=30) as client:
                resp = client.get("https://freesound.org/apiv2/search/text/", params=params)
                resp.raise_for_status()
                data = resp.json()
            
            results = data.get("results", [])
            if not results:
                logger.warning(f"No Freesound results for query: {query}")
                return 0
            
            # Pick random results from top-rated
            selected = random.sample(results, min(count, len(results)))
            
            for sound in selected:
                try:
                    preview_url = sound.get("previews", {}).get("preview-hq-mp3")
                    if not preview_url:
                        continue
                    
                    sound_id = sound.get("id", "unknown")
                    # Sanitize name for filename
                    safe_name = "".join(c if c.isalnum() or c in "._- " else "" for c in sound.get("name", str(sound_id)))
                    safe_name = safe_name.strip()[:50]
                    filename = f"fs_{sound_id}_{safe_name}.mp3"
                    filepath = self.trending_sounds_dir / filename
                    
                    # Skip if already cached
                    if filepath.exists():
                        logger.debug(f"Sound already cached: {filename}")
                        downloaded += 1
                        continue
                    
                    # Download preview MP3 (no auth needed for CDN links)
                    with httpx.Client(timeout=30) as client:
                        audio_resp = client.get(preview_url)
                        audio_resp.raise_for_status()
                        filepath.write_bytes(audio_resp.content)
                    
                    logger.info(f"Downloaded sound: {filename} ({sound.get('duration', '?')}s)")
                    downloaded += 1
                    
                except Exception as e:
                    logger.warning(f"Failed to download sound {sound.get('id')}: {e}")
                    continue
            
        except Exception as e:
            logger.error(f"Freesound fetch failed: {e}")
        
        return downloaded
    
    def get_random_trending_sound(self) -> Optional[Path]:
        """
        Pick a random trending sound. Auto-fetches from Freesound.org if cache is low.
        Falls back to teamwork_trend.mp3 if everything fails.
        
        Returns:
            Path to a random sound file, or None if none available
        """
        # Check cached trending sounds
        trending_files = list(self.trending_sounds_dir.glob("*.mp3")) + \
                         list(self.trending_sounds_dir.glob("*.wav")) + \
                         list(self.trending_sounds_dir.glob("*.m4a"))
        
        # Filter out README files
        trending_files = [f for f in trending_files if f.suffix in ('.mp3', '.wav', '.m4a')]
        
        # Auto-fetch if cache has fewer than 5 sounds
        if len(trending_files) < 5:
            fetched = self._fetch_sounds_from_freesound(count=8)
            if fetched > 0:
                # Refresh file list
                trending_files = list(self.trending_sounds_dir.glob("*.mp3")) + \
                                 list(self.trending_sounds_dir.glob("*.wav")) + \
                                 list(self.trending_sounds_dir.glob("*.m4a"))
        
        if trending_files:
            chosen = random.choice(trending_files)
            logger.info(f"Using trending sound: {chosen.name}")
            return chosen
        
        # Fall back to teamwork_trend.mp3
        fallback = self.sounds_dir / "teamwork_trend.mp3"
        if fallback.exists():
            logger.info("No trending sounds found, using teamwork_trend.mp3")
            return fallback
        
        logger.warning("No sound files available at all")
        return None
    
    def add_sound_to_video(
        self,
        input_video_path: str,
        output_video_path: str,
        sound_path: Optional[str] = None
    ) -> bool:
        """
        Add background sound/music to video using FFmpeg.
        
        If no sound_path specified, picks a random trending sound.
        
        Args:
            input_video_path: Source video (with text overlay)
            output_video_path: Output with audio
            sound_path: Path to audio file (None = random trending sound)
        
        Returns:
            True if successful
        """
        try:
            # Pick a random trending sound if none specified
            if sound_path is None:
                sound_file = self.get_random_trending_sound()
                if sound_file is None:
                    logger.warning("No sound files available, copying video without audio")
                    import shutil
                    shutil.copy(input_video_path, output_video_path)
                    return True
                sound_path = str(sound_file)
            
            sound_path = Path(sound_path)
            
            if not sound_path.exists():
                logger.warning(f"Sound file not found: {sound_path}, skipping audio")
                import shutil
                shutil.copy(input_video_path, output_video_path)
                return True
            
            # FFmpeg command to mux audio with video
            # -shortest: Crop audio to video length
            cmd = [
                "ffmpeg", "-y",
                "-i", input_video_path,      # Video input
                "-i", str(sound_path),        # Audio input
                "-c:v", "copy",               # No re-encode video (fast)
                "-c:a", "aac",                # TikTok-friendly audio codec
                "-shortest",                  # Crop audio to video length
                "-map", "0:v:0",              # Video from first input
                "-map", "1:a:0",              # Audio from second input
                output_video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info(f"Sound added: {sound_path.name if isinstance(sound_path, Path) else sound_path}")
                return True
            else:
                logger.error(f"FFmpeg audio mux error: {result.stderr[:200]}")
                # Fall back to video without sound
                import shutil
                shutil.copy(input_video_path, output_video_path)
                return False
                
        except FileNotFoundError:
            logger.error("FFmpeg not found - sound not added")
            return False
        except Exception as e:
            logger.error(f"Sound addition failed: {e}")
            return False
    
    # ===========================
    # YouTube Scene-Clipping Pipeline (FREE, unique clips)
    # ===========================
    
    # Search queries for finding long compilation videos on YouTube
    # yt-dlp uses "ytsearch3:" prefix to find 3 results per query
    YOUTUBE_SEARCH_QUERIES = [
        "4K city timelapse compilation",
        "city night timelapse 4K",
        "nature scenery montage 4K",
        "sunset timelapse collection",
        "drone city footage compilation",
        "cinematic nature b-roll 4K",
        "city skyline timelapse night",
        "ocean waves cinematic 4K",
        "mountain landscape timelapse",
        "aerial city drone footage",
        "tokyo night timelapse 4K",
        "new york city timelapse",
        "london city timelapse",
        "nature documentary b-roll",
        "city traffic timelapse night",
    ]
    
    def fetch_youtube_source_videos(self, max_videos: int = 2) -> int:
        """
        Auto-search YouTube for long time-lapse/scenery compilations and download them.
        Uses yt-dlp's ytsearch to find videos automatically — no manual URL curation needed.
        
        Downloads to {output_dir}/youtube_sources/ for later scene extraction.
        
        Args:
            max_videos: Max number of source videos to download per run
            
        Returns:
            Number of videos successfully downloaded
        """
        import yt_dlp
        
        source_dir = self.output_dir / "youtube_sources"
        source_dir.mkdir(parents=True, exist_ok=True)
        
        # Check existing sources
        existing = list(source_dir.glob("*.mp4"))
        if len(existing) >= 5:
            logger.info(f"YouTube source cache has {len(existing)} videos — sufficient")
            return len(existing)
        
        downloaded = 0
        query = random.choice(self.YOUTUBE_SEARCH_QUERIES)
        search_term = f"ytsearch3:{query}"  # Search for 3 results
        
        logger.info(f"Searching YouTube for: '{query}'")
        
        ydl_opts = {
            "format": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best[height<=720]",
            "merge_output_format": "mp4",
            "outtmpl": str(source_dir / "yt_%(id)s.%(ext)s"),
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            # Only download videos 3-30 minutes long (compilations)
            "match_filter": yt_dlp.utils.match_filter_func("duration >= 180 & duration <= 1800"),
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # First extract info to get video IDs
                info = ydl.extract_info(search_term, download=False)
                
                if not info or "entries" not in info:
                    logger.warning(f"No YouTube results for '{query}'")
                    return 0
                
                entries = list(info["entries"])
                
                for entry in entries[:max_videos]:
                    if entry is None:
                        continue
                    
                    video_id = entry.get("id", "unknown")
                    title = entry.get("title", "Unknown")
                    duration = entry.get("duration", 0)
                    
                    # Skip if already downloaded
                    target_path = source_dir / f"yt_{video_id}.mp4"
                    if target_path.exists():
                        logger.info(f"  Already cached: {title} ({duration}s)")
                        continue
                    
                    logger.info(f"  Downloading: {title} ({duration}s)...")
                    
                    try:
                        ydl.download([entry["webpage_url"]])
                        
                        if target_path.exists():
                            size_mb = target_path.stat().st_size / 1024 / 1024
                            logger.info(f"  ✓ Downloaded: {title} ({size_mb:.1f}MB)")
                            downloaded += 1
                        else:
                            # yt-dlp may have saved with a slightly different name
                            # Check for any new file with this video ID
                            matches = list(source_dir.glob(f"yt_{video_id}.*"))
                            if matches:
                                # Rename to .mp4 if needed
                                if matches[0].suffix != ".mp4":
                                    matches[0].rename(target_path)
                                downloaded += 1
                                logger.info(f"  ✓ Downloaded: {title}")
                            else:
                                logger.warning(f"  ⚠ Download completed but file not found for {video_id}")
                    except Exception as e:
                        logger.warning(f"  ✗ Failed to download {title}: {e}")
                        continue
                
        except Exception as e:
            logger.error(f"YouTube search failed: {e}")
        
        logger.info(f"YouTube fetch complete: {downloaded} new source videos")
        return downloaded
    
    def detect_scenes(self, video_path: str, threshold: float = 0.3) -> List[float]:
        """
        Detect scene changes in a video using FFmpeg's scene detection filter.
        
        Uses select='gt(scene,threshold)' to find timestamps where major visual
        changes occur (cuts between different scenes in a compilation).
        
        Args:
            video_path: Path to the source video
            threshold: Scene change sensitivity (0.0-1.0, lower = more sensitive)
                       0.3 = moderate (catches clear cuts, ignores minor changes)
                       
        Returns:
            List of timestamps (in seconds) where new scenes begin
        """
        try:
            # FFmpeg scene detection: outputs timestamps where scene score > threshold
            cmd = [
                "ffmpeg", "-i", video_path,
                "-vf", f"select='gt(scene,{threshold})',showinfo",
                "-vsync", "vfr",
                "-f", "null", "-"
            ]
            
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=300
            )
            
            # Parse showinfo output for timestamps
            # Format: [Parsed_showinfo_0 ...] n:123 pts:12345 pts_time:45.678 ...
            timestamps = []
            for line in result.stderr.split("\n"):
                if "pts_time:" in line:
                    try:
                        pts_part = line.split("pts_time:")[1]
                        ts = float(pts_part.split()[0])
                        timestamps.append(ts)
                    except (ValueError, IndexError):
                        continue
            
            # Always include 0.0 as the first scene
            if not timestamps or timestamps[0] > 1.0:
                timestamps.insert(0, 0.0)
            
            # Filter out scenes too close together (< 5 seconds apart)
            filtered = [timestamps[0]]
            for ts in timestamps[1:]:
                if ts - filtered[-1] >= 5.0:
                    filtered.append(ts)
            
            logger.info(f"Detected {len(filtered)} scenes in {video_path}")
            return filtered
            
        except subprocess.TimeoutExpired:
            logger.error(f"Scene detection timed out for {video_path}")
            return [0.0]
        except Exception as e:
            logger.error(f"Scene detection failed: {e}")
            return [0.0]
    
    def extract_scene_clips(
        self,
        source_path: str,
        scenes: List[float],
        clip_duration: int = 8,
        max_clips: int = 50
    ) -> int:
        """
        Extract unique clips from each detected scene in a YouTube source video.
        Each clip is cropped to 9:16 (720x1280) for TikTok.
        
        Args:
            source_path: Path to the YouTube source video
            scenes: List of scene-change timestamps from detect_scenes()
            clip_duration: Length of each clip (7-10 seconds)
            max_clips: Max clips to extract per source video
            
        Returns:
            Number of clips successfully extracted
        """
        scene_dir = self.output_dir / "scene_clips"
        scene_dir.mkdir(parents=True, exist_ok=True)
        
        # Get video ID from filename (yt_VIDEOID.mp4)
        source_name = Path(source_path).stem  # e.g., "yt_dQw4w9WgXcQ"
        
        # Get total video duration
        try:
            probe_cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                source_path
            ]
            probe_result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=15)
            total_duration = float(probe_result.stdout.strip() or "0")
        except Exception:
            total_duration = 0
        
        extracted = 0
        
        for i, scene_ts in enumerate(scenes[:max_clips]):
            # Randomize clip duration slightly (7-10 seconds)
            this_clip_duration = random.randint(7, 10)
            
            # Make sure we have enough video left for this clip
            if total_duration > 0 and scene_ts + this_clip_duration > total_duration:
                continue
            
            clip_filename = f"{source_name}_scene{i:03d}.mp4"
            clip_path = scene_dir / clip_filename
            
            if clip_path.exists():
                extracted += 1  # Already extracted
                continue
            
            try:
                # Clip + force crop to 9:16 (720x1280) + strip audio
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", str(scene_ts),
                    "-i", source_path,
                    "-t", str(this_clip_duration),
                    "-vf", "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280",
                    "-an",  # Strip audio (we add our own trending sound)
                    "-c:v", "libx264",
                    "-preset", "fast",
                    "-movflags", "+faststart",
                    clip_path
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0 and clip_path.exists():
                    extracted += 1
                    if extracted % 10 == 0:
                        logger.info(f"  Extracted {extracted} clips so far...")
                else:
                    logger.debug(f"  Clip {i} failed: {result.stderr[:100]}")
                    
            except Exception as e:
                logger.debug(f"  Clip {i} extraction error: {e}")
                continue
        
        logger.info(f"Extracted {extracted} scene clips from {source_name}")
        return extracted
    
    def clip_stock_footage(self, source_path: str, output_path: str, duration: int = 8) -> bool:
        """
        Clip a stock video to a short segment (7-10 seconds) for TikTok.
        Picks a random start point and crops to 9:16 if needed.
        
        Args:
            source_path: Path to full stock video
            output_path: Path for clipped output
            duration: Target clip length in seconds
            
        Returns:
            True if successful
        """
        try:
            # Get video duration first
            probe_cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                source_path
            ]
            probe_result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=15)
            total_duration = float(probe_result.stdout.strip() or "0")
            
            if total_duration < duration + 1:
                # Video too short, use the whole thing
                start_time = 0
            else:
                # Random start point, leaving room for the clip
                max_start = total_duration - duration - 1
                start_time = random.uniform(0, max(0, max_start))
            
            # Clip + ensure 9:16 + normalize to 720x1280
            cmd = [
                "ffmpeg", "-y",
                "-ss", str(start_time),
                "-i", source_path,
                "-t", str(duration),
                "-vf", "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280",
                "-an",  # Strip audio (we add our own sound)
                "-c:v", "libx264",
                "-preset", "fast",
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info(f"Stock clip created: {duration}s from {start_time:.1f}s")
                return True
            else:
                logger.error(f"Clip failed: {result.stderr[:200]}")
                return False
                
        except Exception as e:
            logger.error(f"Stock clipping failed: {e}")
            return False
    
    def generate_stock_video(
        self,
        text_overlay: Optional[str] = None,
    ) -> 'GeneratedVideo':
        """
        Generate a video using unique scene clips from YouTube compilations.
        
        Pipeline:
        1. Pick random scene clip (auto-fetch + extract if cache is low)
        2. Already 9:16 cropped to 720x1280 from extraction step
        3. Add Loom-style multi-line text overlay ("Moot me" x8)
        4. Add trending sound
        5. Strip metadata
        
        Cost: $0.00 — uses free YouTube footage with unique scene cuts
        """
        start_time = time.time()
        
        # Ensure we have scene clips available
        scene_dir = self.output_dir / "scene_clips"
        scene_dir.mkdir(parents=True, exist_ok=True)
        scene_clips = list(scene_dir.glob("*.mp4"))
        
        if len(scene_clips) < 5:
            logger.info("Low scene clip cache — fetching YouTube sources and extracting...")
            self._replenish_scene_clips()
            scene_clips = list(scene_dir.glob("*.mp4"))
        
        if not scene_clips:
            logger.error("No scene clips available — falling back to AI pipeline")
            return self.generate_teamwork_video(text_overlay=text_overlay)
        
        # 1. Pick a scene clip NOT already used in this batch
        unused_clips = [c for c in scene_clips if c.name not in self._used_clips]
        if not unused_clips:
            # All clips used — reset tracker and try to get more
            logger.info("All scene clips used in this batch — resetting tracker and fetching more")
            self._used_clips.clear()
            self._replenish_scene_clips()
            scene_clips = list(scene_dir.glob("*.mp4"))
            unused_clips = scene_clips
        
        source_clip = random.choice(unused_clips)
        self._used_clips.add(source_clip.name)  # Mark as used
        logger.info(f"Using scene clip: {source_clip.name} (used {len(self._used_clips)}/{len(scene_clips)} unique clips)")
        
        # 2. Scene clip is already 9:16 (720x1280) — just copy it for processing
        video_filename = f"teamwork_{int(time.time())}_{random.randint(1000, 9999)}.mp4"
        raw_clip_path = self.output_dir / f"raw_{video_filename}"
        final_video_path = self.output_dir / video_filename
        
        # Copy scene clip to working file
        import shutil
        shutil.copy2(str(source_clip), str(raw_clip_path))
        
        # 3. Add Loom-style multi-line text overlay
        final_text_line = text_overlay or random.choice(TEXT_OVERLAY_LINES)
        overlay_path = self.output_dir / f"overlay_{video_filename}"
        
        overlay_success = self.add_text_overlay(
            str(raw_clip_path),
            str(overlay_path),
            final_text_line,
            repeat_count=8,
            font_size=42
        )
        
        if overlay_success:
            raw_clip_path.unlink(missing_ok=True)
        else:
            overlay_path = raw_clip_path
            logger.warning("Using clip without text overlay")
        
        # 4. Add trending sound
        sound_path = self.output_dir / f"sound_{video_filename}"
        sound_success = self.add_sound_to_video(
            str(overlay_path),
            str(sound_path)
        )
        
        if sound_success and sound_path.exists():
            if overlay_path != raw_clip_path:
                overlay_path.unlink(missing_ok=True)
        else:
            sound_path = overlay_path
            logger.warning("Using video without sound")
        
        # 5. Strip metadata
        strip_success = self.strip_metadata(
            str(sound_path),
            str(final_video_path)
        )
        
        if strip_success:
            if sound_path != overlay_path and sound_path != raw_clip_path:
                sound_path.unlink(missing_ok=True)
        else:
            if sound_path.exists():
                sound_path.rename(final_video_path)
        
        duration = time.time() - start_time
        
        if final_video_path.exists():
            logger.info(f"Scene clip video generated in {duration:.1f}s: {final_video_path.name}")
            return GeneratedVideo(
                success=True,
                video_path=str(final_video_path),
                text_overlay=final_text_line,
                cost_usd=0.00  # FREE!
            )
        else:
            return GeneratedVideo(
                success=False,
                error="Scene clip video pipeline failed",
                cost_usd=0.00
            )
    
    def _replenish_scene_clips(self):
        """
        Auto-fetch YouTube source videos and extract scene clips.
        Called when scene_clips cache is running low.
        """
        # Step 1: Fetch YouTube source videos
        self.fetch_youtube_source_videos(max_videos=2)
        
        # Step 2: Detect scenes & extract clips from all un-processed sources
        source_dir = self.output_dir / "youtube_sources"
        scene_dir = self.output_dir / "scene_clips"
        
        if not source_dir.exists():
            return
        
        for source_video in source_dir.glob("*.mp4"):
            source_name = source_video.stem
            
            # Check if we already extracted clips from this source
            existing_clips = list(scene_dir.glob(f"{source_name}_scene*.mp4"))
            if len(existing_clips) >= 5:
                continue  # Already processed
            
            logger.info(f"Processing YouTube source: {source_name}...")
            
            # Detect scenes
            scenes = self.detect_scenes(str(source_video), threshold=0.3)
            logger.info(f"  Found {len(scenes)} scenes")
            
            # Extract clips from each scene (already cropped to 9:16)
            extracted = self.extract_scene_clips(
                str(source_video),
                scenes,
                max_clips=50
            )
            logger.info(f"  Extracted {extracted} unique clips from {source_name}")
    
    # ===========================
    # Main Video Pipeline v3 (AI - costs ~$0.20/video)
    # ===========================
    
    def generate_teamwork_video(
        self,
        style_hint: Optional[str] = None,
        text_overlay: Optional[str] = None,
        skip_overlay: bool = False
    ) -> GeneratedVideo:
        """
        Generate a complete teamwork trend video.
        
        Pipeline v3:
        1. Claude generates cinematic image prompt (master-level realism)
        2. Nano Banana Pro 2K creates 9:16 image
        3. Seedance 1.5 Pro converts to 720p 8s video (no audio)
        4. FFmpeg adds text overlay
        5. FFmpeg adds random trending sound
        6. FFmpeg strips metadata
        
        Args:
            style_hint: Location style hint (beach, forest, city, etc.)
            text_overlay: Custom text, or random from list
            skip_overlay: Skip FFmpeg overlay step
        
        Returns:
            GeneratedVideo with paths and URLs
        """
        cost = 0.0
        
        # 1. Generate image prompt with Claude (master-level realism)
        logger.info("Step 1: Generating cinematic image prompt...")
        image_prompt = self.generate_image_prompt_with_claude(style_hint)
        
        # 2. Generate image with Nano Banana Pro 2K
        logger.info("Step 2: Generating 2K image with Nano Banana Pro...")
        image_result = self.kie.generate_image(
            prompt=image_prompt,
            aspect_ratio="9:16",
            resolution="2K",  # Upgraded from 1K
            output_format="png"
        )
        
        if not image_result.success:
            return GeneratedVideo(
                success=False,
                error=f"Image generation failed: {image_result.error}",
                prompt_used=image_prompt
            )
        
        # Wait for image
        logger.info(f"Waiting for image task {image_result.task_id}...")
        image_final = self.kie.wait_for_task(image_result.task_id, timeout_seconds=180)
        
        if not image_final.success or not image_final.result_urls:
            return GeneratedVideo(
                success=False,
                error=f"Image generation failed: {image_final.error or 'No result URLs'}",
                prompt_used=image_prompt
            )
        
        image_url = image_final.result_urls[0]
        cost += 0.12  # Nano Banana Pro 2K cost
        logger.info(f"2K Image generated: {image_url}")
        
        # 3. Convert to video with Seedance 1.5 Pro (720p, 8s, no audio)
        logger.info("Step 3: Converting to cinema-quality video with Seedance 1.5 Pro...")
        video_prompt = self.generate_video_motion_prompt()
        
        video_result = self.kie.image_to_video_seedance(
            image_url=image_url,
            prompt=video_prompt,
            aspect_ratio="9:16",
            resolution="720p",
            duration="8",
            fixed_lens=False,       # Dynamic camera movement
            generate_audio=False    # No AI audio, we add trending sound later
        )
        
        if not video_result.success:
            return GeneratedVideo(
                success=False,
                error=f"Seedance video failed: {video_result.error}",
                image_url=image_url,
                prompt_used=image_prompt,
                cost_usd=cost
            )
        
        # Wait for video (Seedance can take longer)
        logger.info(f"Waiting for Seedance video task {video_result.task_id}...")
        video_final = self.kie.wait_for_task(video_result.task_id, timeout_seconds=600)
        
        if not video_final.success or not video_final.result_urls:
            return GeneratedVideo(
                success=False,
                error=f"Seedance video failed: {video_final.error or 'No result URLs'}",
                image_url=image_url,
                prompt_used=image_prompt,
                cost_usd=cost
            )
        
        video_url = video_final.result_urls[0]
        cost += 0.14  # Seedance 720p/8s no-audio cost
        logger.info(f"Cinema video generated: {video_url}")
        
        # 4. Download video
        video_filename = f"teamwork_{int(time.time())}_{random.randint(1000, 9999)}.mp4"
        raw_video_path = self.output_dir / f"raw_{video_filename}"
        final_video_path = self.output_dir / video_filename
        
        try:
            import httpx
            logger.info("Downloading video...")
            with httpx.Client(timeout=60) as client:
                response = client.get(video_url)
                response.raise_for_status()
                raw_video_path.write_bytes(response.content)
            logger.info(f"Video downloaded: {raw_video_path}")
        except Exception as e:
            return GeneratedVideo(
                success=False,
                error=f"Video download failed: {e}",
                image_url=image_url,
                video_url=video_url,
                prompt_used=image_prompt,
                cost_usd=cost
            )
        
        # 5. Add Loom-style multi-line text overlay
        final_text_line = text_overlay or random.choice(TEXT_OVERLAY_LINES)
        overlay_video_path = self.output_dir / f"overlay_{video_filename}"
        
        if skip_overlay:
            overlay_video_path = raw_video_path
        else:
            overlay_success = self.add_text_overlay(
                str(raw_video_path),
                str(overlay_video_path),
                final_text_line,  # Repeated 8x vertically
                repeat_count=8,
                font_size=42   # Large bold text covering ~60% of screen
            )
            
            if overlay_success:
                raw_video_path.unlink(missing_ok=True)  # Delete raw
            else:
                # Fallback: use raw video without overlay
                overlay_video_path = raw_video_path
                logger.warning("Using video without text overlay")
        
        # 6. Add random trending sound
        logger.info("Step 6: Adding trending sound...")
        sound_video_path = self.output_dir / f"sound_{video_filename}"
        sound_success = self.add_sound_to_video(
            str(overlay_video_path),
            str(sound_video_path)
        )
        
        if sound_success and sound_video_path.exists():
            # Delete overlay intermediate
            if overlay_video_path != raw_video_path:
                overlay_video_path.unlink(missing_ok=True)
        else:
            # Fallback: use video without sound
            sound_video_path = overlay_video_path
            logger.warning("Using video without sound")
        
        # 7. Strip metadata to remove AI fingerprints
        logger.info("Step 7: Stripping metadata...")
        strip_success = self.strip_metadata(
            str(sound_video_path),
            str(final_video_path)
        )
        
        if strip_success:
            # Delete intermediate file
            if sound_video_path != overlay_video_path and sound_video_path != raw_video_path:
                sound_video_path.unlink(missing_ok=True)
        else:
            # Fallback: use video with metadata
            if sound_video_path.exists():
                sound_video_path.rename(final_video_path)
            logger.warning("Using video with metadata (strip failed)")
        
        return GeneratedVideo(
            success=True,
            video_path=str(final_video_path),
            image_url=image_url,
            video_url=video_url,
            prompt_used=image_prompt,
            text_overlay=final_text if not skip_overlay else None,
            cost_usd=cost
        )
    
    def generate_batch(
        self,
        count: int = 5,
        style_hints: Optional[List[str]] = None,
        skip_overlay: bool = False
    ) -> List[GeneratedVideo]:
        """
        Generate multiple videos using YouTube scene clips (FREE, unique).
        Each video uses a unique clip to prevent duplicate content violations.
        
        Args:
            count: Number of videos to generate
            style_hints: Ignored (kept for API compatibility)
            skip_overlay: Ignored (kept for API compatibility)
        
        Returns:
            List of GeneratedVideo results
        """
        results = []
        
        # Reset used clips for fresh batch uniqueness
        self._used_clips.clear()
        
        for i in range(count):
            logger.info(f"Generating stock video {i+1}/{count}...")
            
            result = self.generate_stock_video()
            results.append(result)
            
            if result.success:
                logger.info(f"Video {i+1} success: {result.video_path} ($0.00)")
            else:
                logger.error(f"Video {i+1} failed: {result.error}")
            
            # Small delay between generations
            if i < count - 1:
                time.sleep(2)
        
        return results
    
    # ===========================
    # TikTok Content Helpers
    # ===========================
    
    @staticmethod
    def get_random_caption() -> str:
        """Get random caption for TikTok post."""
        return random.choice(CAPTIONS)
    
    @staticmethod
    def get_hashtags() -> str:
        """Get standard hashtag set."""
        return HASHTAGS
    
    @staticmethod
    def get_full_description() -> str:
        """Get random caption with hashtags."""
        return f"{random.choice(CAPTIONS)} {HASHTAGS}"


# Module-level instance
_generator: Optional[VideoGenerator] = None

def get_video_generator() -> VideoGenerator:
    """Get or create video generator singleton."""
    global _generator
    if _generator is None:
        _generator = VideoGenerator()
    return _generator
