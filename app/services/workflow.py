from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.models import ComicResponse, PromptRequest


def generate_comic(request: PromptRequest, export_pdf: bool = False) -> ComicResponse:
    outline = generate_outline(request)
    story = generate_story(request, outline)

    image_urls = [
        generate_image(panel.image_prompt, panel.panel_number)
        for panel in outline.panels
    ]

    panels = build_comic_layout(outline, story, image_urls)
    title = f"{request.character_name}'s Comic Adventure"
    pdf_url = save_pdf(title, panels) if export_pdf else None

    return ComicResponse(title=title, panels=panels, pdf_url=pdf_url)
