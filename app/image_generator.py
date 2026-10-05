from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .config import get_settings


_PIPELINE = None


def _safe_name(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-")
    return value[:60] or "panel"


def _placeholder(prompt: str, panel_number: int, output: Path) -> str:
    settings = get_settings()
    image = Image.new("RGB", (settings.image_width, settings.image_height), "#f4efe6")
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 30)
        small = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
        small = ImageFont.load_default()

    draw.rounded_rectangle((24, 24, settings.image_width - 24, settings.image_height - 24), 18, outline="#222", width=5)
    draw.text((55, 55), f"COMICCRAFT • PANEL {panel_number}", fill="#222", font=font)
    words = prompt.split()
    lines, current = [], ""
    for word in words:
        test = f"{current} {word}".strip()
        if len(test) > 55:
            lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)
    y = 125
    for line in lines[:10]:
        draw.text((55, y), line, fill="#444", font=small)
        y += 28
    draw.text((55, settings.image_height - 75), "Development placeholder — set IMAGE_PROVIDER=diffusers for AI images.", fill="#666", font=small)
    image.save(output, format="PNG")
    return f"/static/panels/{output.name}"


def _load_pipeline():
    global _PIPELINE
    if _PIPELINE is not None:
        return _PIPELINE

    settings = get_settings()
    import torch
    from diffusers import DiffusionPipeline

    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    kwargs = {"torch_dtype": dtype}
    if settings.hf_token:
        kwargs["token"] = settings.hf_token

    _PIPELINE = DiffusionPipeline.from_pretrained(settings.diffusion_model, **kwargs)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    _PIPELINE = _PIPELINE.to(device)
    return _PIPELINE


def generate_image(prompt: str, panel_number: int) -> str:
    settings = get_settings()
    filename = f"panel-{panel_number:02d}-{_safe_name(prompt)[:35]}.png"
    output = settings.panels_dir / filename

    if settings.image_provider.lower() == "placeholder":
        return _placeholder(prompt, panel_number, output)

    if settings.image_provider.lower() != "diffusers":
        raise RuntimeError("IMAGE_PROVIDER must be 'placeholder' or 'diffusers'.")

    pipe = _load_pipeline()
    image = pipe(
        prompt=prompt,
        negative_prompt="blurry, distorted, malformed hands, unreadable text, watermark",
        width=settings.image_width,
        height=settings.image_height,
        num_inference_steps=20,
        guidance_scale=7.0,
    ).images[0]
    image.save(output, format="PNG")
    return f"/static/panels/{output.name}"
