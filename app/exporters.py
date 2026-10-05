from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import unicodedata

from fpdf import FPDF

from .config import get_settings
from .models import ComicPanel


def _pdf_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value)
    replacements = {"—": "-", "–": "-", "“": '"', "”": '"', "’": "'", "…": "..."}
    return "".join(replacements.get(ch, ch) for ch in value).encode("latin-1", "replace").decode("latin-1")


def save_pdf(title: str, panels: list[ComicPanel]) -> str:
    settings = get_settings()
    filename = f"comic-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')}.pdf"
    output = settings.exports_dir / filename

    pdf = FPDF(unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=14)

    for panel in panels:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.multi_cell(0, 10, _pdf_text(f"Panel {panel.panel_number}: {panel.title}"))
        pdf.ln(2)

        image_path = settings.static_dir / panel.image_url.removeprefix("/static/")
        image_drawn = image_path.exists()
        if image_drawn:
            pdf.image(str(image_path), x=15, y=35, w=180)

        # A 180 mm wide 3:2 image is about 120 mm tall, ending near y=155.
        # Start text below the image to prevent overlap; without an image, use the space near the top.
        pdf.set_xy(15, 160 if image_drawn else 45)
        pdf.set_font("Helvetica", "I", 10)
        pdf.multi_cell(0, 6, _pdf_text(panel.scene_description))
        pdf.ln(3)

        pdf.set_font("Helvetica", "B", 11)
        pdf.ln(2)

        pdf.set_x(15)
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 6, "Narration")
        pdf.set_x(15)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, _pdf_text(panel.narration))

        if panel.dialogue:
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_x(15)
            pdf.multi_cell(0, 6, "Dialogue")
            pdf.set_font("Helvetica", "", 10)
            for line in panel.dialogue:
                pdf.set_x(15)
                pdf.multi_cell(0, 6, _pdf_text(line))

    pdf.output(str(output))
    return f"/static/exports/{filename}"
