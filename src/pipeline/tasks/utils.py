import asyncio
from pathlib import Path

import ffmpeg
from tqdm import tqdm

from src.pipeline.schemas.ffmpeg_progress import FFMPEGProgressSchema

from src.pipeline.schemas.streams import StreamsSchema
from src.pipeline.types import RenderConfig
from src.utils import ffmpeg_logger


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


def display_progress(
    progress_bar: tqdm, progress: FFMPEGProgressSchema, input_duration
):
    percentage: float = (progress.out_time.total_seconds() / input_duration) * 100
    progress_bar.update(int(percentage))


async def ffmpeg_run(
    input_file_path: Path,
    stream: ffmpeg.nodes.OutputStream,
    on_progress=display_progress,
    show_cmd=False,
):
    # Convert to command list
    cmd = stream.compile()
    cmd += ["-progress", "pipe:2", "-loglevel", "warning"]
    if show_cmd:
        ffmpeg_logger.info("Running: %s", " ".join(list(map(str, cmd))))
    # Run ffmpeg as subprocess
    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE
    )

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
        if key != "progress" or not on_progress:
            continue
        on_progress(
            progress_bar,
            FFMPEGProgressSchema.model_validate(progress_dict),
            input_duration,
        )
        if value == "end":
            break

    return_code = await process.wait()
    progress_bar.close()
    if return_code != 0:
        raise RuntimeError(f"FFmpeg failed with return code {return_code}")
