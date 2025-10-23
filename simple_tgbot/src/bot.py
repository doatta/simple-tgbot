#!/usr/bin/env python

import argparse
import logging
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ChatJoinRequestHandler,
    filters,
    PollAnswerHandler,
)
from telegram.error import InvalidToken

from simple_tgbot.src.commands.commands import bot_commands
from simple_tgbot.src.commands.ban_add import poll_answers
from simple_tgbot.src.chat.join import join_request
from simple_tgbot.src.chat.messages import messages_flow

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run telegram bot")
    parser.add_argument(
        "--telegram-token",
        "-t",
        type=str,
        help="Telegram bot token",
        default=os.getenv("TELEGRAM_TOKEN"),
        required=False,
    )
    args = parser.parse_args()

    if not args.telegram_token:
        raise KeyError(
            "Please define ENV variable TELEGRAM_TOKEN,run script with parameter --telegram-token <token-value> or provide secret name with -s"
        )
    return args


def main() -> None:
    """Start the bot"""

    # Parse arguments
    args = parse_args()

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(args.telegram_token).build()

    # Handlers define what bot does
    for command, callback in bot_commands.items():
        application.add_handler(CommandHandler(command=command, callback=callback))
        logger.info(f"Registered handler for /{command}")
    application.add_handler(ChatJoinRequestHandler(join_request))
    application.add_handler(PollAnswerHandler(poll_answers))
    application.add_handler(MessageHandler(filters.ALL, messages_flow))

    # Start the bot
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except InvalidToken:
        logger.error("Invalid token")
        return


if __name__ == "__main__":
    main()
