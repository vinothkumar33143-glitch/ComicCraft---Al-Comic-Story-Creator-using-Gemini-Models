from .models import ComicOutline, ComicStory, ComicPanel


def build_comic_layout(outline: ComicOutline, story: ComicStory, image_urls: list[str]) -> list[ComicPanel]:
    story_by_number = {p.panel_number: p for p in story.panels}
    result: list[ComicPanel] = []

    for index, outline_panel in enumerate(outline.panels):
        story_panel = story_by_number.get(outline_panel.panel_number)
        if story_panel is None:
            raise ValueError(f"Missing story panel {outline_panel.panel_number}.")
        result.append(
            ComicPanel(
                panel_number=outline_panel.panel_number,
                title=outline_panel.title,
                image_url=image_urls[index],
                scene_description=outline_panel.scene_description,
                image_prompt=outline_panel.image_prompt,
                caption=story_panel.caption,
                narration=story_panel.narration,
                dialogue=story_panel.dialogue,
            )
        )
    return result
