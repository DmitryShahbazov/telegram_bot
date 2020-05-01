import logging
from telegram.ext import Updater, CommandHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_vpn_status(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


updater = Updater('1159891259:AAFNZ3isJAWyH8C2dUyfgGfah5yET04fi84', use_context=True)

updater.dispatcher.add_handler(CommandHandler('vpn status', get_vpn_status()))

updater.start_polling()
updater.idle()