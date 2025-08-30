import asyncio
from datetime import datetime
from pathlib import Path

import ffmpeg
from tqdm import tqdm

from backend.src.app_config import app_config
from backend.src.pipeline.schemas.ffmpeg_progress import FFMPEGProgressSchema
from backend.src.pipeline.schemas.streams import StreamsSchema
from backend.src.pipeline.types import RenderConfig
from backend.src.pipeline.types.state_callbacks import UpdateProgressCb
from backend.src.utils import ffmpeg_logger


def get_streams_from_file(file_path: Path) -> StreamsSchema:
    ffmpeg_input = ffmpeg.input(file_path)
    return StreamsSchema(video=ffmpeg_input.video, audio=ffmpeg_input.audio)


def extract_config_by_field_name(
    extract_from: RenderConfig, field_name: str, config_type: type[RenderConfig]
) -> RenderConfig:
    if isinstance(extract_from, config_type):
        return extract_from
    if field_name in extract_from.model_fields:
        return getattr(extract_from, field_name)
    return config_type()


async def display_progress(
    progress_bar: tqdm,
    progress: FFMPEGProgressSchema,
    input_duration,
    last_progress_update: datetime.time,
    on_progress_cb: UpdateProgressCb = None,
) -> datetime.time:
    percentage: int = int((progress.out_time.total_seconds() / input_duration) * 100)
    progress_bar.update(percentage - progress_bar.n)

    seconds_since_last_update: int = int(
        (datetime.now() - last_progress_update).total_seconds()
    )
    if (
        not on_progress_cb
        or seconds_since_last_update < app_config.websockets.update_progress_interval
    ):
        return last_progress_update
    await on_progress_cb(percentage)
    return datetime.now()


async def ffmpeg_run(
    input_file_path: Path, stream: ffmpeg.nodes.OutputStream, on_progress_cb=None
):
    cmd = stream.compile()
    cmd += ["-progress", "pipe:2", "-loglevel", "warning"]
    if app_config.show_ffmpeg_commands:
        ffmpeg_logger.info("Running: %s", " ".join(list(map(str, cmd))))

    # Run ffmpeg as a subprocess
    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE
    )

    last_update_call: datetime.time = datetime.now()
    input_duration = float(ffmpeg.probe(str(input_file_path))["format"]["duration"])
    progress_dict = {}
    progress_bar = tqdm(total=100)
    # Parse structured progress from stderr
    while True:
        line = await process.stderr.readline()
        if not line:
            break
        decoded = line.decode().strip()

        split = decoded.split("=", 1)
        if len(split) < 2:
            ffmpeg_logger.error(split[0])
            continue
        key, value = split

        progress_dict[key] = value.strip()
        if key != "progress":
            continue
        last_update_call = await display_progress(
            progress_bar,
            FFMPEGProgressSchema.model_validate(progress_dict),
            input_duration,
            last_update_call,
            on_progress_cb,
        )
        if value == "end":
            break
    return_code = await process.wait()
    progress_bar.close()
    if return_code != 0:
        raise RuntimeError(f"FFmpeg failed with return code {return_code}")
