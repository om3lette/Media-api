from src.api.request_helpers.HelpersHandler import HelpersHandler
from src.api.video.services.VideoHandler import VideoRequestsHandler
from src.api.request_helpers.YaDiskHelper import YaDiskHelper
from src.api.request_helpers.TranscriptionHelper import TranscriptionHelper
from src.api.video.services.request_handlers.Compress import CompressHandler
from src.api.video.services.request_handlers.CompressAndTranscribe import CompressAndTranscribeHandler

video_requests_handler: VideoRequestsHandler = VideoRequestsHandler(HelpersHandler())

async def register_video_helpers():
    await video_requests_handler.register_request_helper(YaDiskHelper())
    await video_requests_handler.register_request_helper(TranscriptionHelper())

def register_video_handlers():
    video_requests_handler.register_request_handler(CompressAndTranscribeHandler())
    video_requests_handler.register_request_handler(CompressHandler())
