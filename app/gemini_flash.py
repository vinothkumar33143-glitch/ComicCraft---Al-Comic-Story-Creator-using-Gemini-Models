from .config import get_settings
from .models import ComicOutline, PanelOutline, PromptRequest


def _client():
    from google import genai
    settings = get_settings()
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=settings.gemini_api_key)


def _mock_outline(request: PromptRequest) -> ComicOutline:
    scenes = [
        ("The Spark", "The hero discovers an unusual clue that changes the ordinary day."),
        ("Into the Unknown", "The hero follows the clue into a visually striking part of the setting."),
        ("The Challenge", "A surprising obstacle forces the hero to make a brave choice."),
        ("The Turning Point", "The hero finds a clever way through the obstacle and learns something important."),
        ("A New Beginning", "The adventure ends with a memorable image and a hint of what comes next."),
    ]
    panels = []
    for i, (title, description) in enumerate(scenes, 1):
        panels.append(
            PanelOutline(
                panel_number=i,
                title=title,
                scene_description=f"{description} Character: {request.character_name}. Setting: {request.setting}.",
                image_prompt=(
                    f"{request.art_style} comic illustration, {request.character_name} in {request.setting}, "
                    f"{description.lower()} cinematic composition, expressive character, clear foreground and background"
                ),
            )
        )
    return ComicOutline(panels=panels)


def generate_outline(request: PromptRequest) -> ComicOutline:
    settings = get_settings()
    if settings.ai_mode.lower() == "mock":
        return _mock_outline(request)

    from google.genai import types
    client = _client()
    prompt = f"""
Create a cohesive five-panel comic outline.

Story idea: {request.story_prompt}
Main character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}

Requirements:
- Exactly 5 panels.
- Maintain continuity of character, setting, and action.
- Each image_prompt must be suitable for a text-to-image model.
- Do not put speech bubbles or readable text inside the image prompt.
- Keep the story age-appropriate.
"""
    response = client.models.generate_content(
        model=settings.gemini_outline_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComicOutline,
        ),
    )
    if getattr(response, "parsed", None):
        result = response.parsed
        if isinstance(result, ComicOutline):
            return result
    return ComicOutline.model_validate_json(response.text)
