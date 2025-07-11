from pathlib import Path
from typing import Self

import yaml
from pydantic import Field

from backend.src.config.schemas.base_enum_model import BaseEnumModel
from backend.src.config.schemas.cleanup import CleanupSchema
from backend.src.config.schemas.ffmpeg import FFMPEGProperties
from backend.src.config.schemas.summary import SummarySchema
from backend.src.config.schemas.transcription import TranscriptionSchema
from backend.src.config.schemas.websockets import WebsocketsSchema
from backend.src.utils import get_logger_by_filepath

logger = get_logger_by_filepath(__file__)

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class ConfigParser(BaseEnumModel):
    dev_mode: bool = Field(default=False)
    show_ffmpeg_commands: bool = Field(default=False)
    allow_local_files: bool = Field(default=False)
    file_read_chunk_size: int = Field(default=8192)
    requests_queue_size: int = Field(default=10)
    ffmpeg: FFMPEGProperties = Field(default_factory=FFMPEGProperties)
    transcription: TranscriptionSchema = Field(default_factory=TranscriptionSchema)
    summary: SummarySchema = Field(default_factory=SummarySchema)
    cleanup: CleanupSchema = Field(default_factory=CleanupSchema)
    websockets: WebsocketsSchema = Field(default_factory=WebsocketsSchema)

    def model_save_yaml(self, save_path: Path) -> None:
        with open(save_path, "w", encoding="UTF-8") as f:
            f.write(yaml.dump(self.model_dump()))

    @classmethod
    def from_yaml(cls, config_path: Path) -> Self:
        # Create config with default values if not present
        if not config_path.is_file():
            logger.info("Config not found. Using default values")
            ConfigParser().model_save_yaml(config_path)
        if config_path.is_file() and config_path.suffix != ".yaml":
            raise FileNotFoundError("Config must have .yaml extension")

        with open(config_path, encoding="UTF-8") as config_file:
            logger.info("Config loaded!")
            data = yaml.load(config_file, Loader)
        return cls.model_validate(data)
