from src.api.common.file_helpers import UploadFileHelper
from src.api.common.request_helpers.gigachat_helper import GigachatHelper
from src.api.common.services.global_request_handler import GlobalRequestsHandler
from src.api.common.file_helpers.ya_disk_helper import YaDiskHelper
from src.api.common.request_helpers.transcription_helper import TranscriptionHelper

from src.api.tasks_handlers.common.extract_audio import ExtractAudioHandler

from src.api.tasks_handlers.audio.summarize import SummarizeAudioHandler
from src.api.tasks_handlers.audio.transcribe import TranscriptionAudioHandler

from src.api.tasks_handlers.video.summarize import SummarizeVideoHandler
from src.api.tasks_handlers.video.transcribe import TranscriptionVideoHandler
from src.api.tasks_handlers.video.compress import CompressVideoHandler
from src.api.tasks_handlers.video.custom import CustomVideoHandler

task_handlers = [
    ExtractAudioHandler,
    SummarizeVideoHandler,
    TranscriptionVideoHandler,
    CompressVideoHandler,
    CustomVideoHandler,
    TranscriptionAudioHandler,
    SummarizeAudioHandler,
]

global_requests_handler: GlobalRequestsHandler = GlobalRequestsHandler()


async def register_helpers():
    await global_requests_handler.register_request_helper(GigachatHelper())
    await global_requests_handler.register_request_helper(TranscriptionHelper())

    await global_requests_handler.register_file_helper(YaDiskHelper())
    await global_requests_handler.register_file_helper(UploadFileHelper())


def register_handlers():
    for task_handler in task_handlers:
        global_requests_handler.register_request_handler(task_handler())
