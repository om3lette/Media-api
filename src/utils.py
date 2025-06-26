import logging
import os

ffmpeg_logger = logging.getLogger("ffmpeg_runner")


def get_logger_by_filepath(filepath: os.PathLike):
    return logging.getLogger(os.path.basename(filepath))
