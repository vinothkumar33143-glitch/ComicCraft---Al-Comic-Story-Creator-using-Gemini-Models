from app.layout_builder import build_comic_layout
from app.models import ComicOutline, ComicStory, PanelOutline, PanelStory


def test_layout_matches_panels():
    outline = ComicOutline(
        panels=[
            PanelOutline(panel_number=1, title="One", scene_description="A", image_prompt="A"),
            PanelOutline(panel_number=2, title="Two", scene_description="B", image_prompt="B"),
        ]
    )
    story = ComicStory(
        panels=[
            PanelStory(panel_number=1, title="One", caption="C", narration="D"),
            PanelStory(panel_number=2, title="Two", caption="E", narration="F"),
        ]
    )
    layout = build_comic_layout(outline, story, ["/static/panels/a.png", "/static/panels/b.png"])
    assert len(layout) == 2
    assert layout[1].image_url.endswith("b.png")
