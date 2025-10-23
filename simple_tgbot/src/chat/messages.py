import logging
from telegram import Update, Message
from telegram.ext import ContextTypes

from simple_tgbot.src.bot_config import bot_config
from simple_tgbot.src.chat.administrators import ChatAdministrators

logger = logging.getLogger(__name__)


# Check all messages
async def messages_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Defines the logic of checks for all incoming messages
    """

    if not update.message or not update.message.text:
        return

    # Cache chat administrators
    # Execute just once, then Timer will start periodic updates
    if update.message.chat.type != "private" and not context.chat_data.get(
        "administrators"
    ):
        await ChatAdministrators.update_chat_administrators(
            update.effective_chat.id, update.effective_chat.title, context
        )

    await check_message(message=update.message, context=context)


async def check_message(message: Message, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Checks each message and ban for banned phrases
    Ignore chat administrators and bot itself
    """
    from simple_tgbot.src.commands.ban import ban

    if not message:
        return False

    administrators = ChatAdministrators.get_chat_administrators(
        message.chat_id, context
    )
    chat_member = await message.chat.get_member(message.from_user.id)
    if chat_member in administrators or chat_member == message.chat.get_bot():
        return

    if bot_config.banned_phrases:
        for phrase in bot_config.banned_phrases:
            if not phrase in message.text.strip().lower():
                continue
            await ban(message, phrase)
            return True

    return False
