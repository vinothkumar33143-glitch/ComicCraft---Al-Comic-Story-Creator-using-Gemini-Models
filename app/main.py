from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .routes import router


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Generate five-panel AI comic stories with Gemini and Stable Diffusion.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)
