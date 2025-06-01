from pathlib import Path

from fastapi import APIRouter, HTTPException
from starlette.responses import FileResponse

from src.constants import ARCHIVE_FORMAT, OUT_FOLDER

static_router: APIRouter = APIRouter()


@static_router.get("/download/")
async def output_browser(request_id: str):
    target_path: Path = (OUT_FOLDER / request_id).with_suffix(f".{ARCHIVE_FORMAT}")

    if target_path.is_file():
        return FileResponse(
            target_path,
            filename=target_path.name,
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f'attachment; filename="{target_path.name}"'
            },
        )
    raise HTTPException(status_code=400, detail="Invalid path")
