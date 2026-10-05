# ComicCraft — AI Comic Story Creator

ComicCraft is a FastAPI + Jinja2 web application that turns a story idea into a five-panel comic.

## Architecture

- **FastAPI** — web/API server and request validation
- **Google GenAI SDK** — structured comic outline + story/narration
- **Hugging Face Diffusers** — local Stable Diffusion image generation
- **Pillow** — image handling
- **FPDF2** — PDF export
- **Jinja2** — server-rendered frontend

The original specification referenced `google-generativeai`, Gemini 1.5 Pro, and an older Diffusers workflow. This implementation uses Google's current `google-genai` SDK and configurable current Gemini model names.

## Quick start (Windows)

```powershell
cd ComicCraft
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
copy .env.example .env
```

For the fastest first run, leave:

```env
AI_MODE=mock
IMAGE_PROVIDER=placeholder
```

Then:

```powershell
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

API docs: http://127.0.0.1:8000/docs

## Real Gemini + Stable Diffusion

Create a Gemini API key and put it in `.env`:

```env
AI_MODE=gemini
GEMINI_API_KEY=your_key_here
GEMINI_OUTLINE_MODEL=gemini-3.6-flash
GEMINI_STORY_MODEL=gemini-3.1-pro-preview
```

For local Diffusers image generation, first install the optional AI image packages:

```powershell
python -m pip install -r requirements-ai-images.txt
```

Then set these values in `.env`:

```env
IMAGE_PROVIDER=diffusers
DIFFUSION_MODEL=stabilityai/stable-diffusion-xl-base-1.0
```

The first image generation downloads the model from Hugging Face and can require many GB of disk/RAM/VRAM. A CUDA-capable GPU is strongly recommended. The default placeholder provider works without downloading a model.

If you do not have suitable hardware, keep `IMAGE_PROVIDER=placeholder` while developing the UI/API, or replace `image_generator.py` with a hosted image provider.

## API

### POST `/generate-comic/json`

```json
{
  "story_prompt": "A brave fox explores an enchanted forest.",
  "character_name": "Fenn",
  "setting": "forest",
  "tone": "dramatic",
  "art_style": "comic book"
}
```

Returns the generated panel layout and PDF download URL.

### GET `/health`

Returns application and provider status.

### POST `/test-image`

Generate one image from a prompt.

## Project structure

```text
ComicCraft/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── routes.py
│   ├── workflow.py
│   ├── gemini_flash.py
│   ├── gemini_pro.py
│   ├── image_generator.py
│   ├── layout_builder.py
│   └── exporters.py
├── static/
│   ├── css/style.css
│   ├── js/app.js
│   ├── panels/.gitkeep
│   └── exports/.gitkeep
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
├── tests/
│   ├── test_health.py
│   ├── test_layout.py
│   └── test_pdf.py
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-ai-images.txt  # optional local Stable Diffusion dependencies
└── README.md
```

## VS Code

1. Open the `ComicCraft` folder.
2. Install the Python extension.
3. Select `.venv` as the Python interpreter.
4. Open a terminal and activate the environment.
5. Run `uvicorn app.main:app --reload`.
6. Use the browser UI or `/docs`.

## Testing

```powershell
pip install pytest httpx
pytest -q
```

Tests intentionally use mock/placeholder providers so they do not require paid APIs or model downloads.

## Notes

Generated files are stored under `static/panels` and `static/exports`. They are ignored by Git except for `.gitkeep`.

Never commit `.env` or API keys.

## Mobile / Android

For an Android-only setup, see `MOBILE_SETUP.md`. The included `run_mobile.py` launcher starts the app with a phone-friendly host. The default configuration is mock AI + placeholder images, so no API key or Stable Diffusion model is required for the demo.
