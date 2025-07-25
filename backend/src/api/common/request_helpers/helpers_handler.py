from backend.src.api.common.request_helpers.base_helper import BaseHelper
from backend.src.app_config import app_config
from backend.src.utils import get_logger_by_filepath

logger = get_logger_by_filepath(__file__)


class HelpersHandler:
    def __init__(self):
        self._helpers: list[BaseHelper] = []

    async def register_helper(self, helper: BaseHelper):
        self._helpers.append(helper)
        await helper.init(app_config)

    def get_helper_by_name(self, name: str):
        for helper in self._helpers:
            if helper.name == name:
                return helper
        raise NameError(f"{name} helper not found")
