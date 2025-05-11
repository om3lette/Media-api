from typing import Union

from src.api.audio.enums import AudioRequestType
from src.api.video.enums import VideoRequestType

from src.api.common.file_helpers import BaseFileHelper
from src.api.common.request_helpers import BaseHelper
from src.api.common.services.BaseHandler import BaseHandler

RequestType = Union[VideoRequestType, AudioRequestType]

RequestHandler = BaseHandler
RequestHelper = BaseHelper

FileHelper = BaseFileHelper

