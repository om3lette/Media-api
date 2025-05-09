from src.config.ConfigParser import ConfigParser
from src.config.schemas.default_system_prompt import SYSTEM_PROMPT
from src.constants import CONFIG_PATH

app_config: ConfigParser = ConfigParser.from_yaml(CONFIG_PATH)
