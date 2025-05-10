from src.api.common.file_helpers import UploadFileHelper
from src.api.common.request_helpers.GigachatHelper import GigachatHelper
from src.api.common.services.GlobalRequestHandler import GlobalRequestsHandler
from src.api.common.file_helpers.YaDiskHelper import YaDiskHelper
from src.api.common.request_helpers import TranscriptionHelper

import src.api.video.services as video_services

global_requests_handler: GlobalRequestsHandler = GlobalRequestsHandler()


async def register_helpers():
    await global_requests_handler.register_request_helper(GigachatHelper())
    await global_requests_handler.register_request_helper(TranscriptionHelper())

    await global_requests_handler.register_file_helper(YaDiskHelper())
    await global_requests_handler.register_file_helper(UploadFileHelper())


def register_handlers():
    global_requests_handler.register_request_handler(video_services.Compression())
    global_requests_handler.register_request_handler(video_services.AudioExtraction())
    global_requests_handler.register_request_handler(video_services.Transcription())
    global_requests_handler.register_request_handler(video_services.Summarization())
