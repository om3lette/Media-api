from backend.src.config.config_parser import ConfigParser
from backend.src.constants import CONFIG_PATH

app_config: ConfigParser = ConfigParser.from_yaml(CONFIG_PATH)
