# Overview

This python package runs simple telegram bot. Current functionality:

- [x] `Antispam`: Bot will block any user who will send message to chat with words from list `banned_phrases` in `config.yaml`. 
  - [x] `/ban` command: If someone replies some message with `/ban` command,  bot will run the same check. You can run `/ban_add <phrase>` to add some phrase from the sus message to the list of banned phrases, and after successfull poll, reply to sus message with `/ban`. Now bot will detect banned phrase in sus message and will ban the user.
  - [x] `/ban_add` command: `/ban_add <phrase>` starts poll to add the `phrase` to the list of banned phrases. Count of voters defined in `config.yaml` file, for more details please check `README.md` in config repository. If poll decision will be to add phrase to the list, bot will save new list and push changes to the config repository.
- [x] `Chat join approval`: If some user will send request to join the chat, bot will automatically approve it. If `bot` will send request to join the chat, it will be declined.


# Installation

## Prerequisites

### Telegram bot

In order to run the bot, you will need to [create and obtain bot token][2] using BotFather.

### make

In order to run the bot you need `make` command. It's not mandatory, you still can trigger it using python directly, but for simplification `Makefile` is prepared.

If you don't have `make` command, you can install it using your package manager, for example:

```
sudo dnf install -y make
```

### git 

Bot configuration file is stored in a separate repository (check `.gitmodules`) and accessed using git submodules.
Bot can update it's configuration file and then push these changes to the repo. Also it's periodically checks for latest updates from repository.

If you don't have `git` command, you can install it using your package manager, for example:

```
sudo dnf install -y git
```

But in order to keep your changes separately, you will need to create your own repository with `config.yaml` file, and update git submodules to sync `config/` to your repository. Also you need to configure your system (git ssh keys), so than bot can push changes to that repository.

### mise

In order to manage python version, [mise][1] is used. You can install it using `make`:

```
make prepare
```

This will update your PATH variable in `~/.bash_profile`, so you will need to reload it:

```
source ~/.bash_profile
```


# How to run

To run the bot:

```
make TOKEN='<BOT_TOKEN>'
```

You also can use environment variable `TELEGRAM_TOKEN`:

```
export TELEGRAM_TOKEN='<BOT_TOKEN>'
make
```


[1]: https://mise.jdx.dev/
[2]: https://core.telegram.org/bots/tutorial#obtain-your-bot-token