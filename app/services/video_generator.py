"""
Teamwork Trend Video Generator v4.0

Full pipeline:
1. JSON-structured prompt → Nano Banana Pro 1K creates ultra-realistic 9:16 image
2. Hailuo 2.3 Standard converts to 6s 768P video
3. FFmpeg adds centered text overlay
4. FFmpeg adds random trending sound/music
5. FFmpeg strips metadata (removes AI fingerprints)

Image reuse: 1 base image → 3 videos per account via varied motion prompts.
Cost: ~$0.18/video avg (was $0.26).
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

# Ultra-realistic JSON prompt templates for Nano Banana Pro
# Each scene is POV walking through nature/city — structured for maximum photorealism
JSON_PROMPT_TEMPLATES = [
    # 1. Beach golden hour
    {
        "meta": {
            "quality": "ultra photorealistic",
            "resolution": "8k",
            "camera": "Sony A7IV",
            "lens": "35mm prime",
            "aspect_ratio": "9:16",
            "style": "golden hour natural light, DSLR realism, Kodak Portra 400 film look"
        },
        "scene": {
            "concept": "first-person POV walking along a pristine sandy beach at golden hour",
            "location": "wide sandy beach with gentle waves",
            "time": "golden hour, 30 minutes before sunset"
        },
        "environment": {
            "foreground": ["wet sand with gentle footprint impressions", "foam from receding waves"],
            "midground": ["a jogger running along the waterline in the distance", "seagulls scattered on the sand"],
            "background": ["warm orange-pink sunset over the ocean horizon", "distant headland silhouette"],
            "atmosphere": "salt air haze, warm golden light wrapping around everything"
        },
        "camera": {
            "shot_type": "first-person POV looking forward at the horizon",
            "aperture": "f/2.8",
            "depth_of_field": "shallow, background softly blurred",
            "perspective": "natural walking height, eye level"
        },
        "lighting": {
            "type": "golden hour natural sunlight",
            "direction": "low angle side-backlighting from the left",
            "quality": "warm, soft, with gentle lens flare",
            "shadows": "long and soft on the sand"
        },
        "colors_and_tone": {
            "palette": "warm golden sand, coral sunset sky, turquoise water, natural skin tones",
            "contrast": "medium, film-like",
            "saturation": "natural, slightly warm"
        },
        "quality_and_technical_details": {
            "resolution": "masterpiece, extremely detailed",
            "texture_focus": "sand grains, water surface, natural light scatter",
            "noise": "subtle ISO grain consistent with golden hour photography"
        },
        "negative_prompt": {
            "forbidden_concepts": ["cartoon", "illustration", "3d render", "plastic skin", "oversaturated", "HDR", "feet visible", "legs visible", "selfie", "wide angle distortion"]
        }
    },
    # 2. Forest trail
    {
        "meta": {
            "quality": "ultra photorealistic",
            "resolution": "8k",
            "camera": "Canon R5",
            "lens": "35mm f/1.8",
            "aspect_ratio": "9:16",
            "style": "volumetric forest light, natural film grain, cinematic depth"
        },
        "scene": {
            "concept": "first-person POV peaceful walk through a lush forest trail",
            "location": "dense green forest with tall pines and ferns",
            "time": "late morning, dappled sunlight"
        },
        "environment": {
            "foreground": ["dirt path with exposed tree roots", "fern fronds at the edges"],
            "midground": ["a hiker with backpack walking ahead on the trail", "fallen moss-covered log"],
            "background": ["towering pine trees creating a natural canopy", "volumetric light rays filtering through branches"],
            "atmosphere": "misty morning air, earthy smell, peaceful silence"
        },
        "camera": {
            "shot_type": "first-person POV looking forward down the trail",
            "aperture": "f/2.8",
            "depth_of_field": "shallow with creamy bokeh background",
            "perspective": "natural walking eye level"
        },
        "lighting": {
            "type": "dappled forest sunlight, volumetric rays",
            "direction": "overhead filtered through canopy, backlighting the path",
            "quality": "soft with dramatic god rays",
            "shadows": "complex dappled patterns on the forest floor"
        },
        "colors_and_tone": {
            "palette": "rich earthy greens, warm brown bark, golden light shafts, cool shadow tones",
            "contrast": "high in light shafts, soft in shadows",
            "saturation": "natural with lush greens"
        },
        "quality_and_technical_details": {
            "resolution": "masterpiece, extremely detailed",
            "texture_focus": "bark texture, moss detail, leaf veins, dirt path",
            "noise": "subtle natural grain"
        },
        "negative_prompt": {
            "forbidden_concepts": ["cartoon", "illustration", "3d render", "oversaturated", "feet visible", "legs visible", "wide angle distortion"]
        }
    },
    # 3. City park autumn
    {
        "meta": {
            "quality": "ultra photorealistic",
            "resolution": "8k",
            "camera": "Sony A7IV",
            "lens": "50mm prime",
            "aspect_ratio": "9:16",
            "style": "autumn warmth, soft backlight, cinematic color grading"
        },
        "scene": {
            "concept": "first-person POV leisurely stroll through a city park in peak autumn",
            "location": "urban park lined with mature maple and oak trees",
            "time": "late afternoon, warm autumn light"
        },
        "environment": {
            "foreground": ["cobblestone walking path covered in fallen golden leaves"],
            "midground": ["a couple walking their golden retriever ahead", "park bench with someone reading"],
            "background": ["row of trees with fiery orange-red canopy", "soft city skyline visible through branches"],
            "atmosphere": "crisp autumn air, golden leaves gently falling, warm afternoon glow"
        },
        "camera": {
            "shot_type": "first-person POV walking forward through the park",
            "aperture": "f/2.0",
            "depth_of_field": "shallow, people and trees softly blurred",
            "perspective": "natural eye level"
        },
        "lighting": {
            "type": "warm autumn afternoon sunlight",
            "direction": "low-angle backlighting through the trees",
            "quality": "soft golden, with gentle lens flare through leaves",
            "shadows": "long and warm on the path"
        },
        "colors_and_tone": {
            "palette": "golden amber, burnt orange, russet red, warm brown, soft green",
            "contrast": "medium-warm",
            "saturation": "rich but natural autumn tones"
        },
        "quality_and_technical_details": {
            "resolution": "masterpiece, extremely detailed",
            "texture_focus": "individual leaf detail, cobblestone texture, bark patterns",
            "noise": "subtle film grain, Kodak Portra warmth"
        },
        "negative_prompt": {
            "forbidden_concepts": ["cartoon", "illustration", "3d render", "oversaturated", "feet visible", "legs visible", "wide angle distortion"]
        }
    },
    # 4. European cobblestone street
    {
        "meta": {
            "quality": "ultra photorealistic",
            "resolution": "8k",
            "camera": "Fujifilm X-T5",
            "lens": "23mm f/2.0",
            "aspect_ratio": "9:16",
            "style": "European travel photography, warm ambient lighting, film grain"
        },
        "scene": {
            "concept": "first-person POV evening walk through a charming European cobblestone street",
            "location": "narrow old-town street in southern Europe with stone buildings",
            "time": "blue hour, just after sunset"
        },
        "environment": {
            "foreground": ["worn cobblestone street glistening slightly from recent rain"],
            "midground": ["warm outdoor café tables with candles", "locals chatting at a small bistro"],
            "background": ["old stone buildings with colorful shutters", "warm string lights draped between buildings", "church bell tower silhouetted against blue-purple sky"],
            "atmosphere": "romantic evening ambiance, warm café glow against cool twilight sky"
        },
        "camera": {
            "shot_type": "first-person POV walking forward down the narrow street",
            "aperture": "f/2.0",
            "depth_of_field": "medium, string lights creating beautiful bokeh",
            "perspective": "natural walking height"
        },
        "lighting": {
            "type": "mixed warm café light and cool twilight",
            "direction": "warm point-source lights from cafés and string lights",
            "quality": "cozy warm interior glow contrasting with blue hour sky",
            "shadows": "soft deep shadows in doorways and alleys"
        },
        "colors_and_tone": {
            "palette": "warm amber from lights, cool blue-purple sky, stone beige, terracotta",
            "contrast": "medium-high for drama",
            "saturation": "rich but natural"
        },
        "quality_and_technical_details": {
            "resolution": "masterpiece, extremely detailed",
            "texture_focus": "wet cobblestone reflections, stone wall texture, candlelight flicker",
            "noise": "moderate film grain consistent with low-light shooting"
        },
        "negative_prompt": {
            "forbidden_concepts": ["cartoon", "illustration", "3d render", "oversaturated", "feet visible", "legs visible", "wide angle distortion", "neon signs"]
        }
    },
    # 5. Mountain trail sunrise
    {
        "meta": {
            "quality": "ultra photorealistic",
            "resolution": "8k",
            "camera": "Nikon Z8",
            "lens": "24mm f/2.8",
            "aspect_ratio": "9:16",
            "style": "epic mountain landscape, sunrise drama, DSLR quality"
        },
        "scene": {
            "concept": "first-person POV hiking a mountain trail at sunrise with breathtaking valley views",
            "location": "alpine mountain trail with panoramic valley overlook",
            "time": "sunrise, first golden light hitting the peaks"
        },
        "environment": {
            "foreground": ["rocky dirt trail with alpine wildflowers at the edges"],
            "midground": ["two hikers resting on a rocky outcrop ahead looking at the view"],
            "background": ["misty valley below with layers of mountains fading into the distance", "warm golden sunrise light on the peaks"],
            "atmosphere": "crisp mountain air, morning mist in the valley, epic scale"
        },
        "camera": {
            "shot_type": "first-person POV looking forward along the trail toward the vista",
            "aperture": "f/5.6",
            "depth_of_field": "deep, landscape sharp from mid to background",
            "perspective": "slightly elevated trail perspective"
        },
        "lighting": {
            "type": "sunrise golden light",
            "direction": "low angle from the right, raking across the mountains",
            "quality": "warm dramatic with orange-golden tones",
            "shadows": "deep valley shadows contrasting with lit peaks"
        },
        "colors_and_tone": {
            "palette": "golden sunrise orange, deep blue shadows, green alpine meadow, misty grey valleys",
            "contrast": "high dramatic",
            "saturation": "vibrant but natural sunrise colors"
        },
        "quality_and_technical_details": {
            "resolution": "masterpiece, extremely detailed",
            "texture_focus": "rock surface, wildflower petals, distant mountain ridgelines",
            "noise": "very subtle, clean landscape photography"
        },
        "negative_prompt": {
            "forbidden_concepts": ["cartoon", "illustration", "3d render", "oversaturated", "feet visible", "legs visible", "selfie"]
        }
    },
    # 6. Japanese garden
    {
        "meta": {
            "quality": "ultra photorealistic",
            "resolution": "8k",
            "camera": "Sony A7C II",
            "lens": "40mm f/2.5",
            "aspect_ratio": "9:16",
            "style": "serene zen atmosphere, soft morning light, natural tones"
        },
        "scene": {
            "concept": "first-person POV gentle walk through a traditional Japanese garden",
            "location": "manicured Japanese zen garden with stone paths and bamboo",
            "time": "early morning, soft diffused light with subtle mist"
        },
        "environment": {
            "foreground": ["stepping stones on raked white gravel", "manicured moss borders"],
            "midground": ["arched wooden bridge over koi pond", "elderly couple admiring maple tree"],
            "background": ["bamboo grove swaying gently", "traditional wooden pagoda partially visible"],
            "atmosphere": "tranquil, meditative, morning dew on leaves, subtle fog"
        },
        "camera": {
            "shot_type": "first-person POV looking forward along the garden path",
            "aperture": "f/2.5",
            "depth_of_field": "shallow, beautiful background separation",
            "perspective": "natural walking height, slightly contemplative downward angle"
        },
        "lighting": {
            "type": "soft diffused morning light with mist",
            "direction": "ambient overhead with slight backlight through bamboo",
            "quality": "ethereal, soft, zen-like",
            "shadows": "gentle and soft everywhere"
        },
        "colors_and_tone": {
            "palette": "jade green moss, white gravel, dark wood brown, soft pink blossoms, grey stone",
            "contrast": "low-medium, peaceful",
            "saturation": "muted and natural, wabi-sabi aesthetic"
        },
        "quality_and_technical_details": {
            "resolution": "masterpiece, extremely detailed",
            "texture_focus": "raked gravel patterns, moss texture, wood grain, water reflections",
            "noise": "very subtle, clean"
        },
        "negative_prompt": {
            "forbidden_concepts": ["cartoon", "illustration", "3d render", "oversaturated", "feet visible", "legs visible", "cherry blossom overload"]
        }
    },
    # 7. Riverside sunset
    {
        "meta": {
            "quality": "ultra photorealistic",
            "resolution": "8k",
            "camera": "Canon R6 II",
            "lens": "35mm f/1.4",
            "aspect_ratio": "9:16",
            "style": "golden reflections, warm evening, natural film aesthetic"
        },
        "scene": {
            "concept": "first-person POV calm walk along a quiet riverside path at sunset",
            "location": "tree-lined river path with a wide peaceful river",
            "time": "sunset, warm golden light reflecting off the water"
        },
        "environment": {
            "foreground": ["gravel walking path with tall grass and wildflowers at the edges"],
            "midground": ["fisherman sitting on the far bank", "wooden dock with a small rowboat"],
            "background": ["golden sunset reflecting on the river surface", "willow trees draping into the water"],
            "atmosphere": "peaceful end of day, warm breeze, birdsong"
        },
        "camera": {
            "shot_type": "first-person POV looking forward along the river path",
            "aperture": "f/2.0",
            "depth_of_field": "shallow, river and trees beautifully blurred",
            "perspective": "natural walking eye level"
        },
        "lighting": {
            "type": "warm sunset light",
            "direction": "low angle from ahead, golden backlight",
            "quality": "rich warm golden with subtle lens flare",
            "shadows": "long and warm stretching toward camera"
        },
        "colors_and_tone": {
            "palette": "molten gold water reflections, warm green foliage, soft pink sky, earthy path",
            "contrast": "medium, warm tones dominant",
            "saturation": "rich golden but natural"
        },
        "quality_and_technical_details": {
            "resolution": "masterpiece, extremely detailed",
            "texture_focus": "water ripple reflections, grass detail, gravel texture",
            "noise": "subtle warm film grain"
        },
        "negative_prompt": {
            "forbidden_concepts": ["cartoon", "illustration", "3d render", "oversaturated", "feet visible", "legs visible"]
        }
    },
    # 8. Tropical path
    {
        "meta": {
            "quality": "ultra photorealistic",
            "resolution": "8k",
            "camera": "iPhone 15 Pro Max",
            "lens": "24mm wide",
            "aspect_ratio": "9:16",
            "style": "tropical paradise, vivid natural colors, iPhone realism"
        },
        "scene": {
            "concept": "first-person POV walking through a lush tropical jungle path toward the ocean",
            "location": "tropical island path with palm trees and exotic vegetation",
            "time": "mid-morning, bright dappled tropical light"
        },
        "environment": {
            "foreground": ["sandy wooden boardwalk path through dense tropical plants"],
            "midground": ["palm fronds arching over the path", "bright tropical flowers"],
            "background": ["glimpse of turquoise ocean through the vegetation", "bright blue sky with white clouds"],
            "atmosphere": "humid tropical air, bright vibrant colors, paradise feeling"
        },
        "camera": {
            "shot_type": "first-person POV walking forward toward the ocean",
            "aperture": "f/1.8",
            "depth_of_field": "shallow, tropical plants creating natural frame",
            "perspective": "natural walking height"
        },
        "lighting": {
            "type": "bright tropical sunlight filtered through canopy",
            "direction": "overhead with dappled patterns",
            "quality": "bright and vivid with natural shadows",
            "shadows": "sharp dappled leaf shadows on the boardwalk"
        },
        "colors_and_tone": {
            "palette": "vivid tropical green, turquoise ocean, white sand, bright flower colors",
            "contrast": "high, vivid tropical",
            "saturation": "vibrant but natural tropical vibrancy"
        },
        "quality_and_technical_details": {
            "resolution": "masterpiece, extremely detailed",
            "texture_focus": "palm bark, tropical leaf veins, wooden boardwalk grain",
            "noise": "minimal, clean bright photography"
        },
        "negative_prompt": {
            "forbidden_concepts": ["cartoon", "illustration", "3d render", "oversaturated", "feet visible", "legs visible", "tourists"]
        }
    },
]

# Simple text fallback templates (used when Claude is unavailable)
IMAGE_PROMPT_TEMPLATES = [
    "Photorealistic POV walking through a sun-dappled city park, golden afternoon light filtering through cherry blossom trees, a couple walking their dog in the distance, shallow depth of field, warm tones, cinematic",
    "Hyper-realistic POV stroll along a pristine sandy beach at golden hour, soft warm sunlight with lens flare, a jogger running far ahead on the shoreline, gentle ocean waves, natural film grain",
    "Ultra-realistic POV peaceful walk through a lush forest trail, volumetric light rays through tall pine trees, a hiker with a backpack visible far ahead, rich earthy greens, shallow depth of field",
    "Photorealistic POV relaxed stroll through autumn woods, golden maple leaves falling, a person walking their golden retriever far ahead on the trail, warm soft backlight, natural film grain",
]

# Text overlays for videos — Loom-style multi-line format
# Each entry is repeated 8x in a vertical column covering the screen
TEXT_OVERLAY_LINES = [
    "Moot me",
    "Teamwork trend",
    "Moot me up",
    "Teamwork ifb",
]

# Captions for TikTok posts — teamwork hashtags
CAPTIONS = [
    "#teamwork #teamworktrend #teamworkchallenge #teamwork1minago #teamwork1hourago",
    "#teamwork #teamworktrend #teamworkchallenge #fyp",
    "#teamwork #teamworkchallenge #teamwork1minago #teamwork1hourago",
    "#teamworktrend #teamworkchallenge #teamwork #fyp",
]

# Hashtags — teamwork format
HASHTAGS = "#teamwork #teamworktrend #teamworkchallenge #teamwork1minago #teamwork1hourago"

# Varied motion prompts for Hailuo 2.3 — each creates a DIFFERENT video from the same base image
# Using diverse walking styles, camera movements, and environmental interactions
HAILUO_MOTION_PROMPTS = [
    "Slow, steady forward walking POV, gentle rhythmic camera sway, warm sunlight shifting on the ground, peaceful natural pace, immersive first-person perspective",
    "Medium pace walking forward, subtle handheld camera feel, light breeze moving nearby foliage, natural head-bob motion, birds flying across the sky",
    "Relaxed contemplative walk forward, smooth cinematic glide, slight left-to-right looking around motion, sun flare gently shifting, ambient dust particles floating",
    "Brisk morning walk forward through the scene, energetic camera movement, light bouncing dynamically, leaves rustling from the walking breeze",
    "Ultra-smooth steadicam forward walk, dreamy slow motion feeling, subtle focus pull from foreground to background, golden light dancing",
    "Natural casual stroll forward, gentle camera tilt looking up at the sky briefly then back forward, clouds slowly drifting, peaceful ambient motion",
    "Slow meditative walk forward, camera gently drifting right to explore the scenery, soft wind blowing grass and flowers, serene atmosphere",
    "Steady confident walk forward, dynamic camera with slight zoom-in effect, shadows lengthening, warm light intensifying",
    "Gentle flowing forward motion, camera with slight S-curve path variation, light filtering through trees shifting patterns, magical atmosphere",
]

# =========================================
# MASTER CLAUDE SYSTEM PROMPT (JSON OUTPUT)
# =========================================

CLAUDE_IMAGE_SYSTEM_PROMPT = """You are a world-class cinematographer specializing in ultra-photorealistic AI image generation using structured JSON prompts for Nano Banana Pro.

You MUST output a valid JSON object controlling every aspect of the image. Follow this exact structure:

{
  "meta": {
    "quality": "ultra photorealistic",
    "resolution": "8k",
    "camera": "(real camera model)",
    "lens": "(focal length and aperture)",
    "aspect_ratio": "9:16",
    "style": "(brief style description)"
  },
  "scene": {
    "concept": "first-person POV walking through (specific scene)",
    "location": "(detailed location)",
    "time": "(time of day and lighting conditions)"
  },
  "environment": {
    "foreground": ["(path/ground details)"],
    "midground": ["(people, objects at medium distance)"],
    "background": ["(distant scenery, sky)"],
    "atmosphere": "(ambient description)"
  },
  "camera": {
    "shot_type": "first-person POV looking forward",
    "aperture": "(f-stop)",
    "depth_of_field": "(description)",
    "perspective": "natural walking height, eye level"
  },
  "lighting": {
    "type": "(light source)",
    "direction": "(from where)",
    "quality": "(warm/cool, soft/hard)",
    "shadows": "(shadow description)"
  },
  "colors_and_tone": {
    "palette": "(specific colors)",
    "contrast": "(level)",
    "saturation": "(level and feel)"
  },
  "quality_and_technical_details": {
    "resolution": "masterpiece, extremely detailed",
    "texture_focus": "(what textures matter)",
    "noise": "(film grain description)"
  },
  "negative_prompt": {
    "forbidden_concepts": ["cartoon", "illustration", "3d render", "oversaturated", "feet visible", "legs visible", "wide angle distortion"]
  }
}

CRITICAL RULES:
1. ALWAYS first-person walking POV looking FORWARD. NEVER show feet, legs, or body.
2. ALWAYS include 1-3 people naturally in midground/background (pedestrians, joggers, couples, dog walkers)
3. Use REAL camera models (Sony, Canon, Nikon, Fujifilm) and real lens specs
4. VARY locations: beaches, forests, city parks, mountain trails, Japanese gardens, European streets, riverside paths, tropical paths, lavender fields, snowy trails, desert oases
5. Make it indistinguishable from a real photograph
6. Output ONLY the JSON, no explanation"""


class VideoGenerator:
    """
    Generates teamwork trend videos using AI.
    
    Pipeline v4: JSON prompt → Nano Banana Pro 1K (image) → Hailuo 2.3 Standard 6s 768P (video) → FFmpeg (overlay + sound)
    Image reuse: 1 base image → 3 videos per account via varied motion prompts.
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
        
        # Track used JSON templates to avoid repeats in same session
        self._used_json_templates: set = set()
        
        logger.info(f"VideoGenerator v4 initialized (Hailuo 2.3 Standard 6s), output: {self.output_dir}")
    
    # ===========================
    # Claude Prompt Generation
    # ===========================
    
    def generate_image_prompt_with_claude(self, style_hint: Optional[str] = None) -> str:
        """
        Generate ultra-realistic image prompt using JSON-structured templates or Claude.
        
        Uses structured JSON prompts for Nano Banana Pro that control every aspect
        of the image (camera, lighting, environment, etc.) for maximum photorealism.
        
        Args:
            style_hint: Optional hint like "beach", "forest", "city"
        
        Returns:
            JSON-formatted string prompt for Nano Banana Pro
        """
        # First try Claude for unique JSON prompts
        if self.claude_api_key:
            try:
                import httpx
                
                user_message = "Generate a unique, ultra-photorealistic first-person POV walking scene as a JSON object. Make it feel like a real moment captured on a premium camera."
                if style_hint:
                    user_message += f" Location theme: {style_hint}"
                user_message += " Include 1-3 people naturally in the background. Output ONLY the JSON."
                
                response = httpx.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": self.claude_api_key,
                        "anthropic-version": "2023-06-01"
                    },
                    json={
                        "model": "claude-sonnet-4-20250514",
                        "max_tokens": 800,
                        "system": CLAUDE_IMAGE_SYSTEM_PROMPT,
                        "messages": [{"role": "user", "content": user_message}]
                    },
                    timeout=30
                )
                response.raise_for_status()
                
                result = response.json()
                prompt = result.get("content", [{}])[0].get("text", "").strip()
                
                # Validate it's valid JSON
                try:
                    json.loads(prompt)
                    logger.info(f"Claude generated JSON prompt: {prompt[:120]}...")
                    return prompt
                except json.JSONDecodeError:
                    logger.warning("Claude output was not valid JSON, falling back to template")
                    
            except Exception as e:
                logger.warning(f"Claude prompt generation failed: {e}, using JSON template")
        
        # Fallback: use pre-built JSON templates
        # Pick a template we haven't used recently
        available = [i for i in range(len(JSON_PROMPT_TEMPLATES)) if i not in self._used_json_templates]
        if not available:
            self._used_json_templates.clear()
            available = list(range(len(JSON_PROMPT_TEMPLATES)))
        
        # Filter by style hint if provided
        if style_hint:
            style_lower = style_hint.lower()
            style_map = {
                "beach": 0, "forest": 1, "park": 2, "autumn": 2, "city": 2,
                "europe": 3, "cobblestone": 3, "mountain": 4, "japanese": 5,
                "japan": 5, "river": 6, "tropical": 7, "jungle": 7
            }
            for key, idx in style_map.items():
                if key in style_lower and idx in available:
                    template_idx = idx
                    break
            else:
                template_idx = random.choice(available)
        else:
            template_idx = random.choice(available)
        
        self._used_json_templates.add(template_idx)
        template = JSON_PROMPT_TEMPLATES[template_idx]
        prompt_str = json.dumps(template)
        logger.info(f"Using JSON template #{template_idx + 1}: {template['scene']['concept'][:80]}...")
        return prompt_str
    
    def generate_video_motion_prompt(self) -> str:
        """Get a random Hailuo 2.3 motion prompt for varied video output."""
        return random.choice(HAILUO_MOTION_PROMPTS)
    
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
                "-c:v", "libx264",
                "-preset", "fast",
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
        Pick a random sound from assets/sounds/ directory (local files only).
        User adds their own sounds — no API fetching.
        
        Returns:
            Path to a random sound file, or None if none available
        """
        # Collect all sound files from assets/sounds/ and subdirectories
        sound_files = []
        for ext in ('*.mp3', '*.wav', '*.m4a', '*.ogg'):
            sound_files.extend(self.sounds_dir.rglob(ext))
        
        # Filter out README and other non-audio files
        sound_files = [f for f in sound_files if f.suffix in ('.mp3', '.wav', '.m4a', '.ogg')]
        
        if sound_files:
            chosen = random.choice(sound_files)
            logger.info(f"Using local sound: {chosen.name} ({len(sound_files)} available)")
            return chosen
        
        logger.warning("No sound files in assets/sounds/ — video will have no audio")
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
    # Video Source Pipeline (YouTube via Residential Proxy)
    # Each clip gets visual uniqueness transforms
    # ===========================
    
    # YouTube search queries — ONLY footage/timelapse compilations (NO tutorials/talking)
    YOUTUBE_SEARCH_QUERIES = [
        # City timelapses
        "4K city timelapse compilation no talking",
        "city night timelapse 4K compilation",
        "drone city footage 4K no music",
        "cinematic b-roll 4K compilation",
        "city skyline timelapse night 4K",
        "tokyo night walk 4K footage",
        "new york city 4K timelapse",
        "london timelapse 4K night",
        "city traffic night 4K timelapse",
        "rain city ambience 4K footage",
        "neon city lights 4K walking",
        # Nature timelapses & compilations
        "nature scenery 4K no commentary",
        "sunset timelapse 4K collection",
        "ocean waves 4K relaxing footage",
        "mountain landscape 4K timelapse",
        "nature 4K scenery relaxing",
        "countryside 4K drone footage",
        "waterfall 4K nature compilation no talking",
        "forest drone footage 4K no commentary",
        "northern lights timelapse 4K compilation",
        "desert landscape 4K drone footage",
        "tropical beach 4K relaxing footage no talking",
        "autumn leaves 4K timelapse compilation",
        "snow mountain 4K drone footage no music",
        "river nature 4K scenery relaxing footage",
        "volcano timelapse 4K compilation",
        "starry night sky 4K timelapse no talking",
        "coral reef underwater 4K footage compilation",
        "aerial nature 4K drone compilation no commentary",
    ]
    
    # Pexels fallback queries (if YouTube fails)
    PEXELS_SEARCH_QUERIES = [
        "city night timelapse",
        "city skyline night",
        "night city lights",
        "urban night traffic",
        "sunset city skyline",
        "nature timelapse scenery",
        "ocean waves sunset",
        "mountain landscape sunset",
        "tokyo city night",
        "new york skyline night",
        "rain city night",
        "neon lights city",
        "clouds timelapse sky",
    ]
    
    def fetch_youtube_source_videos(self, max_videos: int = 2) -> int:
        """
        Download YouTube compilations via residential proxy to avoid IP blocks.
        
        Uses YOUTUBE_PROXY env var (format: socks5://user:pass@host:port)
        Falls back to direct connection if no proxy set.
        
        Downloads to {output_dir}/youtube_sources/ for scene extraction.
        """
        import yt_dlp
        
        source_dir = self.output_dir / "youtube_sources"
        source_dir.mkdir(parents=True, exist_ok=True)
        
        existing = list(source_dir.glob("*.mp4"))
        if len(existing) >= 5:
            logger.info(f"YouTube source cache has {len(existing)} videos — sufficient")
            return len(existing)
        
        # Residential proxy to bypass YouTube bot detection
        proxy_url = os.getenv("YOUTUBE_PROXY", "")
        if proxy_url:
            logger.info(f"YouTube download using proxy: {proxy_url[:30]}...")
        else:
            logger.warning("YOUTUBE_PROXY not set — downloading direct (may be blocked on datacenter IPs)")
        
        downloaded = 0
        query = random.choice(self.YOUTUBE_SEARCH_QUERIES)
        search_term = f"ytsearch3:{query}"
        
        logger.info(f"Searching YouTube for: '{query}'")
        
        ydl_opts = {
            "format": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best[height<=720]",
            "merge_output_format": "mp4",
            "outtmpl": str(source_dir / "yt_%(id)s.%(ext)s"),
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "match_filter": yt_dlp.utils.match_filter_func("duration >= 180 & duration <= 1800"),
        }
        
        # Add proxy if configured
        if proxy_url:
            ydl_opts["proxy"] = proxy_url
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
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
                            matches = list(source_dir.glob(f"yt_{video_id}.*"))
                            if matches:
                                if matches[0].suffix != ".mp4":
                                    matches[0].rename(target_path)
                                downloaded += 1
                                logger.info(f"  ✓ Downloaded: {title}")
                            else:
                                logger.warning(f"  ⚠ File not found after download: {video_id}")
                    except Exception as e:
                        logger.warning(f"  ✗ Failed to download {title}: {e}")
                        continue
                
        except Exception as e:
            logger.error(f"YouTube fetch failed: {e}")
        
        logger.info(f"YouTube fetch complete: {downloaded} new source videos")
        return downloaded
    
    def detect_scenes(self, video_path: str, threshold: float = 0.3) -> List[float]:
        """Detect scene changes using FFmpeg scene detection filter."""
        try:
            cmd = [
                "ffmpeg", "-i", video_path,
                "-vf", f"select='gt(scene,{threshold})',showinfo",
                "-vsync", "vfr",
                "-f", "null", "-"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            timestamps = []
            for line in result.stderr.split("\n"):
                if "pts_time:" in line:
                    try:
                        pts_part = line.split("pts_time:")[1]
                        ts = float(pts_part.split()[0])
                        timestamps.append(ts)
                    except (ValueError, IndexError):
                        continue
            
            if not timestamps or timestamps[0] > 1.0:
                timestamps.insert(0, 0.0)
            
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
        """Extract unique clips from each detected scene, cropped to 9:16."""
        scene_dir = self.output_dir / "scene_clips"
        scene_dir.mkdir(parents=True, exist_ok=True)
        
        source_name = Path(source_path).stem
        
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
            this_clip_duration = random.randint(7, 10)
            
            if total_duration > 0 and scene_ts + this_clip_duration > total_duration:
                continue
            
            clip_filename = f"{source_name}_scene{i:03d}.mp4"
            clip_path = scene_dir / clip_filename
            
            if clip_path.exists():
                extracted += 1
                continue
            
            try:
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", str(scene_ts),
                    "-i", source_path,
                    "-t", str(this_clip_duration),
                    "-vf", "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280",
                    "-an",
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
    
    def _replenish_scene_clips(self):
        """Auto-fetch YouTube source videos and extract ALL possible scene clips."""
        try:
            logger.info("Replenishing scene clips from YouTube...")
            downloaded = self.fetch_youtube_source_videos(max_videos=2)
            logger.info(f"YouTube fetch returned {downloaded}")
            
            source_dir = self.output_dir / "youtube_sources"
            scene_dir = self.output_dir / "scene_clips"
            
            if not source_dir.exists():
                logger.warning(f"No YouTube source dir: {source_dir}")
                return
            
            for source_video in list(source_dir.glob("*.mp4")):
                source_name = source_video.stem
                existing_clips = list(scene_dir.glob(f"{source_name}_scene*.mp4"))
                if len(existing_clips) >= 5:
                    continue
                
                logger.info(f"Processing: {source_name}...")
                scenes = self.detect_scenes(str(source_video), threshold=0.3)
                # Extract ALL detected scenes — maximize clip library
                extracted = self.extract_scene_clips(str(source_video), scenes, max_clips=999)
                logger.info(f"  Extracted {extracted} clips from {source_name}")
                
        except Exception as e:
            logger.error(f"_replenish_scene_clips FAILED: {type(e).__name__}: {e}")
    
    def fetch_pexels_footage(self, count: int = 5) -> int:
        """
        Fallback: Fetch stock clips from Pexels API (FREE) when YouTube is unavailable.
        """
        api_key = os.getenv("PEXELS_API_KEY", "")
        if not api_key:
            logger.warning("PEXELS_API_KEY not set — can't fetch Pexels footage")
            return 0
        
        stock_dir = self.output_dir / "stock_clips"
        stock_dir.mkdir(parents=True, exist_ok=True)
        
        existing = list(stock_dir.glob("*.mp4"))
        if len(existing) >= 20:
            logger.info(f"Pexels cache has {len(existing)} clips — sufficient")
            return len(existing)
        
        import httpx
        downloaded = 0
        
        try:
            query = random.choice(self.PEXELS_SEARCH_QUERIES)
            logger.info(f"Fetching from Pexels: '{query}'")
            
            with httpx.Client(timeout=30) as client:
                resp = client.get(
                    "https://api.pexels.com/videos/search",
                    params={
                        "query": query,
                        "per_page": min(count, 15),
                        "orientation": "portrait",
                        "size": "medium",
                    },
                    headers={"Authorization": api_key}
                )
                resp.raise_for_status()
                data = resp.json()
            
            videos = data.get("videos", [])
            if not videos:
                logger.warning(f"No Pexels results for '{query}'")
                return 0
            
            for video in videos[:count]:
                video_id = video.get("id", "unknown")
                video_files = video.get("video_files", [])
                
                best_file = None
                for vf in video_files:
                    w = vf.get("width", 0)
                    h = vf.get("height", 0)
                    if h >= 720 and vf.get("link"):
                        if best_file is None or (h > w and h <= 1920):
                            best_file = vf
                
                if not best_file:
                    best_file = next((vf for vf in video_files if vf.get("link")), None)
                
                if not best_file:
                    continue
                
                filename = f"stock_{video_id}.mp4"
                filepath = stock_dir / filename
                
                if filepath.exists():
                    continue
                
                try:
                    with httpx.Client(timeout=60) as client:
                        dl_resp = client.get(best_file["link"])
                        dl_resp.raise_for_status()
                        filepath.write_bytes(dl_resp.content)
                    
                    downloaded += 1
                    size_mb = filepath.stat().st_size / 1024 / 1024
                    logger.info(f"  Downloaded: {filename} ({size_mb:.1f}MB)")
                except Exception as e:
                    logger.warning(f"  Failed to download {video_id}: {e}")
            
            logger.info(f"Pexels fetch complete: {downloaded} new clips")
            
        except Exception as e:
            logger.error(f"Pexels API fetch failed: {e}")
        
        return downloaded
    
    def clip_with_transforms(self, source_path: str, output_path: str, duration: int = 8) -> bool:
        """
        Clip a video and apply random visual transforms for uniqueness.
        
        Transforms: random start, crop offset, hflip, hue shift,
        brightness/saturation, speed variation. Output: 9:16 (720x1280).
        """
        try:
            probe_cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                source_path
            ]
            probe_result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=15)
            total_duration = float(probe_result.stdout.strip() or "0")
            
            speed_factor = random.uniform(0.85, 1.15)
            adjusted_duration = duration / speed_factor
            
            if total_duration < adjusted_duration + 1:
                start_time = 0
            else:
                max_start = total_duration - adjusted_duration - 1
                start_time = random.uniform(0, max(0, max_start))
            
            # Build FFmpeg visual uniqueness filter chain
            filters = []
            
            if abs(speed_factor - 1.0) > 0.02:
                filters.append(f"setpts={1.0/speed_factor}*PTS")
            
            scale_extra = random.randint(20, 80)
            filters.append(f"scale={720 + scale_extra}:{1280 + scale_extra}:force_original_aspect_ratio=increase")
            
            crop_x = random.randint(0, scale_extra)
            crop_y = random.randint(0, scale_extra)
            filters.append(f"crop=720:1280:{crop_x}:{crop_y}")
            
            if random.random() < 0.5:
                filters.append("hflip")
            
            hue_shift = random.uniform(-30, 30)
            brightness = random.uniform(-0.1, 0.1)
            saturation = random.uniform(0.85, 1.15)
            filters.append(f"eq=brightness={brightness:.3f}:saturation={saturation:.2f}")
            filters.append(f"hue=h={hue_shift:.1f}")
            
            filter_chain = ",".join(filters)
            
            cmd = [
                "ffmpeg", "-y",
                "-ss", str(start_time),
                "-i", source_path,
                "-t", str(adjusted_duration),
                "-vf", filter_chain,
                "-an",
                "-c:v", "libx264",
                "-preset", "fast",
                "-movflags", "+faststart",
                "-t", str(duration),
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            
            if result.returncode == 0:
                transforms_log = f"speed={speed_factor:.2f}x, hue={hue_shift:+.0f}°, bright={brightness:+.2f}, sat={saturation:.2f}"
                logger.info(f"Unique clip: {duration}s from {start_time:.1f}s [{transforms_log}]")
                return True
            else:
                logger.error(f"Transform clip failed: {result.stderr[:200]}")
                return False
                
        except Exception as e:
            logger.error(f"clip_with_transforms failed: {e}")
            return False
    
    def clip_stock_footage(self, source_path: str, output_path: str, duration: int = 8) -> bool:
        """Basic clip fallback: crop to 9:16 without visual transforms."""
        try:
            probe_cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                source_path
            ]
            probe_result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=15)
            total_duration = float(probe_result.stdout.strip() or "0")
            
            if total_duration < duration + 1:
                start_time = 0
            else:
                max_start = total_duration - duration - 1
                start_time = random.uniform(0, max(0, max_start))
            
            cmd = [
                "ffmpeg", "-y",
                "-ss", str(start_time),
                "-i", source_path,
                "-t", str(duration),
                "-vf", "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280",
                "-an",
                "-c:v", "libx264",
                "-preset", "fast",
                "-movflags", "+faststart",
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info(f"Basic clip: {duration}s from {start_time:.1f}s")
                return True
            else:
                logger.error(f"Basic clip failed: {result.stderr[:200]}")
                return False
                
        except Exception as e:
            logger.error(f"clip_stock_footage failed: {e}")
            return False
    
    def generate_stock_video(
        self,
        text_overlay: Optional[str] = None,
    ) -> 'GeneratedVideo':
        """
        Generate a unique video using YouTube scene clips (via residential proxy).
        
        Pipeline:
        1. Fetch YouTube scene clips via residential proxy
        2. Apply visual uniqueness transforms (hue, speed, flip, brightness, crop offset)
        3. Add Loom-style multi-line text overlay
        4. Add trending sound
        5. Strip metadata
        
        Cost: $0.00 — each clip is visually unique
        """
        start_time = time.time()
        
        # === SOURCE: YouTube scene clips only (no Pexels) ===
        # Clips are DELETED after use to guarantee no reuse
        source_clip = None
        source_type = None
        
        scene_dir = self.output_dir / "scene_clips"
        scene_dir.mkdir(parents=True, exist_ok=True)
        scene_clips = list(scene_dir.glob("*.mp4"))
        
        if len(scene_clips) < 5:
            logger.info("Low scene clips cache — fetching from YouTube...")
            self._replenish_scene_clips()
            scene_clips = list(scene_dir.glob("*.mp4"))
        
        if scene_clips:
            source_clip = random.choice(scene_clips)
            source_type = "youtube_scene"
            logger.info(f"Using YouTube scene clip: {source_clip.name} ({len(scene_clips)} remaining)")
        
        if source_clip is None:
            logger.error("No YouTube scene clips available. Check YOUTUBE_PROXY env var and proxy credentials.")
            return GeneratedVideo(
                success=False,
                error="No YouTube clips available. Check YOUTUBE_PROXY env var.",
                cost_usd=0.00
            )
        
        # 2. Clip + apply visual transforms
        clip_duration = 7  # Fixed 7-second clips
        video_filename = f"teamwork_{int(time.time())}_{random.randint(1000, 9999)}.mp4"
        raw_clip_path = self.output_dir / f"raw_{video_filename}"
        final_video_path = self.output_dir / video_filename
        
        clip_success = self.clip_with_transforms(
            str(source_clip),
            str(raw_clip_path),
            duration=clip_duration
        )
        
        if not clip_success:
            clip_success = self.clip_stock_footage(
                str(source_clip),
                str(raw_clip_path),
                duration=clip_duration
            )
        
        if not clip_success:
            logger.error(f"Clip processing failed for {source_type} clip")
            return GeneratedVideo(
                success=False,
                error="Clip processing failed",
                cost_usd=0.00
            )
        
        # Delete the source scene clip after use — never reuse
        try:
            source_clip.unlink()
            logger.info(f"Deleted used scene clip: {source_clip.name}")
        except Exception as e:
            logger.warning(f"Could not delete used clip {source_clip.name}: {e}")
        
        # 3. Add text overlay
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
        
        elapsed = time.time() - start_time
        
        if final_video_path.exists():
            logger.info(f"Video generated ({source_type}) in {elapsed:.1f}s: {final_video_path.name}")
            return GeneratedVideo(
                success=True,
                video_path=str(final_video_path),
                text_overlay=final_text_line,
                cost_usd=0.00
            )
        else:
            return GeneratedVideo(
                success=False,
                error="Video pipeline failed",
                cost_usd=0.00
            )
    
    # ===========================
    # Main Video Pipeline v4 (AI — costs ~$0.15-0.24/video)
    # ===========================
    
    def generate_teamwork_video(
        self,
        style_hint: Optional[str] = None,
        text_overlay: Optional[str] = None,
        skip_overlay: bool = False,
        image_url: Optional[str] = None
    ) -> GeneratedVideo:
        """
        Generate a complete teamwork trend video.
        
        Pipeline v4:
        1. JSON-structured prompt → Nano Banana Pro 1K creates ultra-realistic image
        2. Hailuo 2.3 Standard converts to 6s 768P video
        3. FFmpeg adds text overlay
        4. FFmpeg adds random trending sound
        5. FFmpeg strips metadata
        
        Args:
            style_hint: Location style hint (beach, forest, city, etc.)
            text_overlay: Custom text, or random from list
            skip_overlay: Skip FFmpeg overlay step
            image_url: Pre-generated image URL (for image reuse across multiple videos)
        
        Returns:
            GeneratedVideo with paths and URLs
        """
        cost = 0.0
        image_prompt = None
        
        # 1. Generate or reuse image
        if image_url:
            # Reuse existing image (no extra cost)
            logger.info(f"Step 1: Reusing existing image: {image_url[:80]}...")
        else:
            # Generate new image with JSON prompt
            logger.info("Step 1: Generating JSON image prompt...")
            image_prompt = self.generate_image_prompt_with_claude(style_hint)
            
            logger.info("Step 2: Generating 1K image with Nano Banana Pro...")
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
            cost += 0.09  # Nano Banana Pro 1K cost
            logger.info(f"1K Image generated: {image_url}")
        
        # 2. Convert to video with Hailuo 2.3 Standard (6s, 768P)
        logger.info("Step 3: Converting to video with Hailuo 2.3 Standard 6s 768P...")
        video_prompt = self.generate_video_motion_prompt()
        
        video_result = self.kie.image_to_video_hailuo(
            image_url=image_url,
            prompt=video_prompt,
            duration="6",
            resolution="768P"
        )
        
        if not video_result.success:
            return GeneratedVideo(
                success=False,
                error=f"Hailuo video failed: {video_result.error}",
                image_url=image_url,
                prompt_used=image_prompt,
                cost_usd=cost
            )
        
        # Wait for video
        logger.info(f"Waiting for Hailuo video task {video_result.task_id}...")
        video_final = self.kie.wait_for_task(video_result.task_id, timeout_seconds=600)
        
        if not video_final.success or not video_final.result_urls:
            return GeneratedVideo(
                success=False,
                error=f"Hailuo video failed: {video_final.error or 'No result URLs'}",
                image_url=image_url,
                prompt_used=image_prompt,
                cost_usd=cost
            )
        
        video_url = video_final.result_urls[0]
        cost += 0.15  # Hailuo 2.3 Standard 6s 768P cost
        logger.info(f"Hailuo video generated: {video_url}")
        
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
            text_overlay=final_text_line if not skip_overlay else None,
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
    
    def generate_batch_for_account(
        self,
        count: int = 3,
        style_hint: Optional[str] = None,
        text_overlay: Optional[str] = None,
        skip_overlay: bool = False
    ) -> List[GeneratedVideo]:
        """
        Generate multiple AI videos for one account, reusing a single base image.
        
        Cost optimization: generates 1 image ($0.09) then creates 'count' videos
        from it concurrently with varied Hailuo 2.3 motion prompts ($0.15 each).
        
        Args:
            count: Number of videos (default 3 per account)
            style_hint: Location theme for the base image
            text_overlay: Custom text overlay (or random)
            skip_overlay: Skip text overlay step
        
        Returns:
            List of GeneratedVideo results
        """
        import concurrent.futures
        results = []
        
        # Step 1: Generate ONE base image
        logger.info(f"=== Batch for account: generating 1 image + {count} videos ===")
        logger.info("Batch Step 1: Generating base image...")
        
        image_prompt = self.generate_image_prompt_with_claude(style_hint)
        
        image_result = self.kie.generate_image(
            prompt=image_prompt,
            aspect_ratio="9:16",
            resolution="1K",
            output_format="png"
        )
        
        if not image_result.success:
            logger.error(f"Base image generation failed: {image_result.error}")
            return [GeneratedVideo(success=False, error=f"Base image failed: {image_result.error}")] * count
        
        image_final = self.kie.wait_for_task(image_result.task_id, timeout_seconds=180)
        
        if not image_final.success or not image_final.result_urls:
            logger.error(f"Base image failed: {image_final.error or 'No URLs'}")
            return [GeneratedVideo(success=False, error=f"Base image failed: {image_final.error}")] * count
        
        base_image_url = image_final.result_urls[0]
        logger.info(f"Base image ready: {base_image_url[:80]}...")
        
        # Step 2: Generate 'count' videos CONCURRENTLY from the SAME image
        logger.info(f"Batch Step 2: Submitting {count} video generation tasks concurrently...")
        
        def _generate_single_video(i):
            logger.info(f"Batch thread {i+1}/{count}: Starting video generation...")
            try:
                # Add slight stagger to avoid rate limiting on submission
                time.sleep(i * 1.5)
                res = self.generate_teamwork_video(
                    style_hint=style_hint,
                    text_overlay=text_overlay,
                    skip_overlay=skip_overlay,
                    image_url=base_image_url
                )
                if res.success:
                    logger.info(f"Batch thread {i+1}: Success - {res.video_path}")
                else:
                    logger.error(f"Batch thread {i+1}: Failed - {res.error}")
                return res
            except Exception as e:
                logger.error(f"Batch thread {i+1} crashed: {e}")
                return GeneratedVideo(success=False, error=str(e))
        
        # Run video generations in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=count) as executor:
            # Submit all tasks
            futures = [executor.submit(_generate_single_video, i) for i in range(count)]
            # Wait for all to complete
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
        
        total_cost = 0.09 + sum(r.cost_usd for r in results)  # Add image cost
        success_count = sum(1 for r in results if r.success)
        logger.info(f"=== Batch complete: {success_count}/{count} videos, total cost: ${total_cost:.2f} ===")
        
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
