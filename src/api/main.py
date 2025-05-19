import logging
import asyncio

from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from src.api.templates.router import static_router
from src.api.common.router import requests_router
from src.api.status.router import request_status_router
from src.api.common.handlers import (
    global_requests_handler,
    register_helpers,
    register_handlers,
)
from src.app_config import app_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%H:%M:%S %d-%m-%Y",
)


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    register_handlers()
    await register_helpers()

    asyncio.create_task(global_requests_handler.start())
    yield
    if not app_config.dev_mode:
        await global_requests_handler.queue.join()


app: FastAPI = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app_router: APIRouter = APIRouter()
app_router.include_router(requests_router)
app_router.include_router(request_status_router, prefix="/status")

app.include_router(app_router, prefix="/v1")
app.include_router(static_router)
