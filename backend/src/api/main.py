import asyncio
import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.src.api.common.handlers import (
    global_requests_handler,
    register_handlers,
    register_helpers,
)
from backend.src.api.common.io_handlers import requests_repository, db_connection
from backend.src.api.common.router import requests_router
from backend.src.api.download.router import download_router
from backend.src.api.status.handlers import status_subscriber
from backend.src.api.status.router import request_status_router
from backend.src.api.common.background_cleaner import disk_cleanup
from backend.src.app_config import app_config
from backend.src.constants import OPENAPI_SCHEMA

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%H:%M:%S %d-%m-%Y",
)

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    register_handlers()
    await register_helpers()

    scheduler.add_job(
        disk_cleanup,
        trigger="interval",
        seconds=app_config.cleanup.cleanup_interval,
        id="disk_cleanup_task",
        replace_existing=True,
    )
    scheduler.start()

    # Restore queued requests
    for db_entry in requests_repository.get_pending_requests():
        await global_requests_handler.add_request(*db_entry)

    asyncio.create_task(status_subscriber.broadcast())
    asyncio.create_task(global_requests_handler.start())
    yield

    scheduler.shutdown()
    # TODO: Await current request completion?
    # if not app_config.dev_mode:
    #    await global_requests_handler.queue.join()
    db_connection.close()
    await status_subscriber.unsub_and_close()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    app.openapi_schema = OPENAPI_SCHEMA
    return app.openapi_schema


app: FastAPI = FastAPI(lifespan=lifespan)
app.openapi = custom_openapi

if app_config.dev_mode:
    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )

app_router: APIRouter = APIRouter()
app_router.include_router(requests_router)
app_router.include_router(request_status_router)
app_router.include_router(download_router, prefix="/download")

app.include_router(app_router, prefix="/api/v1")
