import logging
from telegram import Update, Message
from telegram.ext import ContextTypes

from simple_tgbot.config import config
from telegram.error import BadRequest

logger = logging.getLogger(__name__)

administrators = []


# Check all messages
async def messages_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Defines the logic of checks for all incoming messages
    """

    if not update.message or not update.message.text:
        return
    await check_message(update.message)


async def check_message(message: Message) -> bool:
    """
    Checks each message
    """
    from simple_tgbot.src.ban import ban

    # Ignore administrators messages
    global administrators
    try:
        if not administrators:
            administrators = await message.chat.get_administrators()
    except BadRequest as error:
        if not error.message == "There are no administrators in the private chat":
            logger.error(error)

    if await message.chat.get_member(message.from_user.id) in administrators:
        return
    if config.banned_phrases:
        for phrase in config.banned_phrases:
            if not phrase.lower() in message.text.lower():
                continue
            await ban(message, phrase)
            return True

    return False
