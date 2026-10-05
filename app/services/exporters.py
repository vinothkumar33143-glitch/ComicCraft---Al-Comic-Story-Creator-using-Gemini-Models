from __future__ import annotations

from datetime import datetime, timezone
import unicodedata

from fpdf import FPDF

from app.config import get_settings


def _pdf_text(value) -> str:
    if value is None:
        return ""
    value = unicodedata.normalize("NFKC", str(value))
    replacements = {
        "—": "-", "–": "-", "“": '"', "”": '"',
        "‘": "'", "’": "'", "…": "...", "•": "-", "\u00a0": " ",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value.encode("latin-1", "replace").decode("latin-1")


def save_pdf(title: str, panels) -> str:
    settings = get_settings()
    settings.exports_dir.mkdir(parents=True, exist_ok=True)
    filename = f"comic-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f')}.pdf"
    output = settings.exports_dir / filename

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.set_margins(left=15, top=15, right=15)

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.multi_cell(0, 12, _pdf_text(title), align="C")
    pdf.ln(8)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, "Created with ComicCraft", align="C")

    for panel in panels:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        number = getattr(panel, "panel_number", 0)
        panel_title = getattr(panel, "title", "")
        pdf.multi_cell(0, 10, f"Panel {number}: {_pdf_text(panel_title)}")
        pdf.ln(3)

        image_url = getattr(panel, "image_url", "")
        image_drawn = False
        if image_url:
            image_path = settings.static_dir / str(image_url).removeprefix("/static/")
            if image_path.exists():
                try:
                    pdf.image(str(image_path), x=15, y=40, w=180)
                    image_drawn = True
                except Exception as exc:
                    print(f"PDF image warning: {exc}")

        # The 3:2 comic image is about 120 mm tall at 180 mm width.
        # Keep the panel text below the image instead of overlapping it.
        pdf.set_xy(15, 165 if image_drawn else 45)
        pdf.set_font("Helvetica", "I", 10)
        scene = getattr(panel, "scene_description", "")
        if scene:
            pdf.multi_cell(0, 6, _pdf_text(scene))

        narration = getattr(panel, "narration", "")
        if narration:
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_x(15)
            pdf.multi_cell(0, 6, "Narration")
            pdf.set_font("Helvetica", "", 10)
            pdf.set_x(15)
            pdf.multi_cell(0, 6, _pdf_text(narration))

        dialogue = getattr(panel, "dialogue", None)
        if dialogue:
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_x(15)
            pdf.multi_cell(0, 6, "Dialogue")
            pdf.set_font("Helvetica", "", 10)
            lines = dialogue if isinstance(dialogue, list) else [dialogue]
            for line in lines:
                pdf.set_x(15)
                pdf.multi_cell(0, 6, _pdf_text(line))

        caption = getattr(panel, "caption", "")
        if caption:
            pdf.ln(3)
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_x(15)
            pdf.multi_cell(0, 6, _pdf_text(caption))

    pdf.output(str(output))
    return f"/static/exports/{filename}"
