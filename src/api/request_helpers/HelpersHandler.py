import logging
import os

from src.api.video.schemas.requests.types import RequestHelper
from src.app_config import app_config

logger = logging.getLogger(os.path.basename(__file__))

class HelpersHandler:
    def __init__(self):
        self._helpers: list[RequestHelper] = []

    async def register_helper(self, helper: RequestHelper):
        self._helpers.append(helper)
        await helper.init(app_config)

    def get_helper_by_name(self, name: str):
        for helper in self._helpers:
            if helper.name == name:
                return helper
        raise NameError(f"{name} helper not found")
