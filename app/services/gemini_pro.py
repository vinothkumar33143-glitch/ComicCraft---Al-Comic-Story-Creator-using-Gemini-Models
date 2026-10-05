from app.config import get_settings
from app.models import ComicOutline, ComicStory, PanelStory, PromptRequest


def _client():
    from google import genai
    settings = get_settings()
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=settings.gemini_api_key)


def _mock_story(request: PromptRequest, outline: ComicOutline) -> ComicStory:
    panels = []
    for panel in outline.panels:
        panels.append(
            PanelStory(
                panel_number=panel.panel_number,
                title=panel.title,
                caption=f"{request.tone.title()} atmosphere — {panel.scene_description}",
                narration=(
                    f"{request.character_name} moves through {request.setting}, following the mystery "
                    f"described in the story idea. The moment feels {request.tone} as the adventure develops."
                ),
                dialogue=[f"{request.character_name}: We have to keep going!"],
            )
        )
    return ComicStory(panels=panels)


def generate_story(request: PromptRequest, outline: ComicOutline) -> ComicStory:
    settings = get_settings()
    if settings.ai_mode.lower() == "mock":
        return _mock_story(request, outline)

    from google.genai import types
    client = _client()
    prompt = f"""
Expand this five-panel outline into polished comic narration.

Story idea: {request.story_prompt}
Character: {request.character_name}
Setting: {request.setting}
Tone: {request.tone}
Art style: {request.art_style}

Outline:
{outline.model_dump_json(indent=2)}

Return exactly five matching panels. For each panel provide:
- title
- short atmospheric caption
- concise narration
- natural character dialogue as a list

Keep continuity across panels and keep the content suitable for a general audience.
"""
    response = client.models.generate_content(
        model=settings.gemini_story_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComicStory,
        ),
    )
    if getattr(response, "parsed", None):
        result = response.parsed
        if isinstance(result, ComicStory):
            return result
    return ComicStory.model_validate_json(response.text)
