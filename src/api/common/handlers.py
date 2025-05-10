from src.api.request_helpers.GigachatHelper import GigachatHelper
from src.api.request_helpers.HelpersHandler import HelpersHandler
from src.api.common.services.GlobalRequestHandler import GlobalRequestsHandler
from src.api.request_helpers.YaDiskHelper import YaDiskHelper
from src.api.request_helpers.TranscriptionHelper import TranscriptionHelper

from src.api.video.services import *

global_requests_handler: GlobalRequestsHandler = GlobalRequestsHandler(HelpersHandler())

async def register_video_helpers():
    await global_requests_handler.register_request_helper(YaDiskHelper())
    await global_requests_handler.register_request_helper(GigachatHelper())
    await global_requests_handler.register_request_helper(TranscriptionHelper())

def register_video_handlers():
    global_requests_handler.register_request_handler(VideoCompression())
    global_requests_handler.register_request_handler(VideoAudioExtraction())
    global_requests_handler.register_request_handler(VideoTranscription())
    global_requests_handler.register_request_handler(VideoSummarization())
