from src.api.request_helpers.BaseHelper import BaseHelper
from src.api.video.services.request_handlers.BaseHandler import BaseHandler
from .Compress import CompressRequestSchema

VideoRequest = CompressRequestSchema

RequestHandler = BaseHandler
RequestHelper = BaseHelper