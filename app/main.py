from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Minimal Web+API")

# Flat structure: /app/static and /app/templates
static_dir = Path("static")
templates_dir = Path("templates")

# Mount static files only if the directory exists (handy during early stages)
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

templates = Jinja2Templates(directory=str(templates_dir))

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the home page as HTML."""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Hello from FastAPI",
            "message": "Hi! This is HTML rendered via FastAPI + Jinja2 using a flat /app structure.",
        },
    )

@app.get("/api/health")
async def health():
    """Simple health check endpoint."""
    return {"status": "ok"}

@app.get("/api/echo")
async def echo(q: str = "world"):
    """Echo back the provided query string."""
    return {"echo": q}
