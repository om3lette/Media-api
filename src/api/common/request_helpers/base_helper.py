from src.config.config_parser import ConfigParser


class BaseHelper:
    def __init__(self, name: str):
        self.name = name

    async def init(self, app_config: ConfigParser) -> None:
        return
