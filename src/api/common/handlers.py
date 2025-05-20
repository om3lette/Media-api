from src.api.common.file_helpers import UploadFileHelper
from src.api.common.file_helpers.ya_disk_helper import YaDiskHelper
from src.api.common.request_helpers.gigachat_helper import GigachatHelper
from src.api.common.request_helpers.tesseract_helper import TesseractHelper
from src.api.common.request_helpers.transcription_helper import TranscriptionHelper
from src.api.common.services.global_request_handler import GlobalRequestsHandler
from src.api.tasks_handlers.audio.custom import CustomAudioHandler
from src.api.tasks_handlers.audio.summarize import SummarizeAudioHandler
from src.api.tasks_handlers.audio.transcribe import TranscriptionAudioHandler
from src.api.tasks_handlers.common.extract_audio import ExtractAudioHandler
from src.api.tasks_handlers.image.custom import CustomImageHandler
from src.api.tasks_handlers.image.image_to_text import ImageToTextHandler
from src.api.tasks_handlers.video.compress import CompressVideoHandler
from src.api.tasks_handlers.video.custom import CustomVideoHandler
from src.api.tasks_handlers.video.summarize import SummarizeVideoHandler
from src.api.tasks_handlers.video.transcribe import TranscriptionVideoHandler

task_handlers = [
    ExtractAudioHandler,
    SummarizeVideoHandler,
    TranscriptionVideoHandler,
    CompressVideoHandler,
    CustomVideoHandler,
    TranscriptionAudioHandler,
    SummarizeAudioHandler,
    CustomAudioHandler,
    ImageToTextHandler,
    CustomImageHandler,
]

request_helpers: list = [GigachatHelper, TranscriptionHelper, TesseractHelper]
file_helpers: list = [YaDiskHelper, UploadFileHelper]

global_requests_handler: GlobalRequestsHandler = GlobalRequestsHandler()


async def register_helpers():
    for request_helper in request_helpers:
        await global_requests_handler.register_request_helper(request_helper())

    for file_helper in file_helpers:
        await global_requests_handler.register_file_helper(file_helper())


def register_handlers():
    for task_handler in task_handlers:
        global_requests_handler.register_request_handler(task_handler())
