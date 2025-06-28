from backend.src.api.common.file_helpers import UploadFileHelper
from backend.src.api.common.file_helpers.local_file_helper import LocalFileHelper
from backend.src.api.common.file_helpers.ya_disk_helper import YaDiskHelper
from backend.src.api.common.request_helpers.gigachat_helper import GigachatHelper
from backend.src.api.common.request_helpers.tesseract_helper import TesseractHelper
from backend.src.api.common.request_helpers.transcription_helper import TranscriptionHelper
from backend.src.api.common.services.global_request_handler import GlobalRequestsHandler
from backend.src.api.tasks_handlers.audio.custom import CustomAudioHandler
from backend.src.api.tasks_handlers.audio.summarize import SummarizeAudioHandler
from backend.src.api.tasks_handlers.audio.transcribe import TranscriptionAudioHandler
from backend.src.api.tasks_handlers.common.extract_audio import ExtractAudioHandler
from backend.src.api.tasks_handlers.image.custom import CustomImageHandler
from backend.src.api.tasks_handlers.image.image_to_text import ImageToTextHandler
from backend.src.api.tasks_handlers.text.custom import CustomTextHandler
from backend.src.api.tasks_handlers.text.summarize import SummarizeTextHandler
from backend.src.api.tasks_handlers.video.compress import CompressVideoHandler
from backend.src.api.tasks_handlers.video.custom import CustomVideoHandler
from backend.src.api.tasks_handlers.video.summarize import SummarizeVideoHandler
from backend.src.api.tasks_handlers.video.transcribe import TranscriptionVideoHandler

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
    SummarizeTextHandler,
    CustomTextHandler,
]

request_helpers: list = [GigachatHelper, TranscriptionHelper, TesseractHelper]
file_helpers: list = [YaDiskHelper, UploadFileHelper, LocalFileHelper]

global_requests_handler: GlobalRequestsHandler = GlobalRequestsHandler()


async def register_helpers():
    for request_helper in request_helpers:
        await global_requests_handler.register_request_helper(request_helper())

    for file_helper in file_helpers:
        await global_requests_handler.register_file_helper(file_helper())


def register_handlers():
    for task_handler in task_handlers:
        global_requests_handler.register_request_handler(task_handler())
