import os
import logging
import yaml

from typing import Self
from pathlib import Path
from pydantic import Field

from src.config.schemas.BaseEnumModel import BaseEnumModel
from src.config.schemas.ffmpeg import FFMPEGProperties
from src.config.schemas.transcription import TranscriptionSchema

logger = logging.getLogger(os.path.basename(__file__))

try:
	from yaml import CLoader as Loader
except ImportError:
	from yaml import Loader


class ConfigParser(BaseEnumModel):
	ffmpeg: FFMPEGProperties = Field(default_factory=FFMPEGProperties)
	transcription: TranscriptionSchema = Field(default_factory=TranscriptionSchema)
	dev_mode: bool = Field(default=False)

	def model_save_yaml(self, save_path: Path) -> None:
		with open(save_path, "w") as f:
			f.write(yaml.dump(self.model_dump()))

	@classmethod
	def from_yaml(cls, config_path: Path) -> Self:
		# Create config with default values if not present
		if not config_path.is_file():
			logger.info("Config not found. Using default values")
			ConfigParser().model_save_yaml(config_path)
		if config_path.is_file() and config_path.suffix != ".yaml":
			raise FileNotFoundError(f"Config must have .yaml extension")

		with open(config_path, "r") as config_file:
			logger.info("Config loaded!")
			data = yaml.load(config_file, Loader)
		return cls.model_validate(data)
