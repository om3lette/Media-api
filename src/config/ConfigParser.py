from typing import Self
from pathlib import Path
from pydantic import Field

import yaml

from src.config.schemas.BaseEnumModel import BaseEnumModel
from src.config.schemas.ffmpeg import FFMPEGProperties
from src.config.schemas.summary import SummarySchema
from src.config.schemas.transcription import TranscriptionSchema
from src.utils import get_logger_from_filepath

logger = get_logger_from_filepath(__file__)

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class ConfigParser(BaseEnumModel):
    dev_mode: bool = Field(default=False)
    file_read_chunk_size: int = Field(default=8192)
    ffmpeg: FFMPEGProperties = Field(default_factory=FFMPEGProperties)
    transcription: TranscriptionSchema = Field(default_factory=TranscriptionSchema)
    summary: SummarySchema = Field(default_factory=SummarySchema)

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

        with open(config_path, "r", encoding="UTF-8") as config_file:
            logger.info("Config loaded!")
            data = yaml.load(config_file, Loader)
        return cls.model_validate(data)
