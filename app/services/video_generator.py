"""
Teamwork Trend Video Generator

Full pipeline:
1. Claude generates unique image prompt
2. Nano Banana Pro creates 9:16 image
3. Grok Imagine converts to 10s video
4. FFmpeg adds centered text overlay
5. FFmpeg strips metadata (removes AI fingerprints)
6. Video ready for GeeLark upload/posting
"""

import os
import random
import httpx
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

# Image prompt templates (for Claude to enhance)
IMAGE_PROMPT_TEMPLATES = [
    "POV shot walking through a sunny nature park trail with green trees and dappled sunlight",
    "POV walking along a beautiful beach at golden hour sunset with gentle waves",
    "POV strolling through a vibrant city park in spring with blooming flowers",
    "POV hiking a scenic mountain trail with stunning vistas ahead",
    "POV walking along a waterfront boardwalk with boats and calm water",
    "POV exploring a peaceful forest path with sunlight filtering through leaves",
    "POV walking through a beautiful garden with colorful flowers",
    "POV strolling downtown city street with nice architecture and trees"
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

# Hashtags (standard set)
HASHTAGS = "#teamwork #teamworktrend #teamworkchallenge #teamworkmakesthedreamwork #fyp #viral #motivation #squadgoals"

# Video motion prompts
VIDEO_MOTION_PROMPTS = [
    "Smooth steady camera walking forward motion through the scene, natural subtle movement",
    "Gentle forward walking motion, steady POV camera movement exploring the area",
    "Calm walking movement through the scene, steady smooth camera motion",
    "Natural walking pace forward through the environment, relaxed camera motion"
]


class VideoGenerator:
    """
    Generates teamwork trend videos using AI.
    
    Pipeline: Claude (prompt) → Nano Banana Pro (image) → Grok (video) → FFmpeg (overlay)
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
        
        logger.info(f"VideoGenerator initialized, output: {self.output_dir}")
    
    # ===========================
    # Claude Prompt Generation
    # ===========================
    
    def generate_image_prompt_with_claude(self, style_hint: Optional[str] = None) -> str:
        """
        Use Claude to generate a unique, creative image prompt.
        
        Args:
            style_hint: Optional hint like "beach", "forest", "city"
        
        Returns:
            Creative image prompt for Nano Banana Pro
        """
        if not self.claude_api_key:
            # Fallback to template if no Claude API
            template = random.choice(IMAGE_PROMPT_TEMPLATES)
            if style_hint:
                template = template.replace("nature park", style_hint)
            return f"{template}, motivational aesthetic, 9:16 vertical format, cinematic quality, vibrant colors"
        
        try:
            system_prompt = """You are a creative prompt engineer for AI image generation. Generate short, vivid image prompts for POV walking/exploring videos in beautiful outdoor locations. 

Requirements:
- POV (first person) perspective
- Outdoor scene: nature, beach, city park, forest, etc.
- Motivational/positive vibe
- 9:16 vertical format optimized
- Short but descriptive (1-2 sentences)

Just output the prompt, nothing else."""
            
            user_message = f"Generate a unique POV scene prompt for a teamwork motivation video."
            if style_hint:
                user_message += f" Theme: {style_hint}"
            
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
                    "model": "claude-sonnet-4-20250514",  # Match working Discord bot
                    "max_tokens": 200,
                    "system": system_prompt,
                    "messages": [{"role": "user", "content": user_message}]
                },
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            prompt = result.get("content", [{}])[0].get("text", "").strip()
            
            # Append quality modifiers
            prompt += ", 9:16 vertical format, cinematic quality, vibrant colors, motivational aesthetic"
            
            logger.info(f"Claude generated prompt: {prompt[:100]}...")
            return prompt
            
        except httpx.HTTPStatusError as e:
            logger.warning(f"Claude API HTTP error {e.response.status_code}: {e.response.text[:200]}, using template")
            template = random.choice(IMAGE_PROMPT_TEMPLATES)
            return f"{template}, motivational aesthetic, 9:16 vertical format, cinematic quality"
        except Exception as e:
            logger.warning(f"Claude prompt generation failed: {e}, using template")
            template = random.choice(IMAGE_PROMPT_TEMPLATES)
            return f"{template}, motivational aesthetic, 9:16 vertical format, cinematic quality"
    
    def generate_video_motion_prompt(self) -> str:
        """Generate motion prompt for video conversion."""
        return random.choice(VIDEO_MOTION_PROMPTS)
    
    # ===========================
    # FFmpeg Text Overlay
    # ===========================
    
    def add_text_overlay(
        self,
        input_video_path: str,
        output_video_path: str,
        text: str,
        font_size: int = 72,
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
            # FFmpeg command to strip all metadata
            # -map_metadata -1: Remove all global metadata
            # -fflags +bitexact: Disable encoding metadata
            # -flags:v +bitexact: Disable video stream metadata
            # -flags:a +bitexact: Disable audio stream metadata
            cmd = [
                "ffmpeg", "-y",
                "-i", input_video_path,
                "-map_metadata", "-1",  # Remove all metadata
                "-fflags", "+bitexact",  # No encoder info
                "-flags:v", "+bitexact",  # No video encoder info
                "-flags:a", "+bitexact",  # No audio encoder info
                "-c:v", "libx264",  # Re-encode video
                "-c:a", "aac",  # Re-encode audio
                "-movflags", "+faststart",  # Optimize for streaming
                output_video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            if result.returncode == 0:
                logger.info("Metadata stripped successfully")
                return True
            else:
                logger.error(f"Metadata strip error: {result.stderr}")
                return False
                
        except FileNotFoundError:
            logger.error("FFmpeg not found - metadata strip skipped")
            return False
        except Exception as e:
            logger.error(f"Metadata strip failed: {e}")
            return False
    
    # ===========================
    # Full Pipeline
    # ===========================
    
    def generate_teamwork_video(
        self,
        style_hint: Optional[str] = None,
        text_overlay: Optional[str] = None,
        skip_overlay: bool = False
    ) -> GeneratedVideo:
        """
        Generate a complete teamwork trend video.
        
        Pipeline:
        1. Claude generates creative image prompt
        2. Nano Banana Pro creates 9:16 image
        3. Grok Imagine converts to 10s video
        4. FFmpeg adds text overlay
        
        Args:
            style_hint: Location style hint (beach, forest, city, etc.)
            text_overlay: Custom text, or random from list
            skip_overlay: Skip FFmpeg overlay step
        
        Returns:
            GeneratedVideo with paths and URLs
        """
        cost = 0.0
        
        # 1. Generate image prompt with Claude
        logger.info("Step 1: Generating image prompt...")
        image_prompt = self.generate_image_prompt_with_claude(style_hint)
        
        # 2. Generate image with Nano Banana Pro
        logger.info("Step 2: Generating image with Nano Banana Pro...")
        image_result = self.kie.generate_image(
            prompt=image_prompt,
            aspect_ratio="9:16",
            resolution="1K",
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
        cost += 0.09  # Nano Banana Pro cost
        logger.info(f"Image generated: {image_url}")
        
        # 3. Convert to video with Grok Imagine
        logger.info("Step 3: Converting to video with Grok Imagine...")
        video_prompt = self.generate_video_motion_prompt()
        
        video_result = self.kie.image_to_video(
            image_url=image_url,
            prompt=video_prompt,
            duration="10",
            mode="normal"
        )
        
        if not video_result.success:
            return GeneratedVideo(
                success=False,
                error=f"Video conversion failed: {video_result.error}",
                image_url=image_url,
                prompt_used=image_prompt,
                cost_usd=cost
            )
        
        # Wait for video
        logger.info(f"Waiting for video task {video_result.task_id}...")
        video_final = self.kie.wait_for_task(video_result.task_id, timeout_seconds=300)
        
        if not video_final.success or not video_final.result_urls:
            return GeneratedVideo(
                success=False,
                error=f"Video conversion failed: {video_final.error or 'No result URLs'}",
                image_url=image_url,
                prompt_used=image_prompt,
                cost_usd=cost
            )
        
        video_url = video_final.result_urls[0]
        cost += 0.15  # Grok Imagine cost
        logger.info(f"Video generated: {video_url}")
        
        # 4. Download video
        video_filename = f"teamwork_{int(time.time())}_{random.randint(1000, 9999)}.mp4"
        raw_video_path = self.output_dir / f"raw_{video_filename}"
        final_video_path = self.output_dir / video_filename
        
        try:
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
            # Just copy raw to overlay path (will be processed for metadata)
            overlay_video_path = raw_video_path
        else:
            overlay_success = self.add_text_overlay(
                str(raw_video_path),
                str(overlay_video_path),
                final_text
            )
            
            if overlay_success:
                raw_video_path.unlink(missing_ok=True)  # Delete raw
            else:
                # Fallback: use raw video without overlay
                overlay_video_path = raw_video_path
                logger.warning("Using video without text overlay")
        
        # 6. Strip metadata to remove AI fingerprints
        logger.info("Step 6: Stripping metadata...")
        strip_success = self.strip_metadata(
            str(overlay_video_path),
            str(final_video_path)
        )
        
        if strip_success:
            # Delete intermediate file
            if overlay_video_path != raw_video_path:
                overlay_video_path.unlink(missing_ok=True)
        else:
            # Fallback: use video with metadata
            if overlay_video_path.exists():
                overlay_video_path.rename(final_video_path)
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
        styles = style_hints or ["nature", "beach", "city", "forest", "mountain"]
        results = []
        
        for i in range(count):
            style = styles[i % len(styles)]
            logger.info(f"Generating video {i+1}/{count} (style: {style})...")
            
            result = self.generate_teamwork_video(
                style_hint=style,
                skip_overlay=skip_overlay
            )
            results.append(result)
            
            if result.success:
                logger.info(f"Video {i+1} complete: {result.video_path}")
            else:
                logger.error(f"Video {i+1} failed: {result.error}")
            
            # Small delay between generations
            if i < count - 1:
                time.sleep(2)
        
        return results
    
    # ===========================
    # Caption/Hashtag Helpers
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
