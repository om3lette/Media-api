from src.api.video.services.VideoHandler import VideoRequestsHandler
from src.api.video.services.YaDiskHelper import YaDiskHelper

ya_disk_helper: YaDiskHelper = YaDiskHelper()
video_requests_handler: VideoRequestsHandler = VideoRequestsHandler(ya_disk_helper)
