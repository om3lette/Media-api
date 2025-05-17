from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from starlette.responses import FileResponse

from src.constants import TEMPLATES_PATH, OUT_FOLDER

static_router: APIRouter = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_PATH)


@static_router.get("/output/{subpath:path}", response_class=HTMLResponse)
async def output_browser(subpath: str):
    target_path: Path = OUT_FOLDER / subpath

    if target_path.is_file():
        return FileResponse(
            target_path,
            filename=target_path.name,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f'attachment; filename="{target_path.name}"'
            },
        )

    if len(subpath) == 0 or not target_path.exists():
        raise HTTPException(status_code=404, detail="Not found")

    if target_path.is_dir():
        files = list(target_path.iterdir())
        s = subpath.replace("/", "")
        links = [
            f'<li><a style="font-size: 16pt"href="/output/{s}/{f.name}">{f.name}</a></li>'
            for f in files
        ]
        return f"<h1>Contents of /output/{subpath}</h1><ul>{''.join(links)}</ul>"

    raise HTTPException(status_code=400, detail="Invalid path")


@static_router.get("/", response_class=HTMLResponse)
async def serve_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
