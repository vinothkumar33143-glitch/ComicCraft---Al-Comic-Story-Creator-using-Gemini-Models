from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from .config import get_settings
from app.services.image_generator import generate_image
from .models import PromptRequest
from app.services.workflow import generate_comic


router = APIRouter()
settings = get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"app_name": settings.app_name})


@router.post("/generate", response_class=HTMLResponse)
def generate_form(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        payload = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )
        comic = generate_comic(payload)
    except Exception as exc:
        return templates.TemplateResponse(request, "index.html", {
            
            "app_name": settings.app_name,
            "error": str(exc),
            "form": {
                "story_prompt": story_prompt,
                "character_name": character_name,
                "setting": setting,
                "tone": tone,
                "art_style": art_style,
            },
        }, status_code=500)


@router.post("/generate-comic/json")
def generate_json(payload: PromptRequest):
    try:
        return generate_comic(payload).model_dump()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/test-image")
def test_image(prompt: str = Form(...)):
    try:
        return {"image_url": generate_image(prompt, 1)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/download/{filename}")
def download_pdf(filename: str):
    safe_name = Path(filename).name
    path = settings.exports_dir / safe_name
    if not path.exists() or path.suffix.lower() != ".pdf":
        raise HTTPException(status_code=404, detail="PDF not found.")
    return FileResponse(path, media_type="application/pdf", filename=safe_name)


@router.get("/export-success", response_class=HTMLResponse)
def export_success(request: Request, filename: str | None = None):
    return templates.TemplateResponse(request, "index.html", {"app_name": settings.app_name})


@router.get("/health")
def health():
    return {
        "status": "ok",
        "ai_mode": settings.ai_mode,
        "image_provider": settings.image_provider,
        "gemini_configured": bool(settings.gemini_api_key),
    }
