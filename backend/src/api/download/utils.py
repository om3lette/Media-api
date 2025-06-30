from pathlib import Path

from fastapi import HTTPException
from starlette.responses import FileResponse, Response, JSONResponse

from backend.src.api.common.io_handlers import requests_repository


def download_request_wrapper(request_id: str, path_builder, response_constructor):
    is_ready, is_present = requests_repository.is_download_ready(request_id)

    if not is_present:
        raise HTTPException(status_code=404)
    if not is_ready:
        return Response(status_code=202)

    target_path: Path = path_builder(request_id)

    if not target_path.is_file():
        raise HTTPException(status_code=404)

    return response_constructor(target_path)


def file_response_builder(file: Path):
    return FileResponse(
        file,
        filename=file.name,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{file.name}"'},
    )


def json_response_builder(file: Path):
    with open(file, "r", encoding="UTF-8") as f:
        return JSONResponse(content={"content": f.read()})
