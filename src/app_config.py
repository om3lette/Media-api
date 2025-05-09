from src.config.ConfigParser import ConfigParser
from src.constants import CONFIG_PATH

app_config: ConfigParser = ConfigParser.from_yaml(CONFIG_PATH)
