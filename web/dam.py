#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import re

import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, message
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

ACTION, DELETE = range(2)


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['Create', 'Delete']]

    update.message.reply_text(
        'Send /cancel to stop talking to me.\n\n'
        'Do you wnt to create or delete a license?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Create or Delete'
        ),
    )

    return ACTION


def choice(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    choice = update.message.text.lower().strip()
    if choice == "delete":
        update.message.reply_text(
            "Please enter the license key to delete")
        return DELETE
    data = requests.post("https://auttg.pythonanywhere.com/create/", data={"hash":"axios"})
    key: dict = data.json()
    key = key.get("key")
    if key:
        update.message.reply_text("You have created a new License!\nKey: %s"%key)
    return ConversationHandler.END


def delete(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    key = update.message.text
    res: dict = requests.post("https://auttg.pythonanywhere.com/delete/", data={"key": key}).json()
    if res.get("success"):
        update.message.reply_text(
            "You have successfully deleted a license\nKey: %s" % res.get("success"))
    else:
        update.message.reply_text(
            "An error occured\nError: %s" % res.get("error"))
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5239920253:AAH6hlmCKanjo8SLR-dbcJTB99j2hg-Bh4k")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ACTION: [MessageHandler(Filters.regex('^(Create|Delete)$'), choice)],
            DELETE: [MessageHandler(Filters.text, delete)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
