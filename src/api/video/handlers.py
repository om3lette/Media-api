from src.api.video.services.VideoHandler import VideoRequestsHandler
from src.api.video.services.YaDiskHelper import YaDiskHelper
from src.pipeline.transcription.Transcriber import Transcriber

ya_disk_helper: YaDiskHelper = YaDiskHelper()
audio_helper: Transcriber = Transcriber()
video_requests_handler: VideoRequestsHandler = VideoRequestsHandler(ya_disk_helper, audio_helper)
