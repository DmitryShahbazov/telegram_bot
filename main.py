import logging
from telegram.ext import Updater, CommandHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def read_vpn_status_log():
    with open('/etc/openvpn/server/openvpn-status.log', 'r') as log_file:
        log_text = log_file.read()
        log_file.close()
    return log_text


def get_vpn_status(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_vpn_status())


updater = Updater('1159891259:AAFNZ3isJAWyH8C2dUyfgGfah5yET04fi84', use_context=True)

updater.dispatcher.add_handler(CommandHandler('vpn_status', get_vpn_status))

updater.start_polling()
updater.idle()