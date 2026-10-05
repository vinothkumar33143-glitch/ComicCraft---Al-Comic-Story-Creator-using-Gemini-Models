from typing import Literal

from pydantic import BaseModel, Field, validator


Tone = Literal["light-hearted", "dramatic", "poetic", "funny"]
ArtStyle = Literal["anime", "pixel art", "comic book", "realistic"]
Setting = Literal["school", "forest", "space", "city", "custom"]


class PromptRequest(BaseModel):
    story_prompt: str = Field(min_length=5, max_length=2000)
    character_name: str = Field(min_length=1, max_length=80)
    setting: str = Field(min_length=1, max_length=120)
    tone: Tone
    art_style: ArtStyle

    @validator("story_prompt", "character_name", "setting")
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty.")
        return value


class PanelOutline(BaseModel):
    panel_number: int = Field(ge=1, le=5)
    title: str
    scene_description: str
    image_prompt: str


class ComicOutline(BaseModel):
    panels: list[PanelOutline]


class PanelStory(BaseModel):
    panel_number: int = Field(ge=1, le=5)
    title: str
    caption: str
    narration: str
    dialogue: list[str] = Field(default_factory=list)


class ComicStory(BaseModel):
    panels: list[PanelStory]


class ComicPanel(BaseModel):
    panel_number: int
    title: str
    image_url: str
    scene_description: str
    image_prompt: str
    caption: str
    narration: str
    dialogue: list[str] = Field(default_factory=list)


class ComicResponse(BaseModel):
    title: str
    panels: list[ComicPanel]
    pdf_url: str | None = None
