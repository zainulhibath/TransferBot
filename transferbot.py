#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Description coming Soon
"""

from telegram.ext   import Updater, CommandHandler, MessageHandler
from telegram.ext   import Filters, CallbackQueryHandler
import logging
import re

# Enable logging
logging.basicConfig (format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger (__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def cmd_start (bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text ('Transferbot 0.1')


def cmd_help (bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text ('TODO /help')


def cmd_document (bot, update):
    """ TODO """
    update.message.reply_text ('Got ' + update.message.document.file_name)
    update.message.reply_text ('MIME ' + update.message.document.mime_type)
    user = update.message.from_user
    document =  bot.get_file(update.message.document.file_id)
    document.download(update.message.document.file_name)
    logger.info("Document of %s: %s", user.first_name, update.message.document.file_name)


def cmd_audio (bot, update):
    """ TODO """
    update.message.reply_text ('Got ' + update.message.audio.file_id)
    update.message.reply_text ('MIME ' + update.message.audio.mime_type)
    print (re.findall(r'/(\w+)', update.message.audio.mime_type))
    user = update.message.from_user
    document =  bot.get_file(update.message.audio.file_id)
    document.download('test.mp3')
    logger.info("Audio of %s: %s", user.first_name, update.message.audio.file_id)


def cmd_halt (bot, update):
    """ TODO """

def cmd_unknown (bot, update):
    """Send a message if the command is not defined."""
    update.message.reply_text ('Command not found. Type /help for... help.')


def cmd_error (bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning ('Update "%s" caused error "%s"', update, error)


def main ():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater ("462574820:AAEG-r9mlu7kTyMnYHcKS0rKae7uYgXBN5Q")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler (CommandHandler ("start",        cmd_start))
    dp.add_handler (CommandHandler ("help",         cmd_help))
    dp.add_handler (CommandHandler ("halt",         cmd_halt))

    # TODO TODO TODO Define image filter here TODO TODO TODO
    dp.add_handler (MessageHandler (Filters.audio, cmd_audio))
    dp.add_handler (MessageHandler (Filters.document, cmd_document))

    # on unknown command, put some help text
    dp.add_handler (MessageHandler (Filters.command, cmd_unknown))

    # log all errors
    dp.add_error_handler (cmd_error)

    # Start the Bot
    updater.start_polling ()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling () is non-blocking and will stop the bot gracefully.
    updater.idle ()


if __name__ == '__main__':
    main ()


