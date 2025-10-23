import logging
from telegram import Update
from telegram.ext import ContextTypes

from simple_tgbot.src.bot_config import bot_config

logger = logging.getLogger(__name__)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Prints help message"""
    from simple_tgbot.src.commands.commands import bot_commands

    help_message = create_formatted_help_message(bot_commands)

    await update.message.reply_html(help_message, disable_web_page_preview=True)


def create_formatted_help_message(bot_commands):
    """Generates a visually appealing and informative help message for the Telegram bot.

    Args:
        bot_commands (dict): A dictionary mapping command names (strings) to their
                             corresponding callback functions.

    Returns:
        str: The formatted help message with bold commands, brief descriptions, and
             appropriate spacing.
    """

    help_message = "<b>Available Commands</b>\n\n"

    for command_aliases, callback in bot_commands.items():
        # Handle command aliases (single string or tuple)
        if isinstance(command_aliases, str):
            command_name = command_aliases
        else:
            command_name = ", /".join(command_aliases)  # Join tuple elements with "/"

        # Extract the first sentence from the docstring for a concise description
        description = callback.__doc__.splitlines()[0] if callback.__doc__ else ""
        help_message += f"<b>/{command_name}</b> - {description}\n"

    if bot_config.print_help_footer:
        help_message += f"\n-----\n{bot_config.footer}"

    return help_message
