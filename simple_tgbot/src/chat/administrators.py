import datetime
import logging
from threading import Timer
from typing import Any, Coroutine, Tuple
from telegram import ChatMember, Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


class ChatAdministrators:
    def get_chat_administrators(chat_id, context: ContextTypes.DEFAULT_TYPE) -> list:
        """
        Returns chat administrators from cache
        """
        if context.chat_data:
            return context.chat_data.get("administrators", [])
        return []

    async def update_chat_administrators(
        chat_id: int, chat_title: str, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        If chat administrators are not cached, get them from Telegram API
        If cache was created more than 10 minutes ago, also update cache
        """

        # Check time difference between last check and now
        if context.chat_data:
            checked_time: datetime.datetime = context.chat_data.get(
                "checked_time", datetime.datetime.time(0, 0)
            )
            current_time = datetime.datetime.now(datetime.timezone.utc)
            time_diff = (current_time - checked_time).total_seconds() / 60
            logger.error(time_diff)
            if time_diff < 0:
                time_diff += 24 * 60

            # If time difference is less than 10 minutes, return cached administrators
            if time_diff < 10:
                return
        administrators = await context.bot.get_chat_administrators(chat_id)
        ChatAdministrators.save_chat_administrators(
            chat_id, chat_title, administrators, context
        )

        # Get updates once in a 10 minutes
        Timer(
            interval=600.0,
            function=await ChatAdministrators.update_chat_administrators(
                chat_id, chat_title, context
            ),
        ).start()
        return

    def save_chat_administrators(
        chat_id: int,
        chat_title: str,
        administrators: Coroutine[Any, Any, Tuple[ChatMember, ...]],
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """
        Saves chat administrators to cache
        """
        payload = {
            "title": chat_title,
            "administrators": administrators,
            "checked_time": datetime.datetime.now(datetime.timezone.utc),
        }
        context.chat_data.update(payload)
