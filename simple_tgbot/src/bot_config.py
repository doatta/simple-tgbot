from dataclasses import dataclass
import logging
from pathlib import Path
from threading import Timer
import yaml

logger = logging.getLogger(__name__)
CONFIG_FILE = "config/config.yaml"


class Dumper(yaml.Dumper):
    """
    Custom YAML dumper to make indentation more readable
    """

    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)


@dataclass
class BanAddPollResults:
    yes_minimum_count: int
    no_maximum_count: int


class BotConfig:
    from simple_tgbot.src.git.git_repo import ChangeType

    def __init__(self, file_path: Path) -> None:
        from simple_tgbot.src.git.git_repo import bot_repo, config_repo

        self.__bot_repo = bot_repo
        self.__config_repo = config_repo
        self.__file_path = file_path
        self.__bot_config: dict = {}
        self.__banned_phrases: list[str] = []
        self.__print_help_footer: bool = False
        self.__footer: str = ""
        self.__ban_add_poll_results: BanAddPollResults = BanAddPollResults(3, 2)
        self.get_updates()

    def get_updates(self) -> None:
        """
        Get latest commit from config repo
        Updates config file and updates values for phrases
        """
        for submodule in self.__bot_repo.repo.submodules:
            submodule.update(to_latest_revision=True)

        new_bot_config = self.load_config_file()

        if new_bot_config and new_bot_config == self.__bot_config:
            Timer(interval=600.0, function=self.get_updates).start()
            return

        self.__bot_config: dict = new_bot_config
        self.__banned_phrases = [
            phrase for phrase in self.__bot_config.get("banned_phrases", [])
        ]

        if self.__bot_config.get("footer") and self.__bot_config["footer"].get("print"):
            self.__print_help_footer = True
            self.__footer = self.__bot_config["footer"].get("text", "")

        if self.__bot_config.get("ban_add_poll_results"):
            self.__ban_add_poll_results = BanAddPollResults(
                self.__bot_config["ban_add_poll_results"].get("yes_minimum_count", 3),
                self.__bot_config["ban_add_poll_results"].get("no_maximum_count", 2),
            )

        # Get updates once in a 10 minutes
        Timer(interval=600.0, function=self.get_updates).start()

    def load_config_file(self) -> dict:
        try:
            with open(self.__file_path, "r") as f:
                return yaml.safe_load(f)
        except (FileNotFoundError, yaml.YAMLError) as error:
            logger.error("Error loading config file: %s", error)
            return None

    def save_config_file(self, change: dict) -> None:
        with open(self.__file_path, "w", encoding="utf-8") as f:
            yaml.dump(self.__bot_config, f, allow_unicode=True, Dumper=Dumper),
        self.__config_repo.push_changes(change)

    def add_banned_phrase(self, phrase: str) -> None:
        from simple_tgbot.src.git.git_repo import ChangeType

        if phrase.strip().lower() in self.banned_phrases:
            return
        logger.info("Adding banned phrase: %s", phrase)
        self.__banned_phrases.append(phrase)
        self.__bot_config["banned_phrases"] = self.__banned_phrases
        change = {"change_type": ChangeType.BANNED_PHRASE_ADDED, "phrase": phrase}
        self.save_config_file(change)

        return

    @property
    def banned_phrases(self) -> list[str]:
        return [phrase.strip().lower() for phrase in self.__banned_phrases]

    @property
    def ban_add_poll_results(self) -> BanAddPollResults:
        return self.__ban_add_poll_results

    @property
    def print_help_footer(self) -> bool:
        return self.__print_help_footer

    @property
    def footer(self) -> str:
        return self.__footer


bot_config = BotConfig(CONFIG_FILE)
