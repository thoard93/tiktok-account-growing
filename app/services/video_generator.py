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

# Text overlays for videos
TEXT_OVERLAYS = [
    "teamwork trend",
    "teamwork ifb",
    "teamwork makes the dream work",
    "let's go teamwork",
    "teamwork challenge",
    "teamwork goals 💪",
    "teamwork",
    "teamwork time"
]

# Captions for TikTok posts
CAPTIONS = [
    "Teamwork makes the dream work 💪 Who's with me?",
    "Let's go teamwork! Tag your squad 🔥",
    "Teamwork trend hitting different 🌟",
    "Real ones know 🤝 #teamwork",
    "Teamwork energy today ✨",
    "Together we rise 🚀",
    "Squad goals fr fr 💯",
    "Teamwork makes everything better 🙌"
]

# Hashtags (max 5, teamwork focused only)
HASHTAGS = "#teamwork #teamworktrend #teamworkchallenge #teamworkmakesthedream #letsgo"

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
        
        # Output directory for generated videos
        self.output_dir = Path(output_dir or os.getenv("VIDEO_OUTPUT_DIR", "./generated_videos"))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Sound directories
        self.sounds_dir = Path(__file__).parent.parent.parent / "assets" / "sounds"
        self.trending_sounds_dir = self.sounds_dir / "trending"
        self.trending_sounds_dir.mkdir(parents=True, exist_ok=True)
        
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
        text: str,
        font_size: int = 24,
        font_color: str = "white",
        border_color: str = "black",
        border_width: int = 3
    ) -> bool:
        """
        Add centered text overlay to video using FFmpeg.
        
        Args:
            input_video_path: Source video
            output_video_path: Output with overlay
            text: Text to overlay
            font_size: Font size in pixels
            font_color: Text color
            border_color: Outline color
            border_width: Outline thickness
        
        Returns:
            True if successful
        """
        try:
            # FFmpeg drawtext filter with border effect
            # Text centered horizontally and vertically
            drawtext_filter = (
                f"drawtext=text='{text}':"
                f"fontsize={font_size}:"
                f"fontcolor={font_color}:"
                f"borderw={border_width}:"
                f"bordercolor={border_color}:"
                f"x=(w-text_w)/2:"
                f"y=(h-text_h)/2"
            )
            
            cmd = [
                "ffmpeg", "-y",
                "-i", input_video_path,
                "-vf", drawtext_filter,
                "-codec:a", "copy",
                output_video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                logger.info(f"Text overlay added: {text}")
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
    # Main Video Pipeline v3
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
        
        # 5. Add text overlay
        final_text = text_overlay or random.choice(TEXT_OVERLAYS)
        overlay_video_path = self.output_dir / f"overlay_{video_filename}"
        
        if skip_overlay:
            overlay_video_path = raw_video_path
        else:
            overlay_success = self.add_text_overlay(
                str(raw_video_path),
                str(overlay_video_path),
                final_text,
                font_size=18  # Smaller, subtle text overlay
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
        Generate multiple teamwork videos.
        
        Args:
            count: Number of videos to generate
            style_hints: List of style hints to cycle through
            skip_overlay: Skip FFmpeg overlay step
        
        Returns:
            List of GeneratedVideo results
        """
        results = []
        
        # Default diverse style hints
        default_hints = [
            "city park", "tropical beach", "mountain trail", "European village",
            "Japanese garden", "autumn forest", "riverside sunset", "lavender field",
            "snowy alpine path", "downtown at night", "botanical garden", "desert oasis"
        ]
        hints = style_hints or default_hints
        
        for i in range(count):
            hint = hints[i % len(hints)]
            logger.info(f"Generating video {i+1}/{count} (theme: {hint})...")
            
            result = self.generate_teamwork_video(
                style_hint=hint,
                skip_overlay=skip_overlay
            )
            results.append(result)
            
            if result.success:
                logger.info(f"Video {i+1} success: {result.video_path}")
            else:
                logger.error(f"Video {i+1} failed: {result.error}")
            
            # Small delay between generations to avoid rate limits
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
