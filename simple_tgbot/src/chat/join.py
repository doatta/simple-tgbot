from telegram import Update
from telegram.ext import ContextTypes


async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.is_bot:
        await update.effective_chat.send_message(
            "Bot %s tried to join the group", update.effective_user.username
        )
        await context.bot.decline_chat_join_request(
            chat_id=update.effective_chat.id, user_id=update.effective_user.id
        )
        return
    await context.bot.approve_chat_join_request(
        chat_id=update.effective_chat.id, user_id=update.effective_user.id
    )
