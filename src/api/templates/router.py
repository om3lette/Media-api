from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from src.constants import TEMPLATES_PATH

static_router: APIRouter = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_PATH)

@static_router.get("/", response_class=HTMLResponse)
async def serve_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
