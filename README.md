# Overview

This python package runs simple telegram bot. Current functionality:

- [x] `Antispam`: Bot will block any user who will send message to chat with words from list `banned_phrases` in `config.yaml`. 
  - [] `/ban` command: If someone replies some message with `/ban` command,  bot will run the same check (to prevent users banning each user without any reason). For now it makes no sense, as bot checks all messages anyway. But in future some more complex logic might be introduced.
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