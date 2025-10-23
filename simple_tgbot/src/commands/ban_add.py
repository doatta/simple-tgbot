from datetime import datetime, timedelta
import logging
from telegram import Update, Message
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from simple_tgbot.src.bot_config import bot_config

logger = logging.getLogger(__name__)


# Define a `/ban` command handler.
async def ban_add_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bot will start a new poll to add phrase to the banned list. If members of chat will reply 'Yes' (count depends on configuration), bot will ban the phrase. Example: /ban_add hello"""
    from simple_tgbot.src.commands.commands import bot_commands

    if not update.message or not update.message.text:
        return

    if update.message.text == f"/ban_add":
        list_of_banned_phrases = "\n- " + "\n- ".join(bot_config.banned_phrases)
        await update.message.reply_text(
            f"{ban_add_command.__doc__}. List of currently banned phrases: {list_of_banned_phrases}"
        )
        return

    phrase_to_ban = update.message.text.replace(f"/ban_add ", "")

    if phrase_to_ban.strip().lower() in bot_config.banned_phrases:
        await update.message.reply_text(f"{phrase_to_ban} is already in banned list")
        return

    NO_BAN_PHRASES: list[str] = []
    for command, _ in bot_commands.items():
        if isinstance(command, tuple):
            NO_BAN_PHRASES.extend(list(command))
            continue
        NO_BAN_PHRASES.append(command)

    if phrase_to_ban.strip().lower() in [
        phrase.strip().lower() for phrase in NO_BAN_PHRASES
    ]:
        await update.message.reply_text("Banning this phrase is prohibited")
        return

    question = f'Ban phrase "{phrase_to_ban}"? \nMinimum count of "Yes" - {bot_config.ban_add_poll_results.yes_minimum_count}. Maximum count for "No" - {bot_config.ban_add_poll_results.no_maximum_count}'
    options = ["Yes", "No"]
    message: Message = await context.bot.send_poll(
        chat_id=update.message.chat_id,
        question=question,
        options=options,
        is_anonymous=False,
        close_date=datetime.now() + timedelta(minutes=2),
    )

    # Save some info about the poll the bot_data for later use in receive_poll_answer
    payload = {
        message.poll.id: {
            "options": options,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
            "phrase_to_ban": phrase_to_ban,
            "yes": 0,
            "no": 0,
        }
    }
    context.bot_data.update(payload)


async def poll_answers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle poll answers.
    This function is called when a user votes in a poll.
    """
    answered_poll = context.bot_data[update.poll_answer.poll_id]
    chat_id = answered_poll["chat_id"]
    phrase_to_ban = answered_poll["phrase_to_ban"]

    try:
        options = answered_poll["options"]
    # this means this poll answer update is from an old poll, we can't do our answering then
    except KeyError:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Sorry, this poll is outdated. Please create new request",
        )
        return

    selected_options = update.poll_answer.option_ids
    for option_id in selected_options:
        if options[option_id] == "Yes":
            answered_poll["yes"] += 1
        elif options[option_id] == "No":
            answered_poll["no"] += 1

    yes_count: int = answered_poll["yes"]
    no_count: int = answered_poll["no"]

    if (
        yes_count >= bot_config.ban_add_poll_results.yes_minimum_count
        and no_count < bot_config.ban_add_poll_results.no_maximum_count
    ):
        bot_config.add_banned_phrase(phrase_to_ban)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Ban phrase {phrase_to_ban} added. New list of banned phrases: {bot_config.banned_phrases}. Now you can reply to sus message with /ban",
        )
        # In small groups when everyone votes, poll automatically completes
        try:
            await context.bot.stop_poll(chat_id, update.poll_answer.poll_id)
        except BadRequest:
            pass
        del context.bot_data[update.poll_answer.poll_id]
        return
    elif no_count >= bot_config.ban_add_poll_results.no_maximum_count:
        await context.bot.send_message(
            chat_id=chat_id, text=f"Phrase {phrase_to_ban} not added to the ban list"
        )
        try:
            await context.bot.stop_poll(chat_id, update.poll_answer.poll_id)
        except BadRequest:
            pass
        del context.bot_data[update.poll_answer.poll_id]
        return
