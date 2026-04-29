"""
JesusAI Video Generator
=======================
Generates "Jesus vs Devil" competition videos for TikTok account growth.

Pipeline:
  1. Pick competition (random or specified) + mode (realistic | cartoon)
  2. Nano Banana Pro 2K  -> 9:16 still image of Jesus + Devil competing
  3. Kling 2.6 (default) or Hailuo 2.3 -> animates the still into a 5-6s clip
  4. FFmpeg adds SEO-word "swipe" text overlay (per TAP method)
  5. FFmpeg adds trending sound (user-supplied via assets/sounds/)
  6. FFmpeg strips metadata (removes AI fingerprint)

Cost: ~$0.22/video (Nano Banana Pro 2K $0.12 + Kling 2.6 $0.10).

Requires KIE_API_KEY env var. Falls back to template prompts if ANTHROPIC_API_KEY is absent.
"""

import json
import logging
import os
import random
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from .kie_client import get_kie_client

logger = logging.getLogger(__name__)


# =============================================================================
# Public types & constants
# =============================================================================

@dataclass
class GeneratedVideo:
    success: bool
    video_path: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    competition: Optional[str] = None
    mode: Optional[str] = None
    prompt_used: Optional[str] = None
    text_overlay: Optional[str] = None
    error: Optional[str] = None
    cost_usd: float = 0.0


# Hashtag set — primary JesusAI tags per user direction
HASHTAGS = "#jesus #jesussaves #jesuslovesyou #fyp #foryou #christian"

CAPTIONS = [
    "Follow me, I'll follow back 🙏",
    "F4F let's grow together 🙏",
    "Jesus loves you ❤️",
    "Support to support 🙏",
    "Follow back? 🙏 #jesus",
    "Like for like 🙏 #jesussaves",
    "Drop a 🙏 if you ride with Jesus",
    "Mutuals only 🙏",
    "🙏🙏🙏 #jesuslovesyou",
    "I follow back fast 🙏 #f4f",
]


# SEO words baked into every video as on-screen text (TAP method: "swipe off-screen so hidden")
# Per the PDF: "Use the SEO words below in every video. Put them on screen, then swipe them off
# screen so they're hidden. This helps boost engagement and keeps you away from violations."
SEO_WORDS = [
    "f4f", "follow for follow", "follow back", "fb", "fast", "moots", "mutuals",
    "grow together", "support for support", "like for like", "l4l",
    "engagement boost", "follower growth", "TikTok growth", "gain followers",
    "grow your account", "better together", "squad goals",
    "jesus", "jesus saves", "jesus loves you", "christian content",
    "faith", "blessed", "god is good", "pray for us", "christian growth",
]

# Single overlay phrases that scroll in the video — kept short for readability
TEXT_OVERLAY_LINES = [
    "Follow back 🙏",
    "F4F",
    "Mutuals 🙏",
    "Like for like",
    "Support to support",
    "Follow for follow",
    "Jesus loves you",
    "🙏 mutuals 🙏",
]


# =============================================================================
# Competition catalog (10 Jesus vs Devil scenes per JesusAI handover doc)
# =============================================================================
#
# Schtick: Devil always wins (Jesus losing/struggling). Controversy drives
# comments, duets, shares -> algorithm boost. This is intentional.
#
# Each entry: name, camera, action (motion prompt), and image hint.

COMPETITIONS = [
    {
        "name": "Arm Wrestling",
        "camera": "side-view",
        "action": "Devil pushing Jesus's arm down with effortless smug confidence; Jesus straining hard, sweat on brow, losing ground.",
    },
    {
        "name": "Tug of War",
        "camera": "side-view",
        "action": "Devil pulling thick rope effortlessly; Jesus dug in heels, leaning back, slipping forward, robe whipping in the wind.",
    },
    {
        "name": "Chess",
        "camera": "side-view",
        "action": "Devil smirking confidently with hand on chin over a chess board; Jesus stressed, hand on forehead, frowning at the position.",
    },
    {
        "name": "Jogging",
        "camera": "side-view",
        "action": "Devil running with effortless smooth stride along a track; Jesus several paces behind, panting, sweating, falling behind.",
    },
    {
        "name": "Swimming",
        "camera": "front-facing",
        "action": "Devil cutting through the pool with smooth powerful freestyle stroke; Jesus splashing wildly behind, struggling, head barely above water.",
    },
    {
        "name": "Running",
        "camera": "front-facing",
        "action": "Devil crossing the finish line first with arms raised in triumph; Jesus several meters back, exhausted, hands on knees.",
    },
    {
        "name": "Cycling",
        "camera": "front-facing",
        "action": "Devil pedaling effortlessly on a road bike, leaning into a curve; Jesus panting heavily on a bike trailing behind, legs burning.",
    },
    {
        "name": "Kayak Racing",
        "camera": "front-facing",
        "action": "Devil paddling powerfully with a sleek kayak slicing through whitewater; Jesus splashing, kayak wobbling, falling behind in the rapids.",
    },
    {
        "name": "Horseback Riding",
        "camera": "front-facing",
        "action": "Devil galloping ahead on a powerful black stallion, cape flowing; Jesus on a slower white horse trailing behind, holding on tight.",
    },
    {
        "name": "Rock Climbing",
        "camera": "dynamic",
        "action": "Devil higher on the rock wall, climbing effortlessly with a smug grin; Jesus below, reaching up, struggling to find the next handhold.",
    },
]


# =============================================================================
# JSON prompt builder (Nano Banana Pro)
# =============================================================================
#
# Uses the master JSON schema from the JESUSAI-HANDOVER ultra-realism guide.
# Pretty-printed JSON improves the model's attention to each field.

GLOBAL_REALISM = "Photorealistic. Shot on a smartphone. Real product footage."


def build_jesusai_image_prompt(competition: dict, mode: str = "realistic") -> str:
    """
    Build a JSON-string prompt for Nano Banana Pro for a Jesus vs Devil scene.

    Args:
        competition: One of COMPETITIONS entries
        mode: "realistic" (default) or "cartoon"

    Returns:
        JSON-formatted string ready to pass as the `prompt` field.
    """
    is_cartoon = mode == "cartoon"

    # Subject — both characters specified, camera angle from competition
    subject = {
        "description": (
            f"Jesus and the Devil competing in {competition['name'].lower()}. "
            f"{competition['action']} "
            "Both figures clearly visible in frame."
        ),
        "jesus": (
            "Jesus Christ — long brown hair, full beard, white robe with red sash, "
            "kind-but-stressed expression, glowing soft halo aura"
        ),
        "devil": (
            "The Devil — red skin, two black horns, sharp goatee, smug confident grin, "
            "black cloak, slight smoke wisps around him"
        ),
        "arrangement": "Jesus on the left, Devil on the right, both fully in frame",
        "camera_angle": competition["camera"],
    }

    # Scene matched to the competition
    scene = {
        "environment": _scene_for(competition["name"]),
        "depth": "natural depth of field, focus on the action between the two figures",
        "environment_feel": "real, grounded, not a sterile studio set",
    }

    if is_cartoon:
        image_type = "vibrant cartoon illustration, bold lines, expressive faces"
        style = "Pixar-style 3D animated cartoon, exaggerated expressions"
        realism = {
            "overall": "stylized 3D cartoon — clean, expressive, family-friendly",
            "textures": "smooth painted surfaces with cartoon shading",
            "color_science": "vibrant saturated colors, slightly exaggerated",
        }
        negative = [
            "photorealistic", "uncanny valley", "scary", "grotesque",
            "garbled text", "warped faces",
        ]
    else:
        image_type = "ultra-realistic cinematic photograph"
        style = "photojournalism, candid, lifelike, editorial-but-real"
        realism = {
            "overall": GLOBAL_REALISM,
            "textures": "natural skin texture with pores, real hair, fabric weave on robes",
            "imperfections": "tiny dust particles in light, real human imperfections — NOT artificially perfect",
            "color_science": "accurate white balance, warm natural tones",
        }
        negative = [
            "studio backdrop", "white seamless background", "professional product photography",
            "flat lighting", "harsh shadows", "blown highlights", "oversaturated colors",
            "AI-generated look", "uncanny valley", "plastic skin", "garbled text",
            "warped faces", "extra fingers", "melted hands",
        ]

    prompt_obj = {
        "image_type": image_type,
        "subject": subject,
        "scene": scene,
        "lighting": {
            "type": "natural ambient light matched to the scene",
            "quality": "soft, dramatic, cinematic",
            "shadows": "natural soft shadows where bodies meet ground",
        },
        "composition": {
            "framing": "9:16 vertical TikTok frame, both figures fully visible",
            "rule_of_thirds": "Jesus left third, Devil right third, action in center",
            "focus": "tack-sharp on both figures, environment naturally soft",
        },
        "camera": {
            "device": "shot on iPhone 15 Pro Max" if not is_cartoon else "rendered cinematic camera",
            "lens": "natural 1x lens, no fisheye",
            "angle": competition["camera"],
            "aspect_ratio": "9:16 vertical (TikTok native)",
        },
        "realism": realism,
        "style": style,
        "negative_prompt": negative,
        "post_processing": "no filters, clean output",
    }

    return json.dumps(prompt_obj, indent=2)


def _scene_for(competition_name: str) -> str:
    """Pick an environment that fits the competition."""
    mapping = {
        "Arm Wrestling": "rustic wooden table in a softly-lit tavern interior",
        "Tug of War": "open grassy field at golden hour with mountains in distance",
        "Chess": "ornate marble chess table by a window, stained-glass light",
        "Jogging": "outdoor running track at dawn, soft morning fog",
        "Swimming": "Olympic swimming pool with crystal blue water, lane markers visible",
        "Running": "outdoor sprint track with finish-line tape, stadium in soft background",
        "Cycling": "winding asphalt road through countryside, golden hour",
        "Kayak Racing": "whitewater rapids with churning blue-white water, forested banks",
        "Horseback Riding": "open prairie with golden grass, dramatic cloudy sky",
        "Rock Climbing": "tall rocky cliff face with handholds, sunset sky behind",
    }
    return mapping.get(competition_name, "dramatic outdoor setting")


def build_jesusai_motion_prompt(competition: dict) -> str:
    """Build the Kling/Hailuo motion prompt for the animation pass."""
    return (
        f"Animate this scene: {competition['action']} "
        "Smooth realistic motion at 30fps, 5-second duration. "
        "Camera holds steady — let the subjects' action drive the shot. "
        "Maintain both characters' identity, costume, and proportions throughout."
    )


# =============================================================================
# VideoGenerator — main pipeline
# =============================================================================

class VideoGenerator:
    """
    JesusAI video generator.

    Pipeline:
      Nano Banana Pro 2K (image) -> Kling 2.6 (video) -> FFmpeg overlay/sound/strip

    Backwards-compatible: exposes generate_teamwork_video() as an alias to
    generate_jesusai_video() so older callers keep working during transition.
    """

    DEFAULT_VIDEO_MODEL = os.getenv("JESUSAI_VIDEO_MODEL", "kling")  # "kling" | "hailuo"

    def __init__(self, output_dir: Optional[str] = None):
        self.kie = get_kie_client()

        raw_anthropic = os.getenv("ANTHROPIC_API_KEY", "")
        self.anthropic_api_key = raw_anthropic.strip() if raw_anthropic else None

        default_dir = "/var/data/generated_videos" if os.path.isdir("/var/data") else "./generated_videos"
        self.output_dir = Path(output_dir or os.getenv("VIDEO_OUTPUT_DIR", default_dir))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.sounds_dir = Path(__file__).parent.parent.parent / "assets" / "sounds"
        self.trending_sounds_dir = self.sounds_dir / "trending"
        self.trending_sounds_dir.mkdir(parents=True, exist_ok=True)

        self._used_competitions: set = set()

        logger.info(
            f"JesusAI VideoGenerator initialized — video model: {self.DEFAULT_VIDEO_MODEL}, "
            f"output: {self.output_dir}"
        )

    # -------------------------------------------------------------------------
    # Pick / build prompt
    # -------------------------------------------------------------------------

    def pick_competition(self, requested: Optional[str] = None) -> dict:
        """Pick a competition by name match (substring) or random not-recently-used."""
        if requested:
            req_lower = requested.lower()
            for comp in COMPETITIONS:
                if req_lower in comp["name"].lower():
                    return comp

        available_idx = [i for i in range(len(COMPETITIONS)) if i not in self._used_competitions]
        if not available_idx:
            self._used_competitions.clear()
            available_idx = list(range(len(COMPETITIONS)))

        idx = random.choice(available_idx)
        self._used_competitions.add(idx)
        return COMPETITIONS[idx]

    # -------------------------------------------------------------------------
    # FFmpeg helpers (kept from prior pipeline — proven, no JesusAI coupling)
    # -------------------------------------------------------------------------

    def add_text_overlay(
        self,
        input_video_path: str,
        output_video_path: str,
        text_line: str,
        repeat_count: int = 8,
        font_size: int = 42,
        font_color: str = "white",
        border_color: str = "black",
        border_width: int = 3,
    ) -> bool:
        """
        Add stacked text overlay to a video. Per TAP method: SEO words on screen,
        then swiped off — but at this stage we just stamp them; the "swipe" is
        the natural reading flow of the stacked column.
        """
        try:
            line_height = font_size + 12
            total_height = repeat_count * line_height
            start_y = f"(h-{total_height})/2"

            safe_text = text_line.replace("'", r"'\''")

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

            cmd = [
                "ffmpeg", "-y",
                "-i", input_video_path,
                "-vf", ",".join(filters),
                "-c:v", "libx264",
                "-preset", "fast",
                "-codec:a", "copy",
                output_video_path,
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                logger.info(f"Text overlay added: '{text_line}' x{repeat_count}")
                return True
            logger.error(f"FFmpeg overlay error: {result.stderr[:300]}")
            return False
        except FileNotFoundError:
            logger.error("FFmpeg not found — overlay skipped")
            return False
        except Exception as e:
            logger.error(f"Text overlay failed: {e}")
            return False

    def strip_metadata(self, input_video_path: str, output_video_path: str) -> bool:
        try:
            cmd = [
                "ffmpeg", "-y",
                "-i", input_video_path,
                "-map_metadata", "-1",
                "-fflags", "+bitexact",
                "-flags:v", "+bitexact",
                "-flags:a", "+bitexact",
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "128k",
                output_video_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            if result.returncode == 0:
                logger.info("Metadata stripped")
                return True
            logger.error(f"Metadata strip error: {result.stderr[:300]}")
            return False
        except FileNotFoundError:
            logger.error("FFmpeg not found — metadata not stripped")
            return False
        except Exception as e:
            logger.error(f"Metadata strip failed: {e}")
            return False

    def get_random_trending_sound(self) -> Optional[Path]:
        """Pick a random local sound file from assets/sounds/. User-supplied."""
        sound_files: List[Path] = []
        for ext in ("*.mp3", "*.wav", "*.m4a", "*.ogg"):
            sound_files.extend(self.sounds_dir.rglob(ext))
        sound_files = [f for f in sound_files if f.suffix in (".mp3", ".wav", ".m4a", ".ogg")]

        if not sound_files:
            logger.warning("No sound files in assets/sounds/ — video will have no audio")
            return None

        chosen = random.choice(sound_files)
        logger.info(f"Using sound: {chosen.name} ({len(sound_files)} available)")
        return chosen

    def add_sound_to_video(
        self,
        input_video_path: str,
        output_video_path: str,
        sound_path: Optional[str] = None,
    ) -> bool:
        try:
            if sound_path is None:
                sound_file = self.get_random_trending_sound()
                if sound_file is None:
                    import shutil
                    shutil.copy(input_video_path, output_video_path)
                    return True
                sound_path = str(sound_file)

            sound_path_obj = Path(sound_path)
            if not sound_path_obj.exists():
                logger.warning(f"Sound file not found: {sound_path} — copying without audio")
                import shutil
                shutil.copy(input_video_path, output_video_path)
                return True

            cmd = [
                "ffmpeg", "-y",
                "-i", input_video_path,
                "-i", str(sound_path_obj),
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                "-map", "0:v:0",
                "-map", "1:a:0",
                output_video_path,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                logger.info(f"Sound added: {sound_path_obj.name}")
                return True
            logger.error(f"FFmpeg audio mux error: {result.stderr[:300]}")
            import shutil
            shutil.copy(input_video_path, output_video_path)
            return False
        except FileNotFoundError:
            logger.error("FFmpeg not found — sound not added")
            return False
        except Exception as e:
            logger.error(f"Sound addition failed: {e}")
            return False

    # -------------------------------------------------------------------------
    # Main pipeline
    # -------------------------------------------------------------------------

    def generate_jesusai_video(
        self,
        competition: Optional[str] = None,
        mode: str = "realistic",
        text_overlay: Optional[str] = None,
        skip_overlay: bool = False,
        image_url: Optional[str] = None,
        sound_path: Optional[str] = None,
    ) -> GeneratedVideo:
        """
        Generate a single JesusAI video.

        Args:
            competition: Name match (e.g. "chess") or None for random
            mode: "realistic" or "cartoon"
            text_overlay: Custom overlay line, or None for random from TEXT_OVERLAY_LINES
            skip_overlay: Skip the FFmpeg overlay step
            image_url: Pre-existing image URL (skips Nano Banana stage — for image reuse)
            sound_path: Specific sound file (or None for random from assets/sounds/)
        """
        cost = 0.0
        comp = self.pick_competition(competition)
        logger.info(f"JesusAI: {comp['name']} ({mode})")

        # 1. IMAGE — Nano Banana Pro 2K (skip if reusing)
        prompt_str = None
        if image_url:
            logger.info(f"Reusing image: {image_url[:80]}...")
        else:
            prompt_str = build_jesusai_image_prompt(comp, mode=mode)
            logger.info("Generating image with Nano Banana Pro 2K...")
            image_result = self.kie.generate_image(
                prompt=prompt_str,
                aspect_ratio="9:16",
                resolution="2K",
                output_format="png",
            )
            if not image_result.success or not image_result.task_id:
                return GeneratedVideo(
                    success=False,
                    competition=comp["name"],
                    mode=mode,
                    error=f"Image submit failed: {image_result.error}",
                    prompt_used=prompt_str,
                )

            wait = self.kie.wait_for_task(image_result.task_id, timeout_seconds=180, poll_interval=5)
            if not wait.success or not wait.result_urls:
                return GeneratedVideo(
                    success=False,
                    competition=comp["name"],
                    mode=mode,
                    error=f"Image generation failed: {wait.error or wait.state}",
                    prompt_used=prompt_str,
                )
            image_url = wait.result_urls[0]
            cost += 0.12  # Nano Banana Pro 2K
            logger.info(f"Image ready: {image_url[:80]}...")

        # 2. VIDEO — Kling 2.6 (default) or Hailuo 2.3
        motion_prompt = build_jesusai_motion_prompt(comp)
        logger.info(f"Animating with {self.DEFAULT_VIDEO_MODEL}...")

        if self.DEFAULT_VIDEO_MODEL == "kling":
            video_result = self.kie.image_to_video_kling(
                image_url=image_url,
                prompt=motion_prompt,
                duration="5",
                aspect_ratio="9:16",
            )
            video_cost = 0.10
        else:
            video_result = self.kie.image_to_video_hailuo(
                image_url=image_url,
                prompt=motion_prompt,
                duration="6",
                resolution="768P",
            )
            video_cost = 0.15

        if not video_result.success or not video_result.task_id:
            return GeneratedVideo(
                success=False,
                competition=comp["name"],
                mode=mode,
                image_url=image_url,
                error=f"Video submit failed: {video_result.error}",
                prompt_used=prompt_str,
                cost_usd=cost,
            )

        video_wait = self.kie.wait_for_task(video_result.task_id, timeout_seconds=420, poll_interval=8)
        if not video_wait.success or not video_wait.result_urls:
            return GeneratedVideo(
                success=False,
                competition=comp["name"],
                mode=mode,
                image_url=image_url,
                error=f"Video generation failed: {video_wait.error or video_wait.state}",
                prompt_used=prompt_str,
                cost_usd=cost,
            )

        cost += video_cost
        video_url = video_wait.result_urls[0]
        logger.info(f"Video ready: {video_url[:80]}...")

        # 3. Download
        video_filename = f"jesusai_{int(time.time())}_{random.randint(1000, 9999)}.mp4"
        raw_path = self.output_dir / f"raw_{video_filename}"
        final_path = self.output_dir / video_filename

        try:
            import httpx
            with httpx.Client(timeout=120) as client:
                resp = client.get(video_url)
                resp.raise_for_status()
                raw_path.write_bytes(resp.content)
        except Exception as e:
            return GeneratedVideo(
                success=False,
                competition=comp["name"],
                mode=mode,
                image_url=image_url,
                video_url=video_url,
                error=f"Video download failed: {e}",
                prompt_used=prompt_str,
                cost_usd=cost,
            )

        # 4. FFmpeg post-process: overlay -> sound -> strip metadata
        current_path = raw_path
        chosen_overlay = text_overlay or random.choice(TEXT_OVERLAY_LINES)

        if not skip_overlay:
            overlay_path = self.output_dir / f"overlay_{video_filename}"
            if self.add_text_overlay(str(current_path), str(overlay_path), chosen_overlay):
                current_path.unlink(missing_ok=True)
                current_path = overlay_path

        sound_out = self.output_dir / f"sound_{video_filename}"
        if self.add_sound_to_video(str(current_path), str(sound_out), sound_path=sound_path):
            if current_path != raw_path:
                current_path.unlink(missing_ok=True)
            current_path = sound_out

        if not self.strip_metadata(str(current_path), str(final_path)):
            # If strip failed, just rename current -> final
            if current_path.exists():
                current_path.rename(final_path)
        else:
            if current_path != raw_path and current_path.exists():
                current_path.unlink(missing_ok=True)

        if not final_path.exists():
            return GeneratedVideo(
                success=False,
                competition=comp["name"],
                mode=mode,
                image_url=image_url,
                video_url=video_url,
                error="Final video missing after post-process",
                prompt_used=prompt_str,
                cost_usd=cost,
            )

        return GeneratedVideo(
            success=True,
            video_path=str(final_path),
            image_url=image_url,
            video_url=video_url,
            competition=comp["name"],
            mode=mode,
            prompt_used=prompt_str,
            text_overlay=chosen_overlay,
            cost_usd=cost,
        )

    # -------------------------------------------------------------------------
    # Batch helpers
    # -------------------------------------------------------------------------

    def generate_batch(
        self,
        count: int = 1,
        mode: str = "realistic",
    ) -> List[GeneratedVideo]:
        """Generate `count` videos with random competitions."""
        results: List[GeneratedVideo] = []
        for i in range(count):
            logger.info(f"Batch progress: {i + 1}/{count}")
            results.append(self.generate_jesusai_video(mode=mode))
        return results

    def generate_batch_for_account(
        self,
        count: int = 1,
        mode: str = "realistic",
    ) -> List[GeneratedVideo]:
        """
        Generate `count` videos for an account.

        Reuses the same base image across the batch by generating one image then
        animating it `count` times with different motion seeds. Cuts cost from
        $0.22*N to $0.12 + $0.10*N (image generated once).
        """
        if count <= 0:
            return []

        comp = self.pick_competition()
        # First video — generates the image
        first = self.generate_jesusai_video(competition=comp["name"], mode=mode)
        results: List[GeneratedVideo] = [first]

        if not first.success or not first.image_url:
            # Image gen failed; fall back to independent generations for the rest
            for _ in range(count - 1):
                results.append(self.generate_jesusai_video(mode=mode))
            return results

        # Reuse image for remaining videos
        for i in range(count - 1):
            logger.info(f"Reusing base image for video {i + 2}/{count}...")
            results.append(
                self.generate_jesusai_video(
                    competition=comp["name"],
                    mode=mode,
                    image_url=first.image_url,
                )
            )
        return results

    # -------------------------------------------------------------------------
    # Caption helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def get_random_caption() -> str:
        return random.choice(CAPTIONS)

    @staticmethod
    def get_hashtags() -> str:
        return HASHTAGS

    @staticmethod
    def get_full_description() -> str:
        return f"{random.choice(CAPTIONS)} {HASHTAGS}"

    # -------------------------------------------------------------------------
    # Backwards-compat aliases (so legacy callers don't break)
    # -------------------------------------------------------------------------

    def generate_teamwork_video(self, *args, **kwargs) -> GeneratedVideo:
        """Deprecated alias — content is now JesusAI. Forwards to generate_jesusai_video."""
        # Strip kwargs that don't apply
        kwargs.pop("style_hint", None)
        return self.generate_jesusai_video(*args, **kwargs)


# =============================================================================
# Singleton
# =============================================================================

_video_generator: Optional[VideoGenerator] = None


def get_video_generator() -> VideoGenerator:
    global _video_generator
    if _video_generator is None:
        _video_generator = VideoGenerator()
    return _video_generator
