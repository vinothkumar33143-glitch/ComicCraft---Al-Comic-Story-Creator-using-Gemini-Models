from app.config import get_settings
from app.exporters import save_pdf
from app.models import ComicPanel


def test_pdf_export():
    panel = ComicPanel(
        panel_number=1,
        title="Test",
        image_url="/static/panels/nonexistent.png",
        scene_description="A test scene.",
        image_prompt="test",
        caption="A caption.",
        narration="A narration.",
        dialogue=[],
    )
    url = save_pdf("Test", [panel])
    path = get_settings().static_dir / url.removeprefix("/static/")
    assert path.exists()
    assert path.suffix == ".pdf"
