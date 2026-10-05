from .exporters import save_pdf
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .models import ComicResponse, PromptRequest


def generate_comic(request: PromptRequest, export_pdf: bool = True) -> ComicResponse:
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
