from src.config.ConfigParser import ConfigParser
from src.constants import CONFIG_PATH
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%H:%M:%S %d-%m-%Y"
)

app_config: ConfigParser = ConfigParser.from_yaml(CONFIG_PATH)
