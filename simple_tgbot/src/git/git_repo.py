from enum import Enum
from git import Repo
import os


ChangeType = Enum("ChangeType", "BANNED_PHRASE_ADDED")


class BotRepo:
    def __init__(self) -> None:
        path_to_bot_repo = os.path.join(os.getcwd())
        self.repo = Repo(path_to_bot_repo)


class ConfigRepo:
    def __init__(self) -> None:
        path_to_config_repo = os.path.join(os.getcwd(), "config")
        self.repo = Repo(path_to_config_repo)

    def push_changes(self, change: dict) -> None:
        commit_message = "Update config: "
        match change["change_type"]:
            case ChangeType.BANNED_PHRASE_ADDED:
                commit_message += "added banned phrase"
                commit_message += f"\n\nNew banned phrase: {change['phrase']}"
            case _:
                commit_message += "unknown change type"
        self.repo.git.add(all=True)
        self.repo.git.commit("-m", commit_message)
        self.repo.git.push()


bot_repo = BotRepo()
config_repo = ConfigRepo()
