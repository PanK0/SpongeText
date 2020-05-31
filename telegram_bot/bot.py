import logging
import os
import random
import sys

from telegram.ext import Updater, CommandHandler

# Enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Getting mode, so we could define run function for local and Heroku setup
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)


def spongify(text) :
    spongytext = ""
    for letter in text :
        rand = random.randint(0, 100)
        if (rand < 50) :
            spongytext += letter.lower()
        else :
            spongytext += letter.upper()
    return spongytext


def help_handler(bot, update):
    # Creating a handler-function for /start command
    logger.info("User {} started bot".format(update.effective_user["id"]))
    bot.send_message(chat_id=update.message.chat_id, text="heLlo! tHiS is the sPoNGeTEXtBot1!1!!" +
                            "\n/sponge   : reply to a message with /sponge to spongify it!" +
                            "\n/spongify : write /spongify before a message to spongify!")


def sponge_handler(bot, update):
    # Creating a handler-function for /spongify command
    logger.info(update.message)
    if (update.message.chat.type == "group") :
        update.message.reply_text("Write /spongify before a message to spongify that message!")
    elif (update.message.reply_to_message != None) :
        logger.info("User " + str(update.message.from_user.first_name) + " spongifyed " + str(update.message.reply_to_message.from_user.first_name))
        text = update.message.reply_to_message.text
        update.message.reply_text(spongify(text))
    else :
        dict = update.message
        logger.info(spongify(update.message.text[8:]))
        update.message.reply_text("Reply to a message writing /sponge to spongify that message!")

def spongify_handler(bot, update):
    if (update.message.reply_to_message != None) :
        update.message.reply_text("Write /spongify before a message to spongify that message!")
        return
    logger.info(update.message)
    bot.send_message(chat_id=update.message.chat_id, text=spongify(update.message.text[10:]))
    #update.message.reply_text(spongify(update.message.text[10:]))

def webapp_handler(bot, update):
    update.message.text("Visit https://pank0.github.io/spongetext/ for the webapp")

if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("help", help_handler))
    updater.dispatcher.add_handler(CommandHandler("sponge", sponge_handler))
    updater.dispatcher.add_handler(CommandHandler("spongify", spongify_handler))
    updater.dispatcher.add_handler(CommandHandler("webapp", webapp_handler))

    run(updater)
