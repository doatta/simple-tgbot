from telegram import Update, Message
from telegram.ext import ContextTypes


# Ban logic
async def ban(message: Message, phrase):
    user_to_ban = message.from_user
    await message.chat.ban_member(user_to_ban.id)
    await message.reply_text(f"User @{user_to_ban.username} banned. Reason: {phrase}")
    await message.delete()


# Define a `/ban` command handler.
async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    from simple_tgbot.src.messages import check_message

    """Replies to ban"""
    if not update.message.reply_to_message or not update.message.reply_to_message.text:
        await update.message.reply_text("Reply to sus message with /ban")
    if await check_message(update.message.reply_to_message):
        await update.message.set_reaction(reaction="❤")
    else:
        await update.message.reply_text("Not sus")
