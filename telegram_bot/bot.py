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


def start_handler(bot, update):
    # Creating a handler-function for /start command
    logger.info("User {} started bot".format(update.effective_user["id"]))
    update.message.reply_text("heLlo! tHiS is the sPoNGeTEXtBot1!1!!\nReply to a message writing /spongify to spongify that message!")


def spongy_handler(bot, update):
    # Creating a handler-function for /spongify command
    if (update.message.reply_to_message) :
        logger.info("User " + str(update.message.from_user.first_name) + " spongifyed " + str(update.message.reply_to_message.from_user.first_name))
        text = update.message.reply_to_message.text
        update.message.reply_text(spongify(text))
    else :
        update.message.reply_text("Reply to a message writing /spongify to spongify that message!")


def webapp_handler(bot, update):
    update.message.reply_text("Visit https://pank0.github.io/spongetext/ for the webapp")

if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("spongify", spongy_handler))
    updater.dispatcher.add_handler(CommandHandler("webapp", webapp_handler))

    run(updater)
