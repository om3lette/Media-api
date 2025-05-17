from typing import Union

from src.api.audio.enums import AudioRequestType
from src.api.video.enums import VideoRequestType

RequestType = Union[VideoRequestType, AudioRequestType]
