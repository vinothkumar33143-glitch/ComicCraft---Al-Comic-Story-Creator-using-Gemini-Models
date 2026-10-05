from functools import lru_cache
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:
    app_name = "ComicCraft"
    app_env = "development"
    host = "127.0.0.1"
    port = 8000

    ai_mode = os.getenv("AI_MODE", "mock")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    gemini_outline_model = "gemini-3.6-flash"
    gemini_story_model = "gemini-3.1-pro-preview"

    image_provider = "placeholder"
    diffusion_model = "stabilityai/stable-diffusion-xl-base-1.0"
    hf_token = os.getenv("HF_TOKEN")

    panel_count = 5
    image_width = 768
    image_height = 512

    @property
    def static_dir(self):
        return BASE_DIR / "static"

    @property
    def panels_dir(self):
        return self.static_dir / "panels"

    @property
    def exports_dir(self):
        return self.static_dir / "exports"

    @property
    def templates_dir(self):
        return BASE_DIR / "templates"


@lru_cache
def get_settings():
    settings = Settings()
    settings.panels_dir.mkdir(parents=True, exist_ok=True)
    settings.exports_dir.mkdir(parents=True, exist_ok=True)
    return settings
