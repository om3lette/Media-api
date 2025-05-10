from src.config.ConfigParser import ConfigParser


class BaseHelper:
    def __init__(self, name: str):
        self.name = name

    async def init(self, app_config: ConfigParser) -> None:
        return
