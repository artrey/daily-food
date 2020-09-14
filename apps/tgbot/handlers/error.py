import html
import json
import logging
import traceback

from django.conf import settings
from telegram import Update, ParseMode
from telegram.ext import CallbackContext


logger = logging.getLogger(__name__)


def error(update: Update, context: CallbackContext):
    """Log the error and send a telegram message to notify the developer."""

    # Log the error before we do anything else,
    # so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:",
                 exc_info=context.error)

    # traceback.format_exception returns the usual python message about
    # an exception, but as a list of strings rather than a single string,
    # so we have to join them together.
    tb_list = traceback.format_exception(None, context.error,
                                         context.error.__traceback__)
    tb = ''.join(tb_list)

    # Build the message with some markup and additional information
    # about what happened. You might need to add some logic to deal with
    # messages longer than the 4096 character limit.
    message = (
        'An exception was raised while handling an update\n'
        '<pre>update = {}</pre>\n\n'
        '<pre>context.chat_data = {}</pre>\n\n'
        '<pre>context.user_data = {}</pre>\n\n'
        '<pre>{}</pre>'
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(str(context.chat_data)),
        html.escape(str(context.user_data)),
        html.escape(tb)
    )[:4096]

    # Finally, send the message
    context.bot.send_message(chat_id=settings.TG_DEVELOPER_CHAT_ID,
                             text=message, parse_mode=ParseMode.HTML)
