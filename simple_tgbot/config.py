import logging
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)
CONFIG_FILE = "config.yaml"


class ConfigFile:
    def __init__(self, file_path: Path) -> None:
        try:
            with open(file_path, "r") as f:
                config_data = yaml.safe_load(f)
        except (FileNotFoundError, yaml.YAMLError) as error:
            logger.error("Error loading config file: %s", error)
            return None

        self.banned_phrases = config_data.get("banned_phrases", [])

    banned_phrases: list[str]


config = ConfigFile(CONFIG_FILE)
