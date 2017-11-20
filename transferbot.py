#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This bot downloads attachments then uploads them to transfer.sh
"""

import logging, re, requests, os
from telegram.ext   import Updater, CommandHandler, MessageHandler
from telegram.ext   import Filters, CallbackQueryHandler

#   GLOBALZ
TOKEN       = open('conf/token.conf', 'r').read().replace("\n", "")
FILES_POOL  = '/tmp/'

#   LOGGER
logging.basicConfig (format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger (__name__)

def remove (filename):
    """ Removes the file after transfer.
    """
    print ('test')
    try:
        os.remove(FILES_POOL + filename)
    except Exception, e:
        logger.error ("Something went wrong, backtrace: \n%s" %(e))
        return
    logger.info ("Removed %s", filename)

def transfer (filename):
    """ Sends filename then deletes it. Returns transfer.sh file's url.
    """
    upload_url = "https://transfer.sh/" + filename
    try:
        r = requests.put (url=upload_url, data=open (FILES_POOL + filename, "r"))
    except Exception, e:
        logger.error ("Something went wrong, backtrace: \n%s" %(e))
        return
    logger.info ("Transfered %s", filename)
    remove (filename)
    try:
        return (r.text.strip ())
    except Exception, e:
        logger.error ("Something went wrong, backtrace: \n%s" %(e))
        return

#   HANDLERS
def cmd_start (bot, update):
    """ Send a message when the command /start is issued.
    """
    update.message.reply_text ('Transferbot 0.1')

def cmd_help (bot, update):
    """ Send a message when the command /help is issued.
    """
    update.message.reply_text ('Just send a picture, video, song or any other of telegram-supported ' \
                               'media to upload it over transfer.sh')

def cmd_unknown (bot, update):
    """ Send a message if the command is not defined.
    """
    update.message.reply_text ('Command not found. Type /help for... help.')

def cmd_error (bot, update, error):
    """ Log Errors caused by updates.
    """
    logger.warning ('Update "%s" caused error "%s"', update, error)

#   ATTACHMENT's FALLBACKS
def fbk_document (bot, update):
    """ Get document, then transfer it.
    """
    user        = update.message.from_user
    document    = bot.get_file (update.message.document.file_id)
    try:
        document.download (FILES_POOL + update.message.document.file_name)
    except Exception, e:
        logger.error ("Something went wrong, backtrace: \n%s" %(e))
        return
    logger.info ("Got document from %s: %s", user.first_name, update.message.document.file_name)
    update.message.reply_text (transfer (update.message.document.file_name))

def fbk_audio (bot, update):
    """ Get audio, then transfer it.
    """
    FIRST_EMT   = 0
    ext         = re.findall (r'/(\w+)', update.message.audio.mime_type)[FIRST_EMT]
    filename    = update.message.audio.file_id + '.' + ext
    user        = update.message.from_user
    document    = bot.get_file (update.message.audio.file_id)
    try:
        document.download (FILES_POOL + filename)
    except Exception, e:
        logger.error ("Something went wrong, backtrace: \n%s" %(e))
        return
    logger.info ("Got audio from %s: %s", user.first_name, filename)
    update.message.reply_text (transfer (filename))

def fbk_video (bot, update):
    """ Get video, then transfer it.
    """
    FIRST_EMT   = 0
    ext         = re.findall (r'/(\w+)', update.message.video.mime_type)[FIRST_EMT]
    filename    = update.message.video.file_id + '.' + ext
    user        = update.message.from_user
    document    = bot.get_file (update.message.video.file_id)
    try:
        document.download (FILES_POOL + filename)
    except Exception, e:
        logger.error ("Something went wrong, backtrace: \n%s" %(e))
        return
    logger.info ("Got video from %s: %s", user.first_name, filename)
    update.message.reply_text (transfer (filename))

def fbk_photo (bot, update):
    """ Get chat photo, the biggest from the list
    """
    BIGGEST_PIC = 3
    filename    = update.message.photo[BIGGEST_PIC].file_id + '.jpg'
    user        = update.message.from_user
    document    = bot.get_file (update.message.photo[BIGGEST_PIC].file_id)
    try:
        document.download (FILES_POOL + filename)
    except Exception, e:
        logger.error ("Something went wrong, backtrace: \n%s" %(e))
        return
    logger.info ("Got photo from %s: %s", user.first_name, filename)
    update.message.reply_text (transfer (filename))

#   MAIN
def main ():
    """ Start the bot.
    """
    #   Create the EventHandler and pass it your bot's token.
    updater = Updater (TOKEN)

    #   Get the dispatcher to register handlers
    dp = updater.dispatcher

    #   on different commands - answer in Telegram
    dp.add_handler (CommandHandler ("start",        cmd_start))
    dp.add_handler (CommandHandler ("help",         cmd_help))

    #   on unknown command, put some help text
    dp.add_handler (MessageHandler (Filters.command, cmd_unknown))

    #   Add stuff to handle
    dp.add_handler (MessageHandler (Filters.photo,      fbk_photo))
    dp.add_handler (MessageHandler (Filters.audio,      fbk_audio))
    dp.add_handler (MessageHandler (Filters.video,      fbk_video))
    dp.add_handler (MessageHandler (Filters.document,   fbk_document))

    #   log all errors
    dp.add_error_handler (cmd_error)

    #   Start the Bot
    updater.start_polling ()
    logger.info ('Kicking')

    #   Loop until SIGNALS
    updater.idle ()

if __name__ == '__main__':
    main ()
