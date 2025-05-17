from pathlib import Path

from gigachat import GigaChat
from gigachat.models import Messages, MessagesRole, Chat

from src.api.common.enums import RequestHelpersNames
from src.api.common.request_helpers.base_helper import BaseHelper
from src.api.common.utils import get_summary_filename
from src.api.video.schemas.requests.summarize import SummarizeConfig
from src.app_config import app_config
from src.config.enums import GigachatModels
from src.config.schemas.default_system_prompt import SYSTEM_PROMPT
from src.utils import get_logger_from_filepath

logger = get_logger_from_filepath(__file__)


class GigachatHelper(BaseHelper):
    def __init__(self):
        super().__init__(RequestHelpersNames.GIGACHAT)

    async def init(self, _):
        logger.info("Using %s", app_config.summary.model)

    @staticmethod
    def _assemble_user_query(transcription_path: Path):
        with open(transcription_path, "r", encoding="UTF-8") as f:
            return (
                "Предоставь краткое содержание следующего текстового файла/текста:\n"
                + f.read()
            )

    @staticmethod
    def _write_output(transcription_path: Path, content: str):
        with open(
            transcription_path.parent / get_summary_filename(), "w", encoding="UTF-8"
        ) as f:
            f.write(content)

    async def summarize(self, config: SummarizeConfig, transcription_path: Path):
        if app_config.summary.gigachat_api_token in [None, "", "<YOUR_TOKEN>"]:
            self._write_output(transcription_path, "Api token was not provided")
            return
        with GigaChat(
            credentials=app_config.summary.gigachat_api_token,
            model=config.summary.model
            if not app_config.dev_mode
            else GigachatModels.LITE,
            scope=app_config.summary.scope,
            verify_ssl_certs=False,
        ) as giga:
            messages: list[Messages] = [
                Messages(role=MessagesRole.SYSTEM, content=SYSTEM_PROMPT),
                Messages(
                    role=MessagesRole.USER,
                    content=self._assemble_user_query(transcription_path),
                ),
            ]
            chat = Chat(messages=messages)
            response = await giga.achat(chat)
            self._write_output(transcription_path, response.choices[0].message.content)
