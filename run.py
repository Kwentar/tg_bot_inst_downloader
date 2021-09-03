from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext

import config
from downloader import get_decs_and_image_url_by_url


def start(update: Update, context: CallbackContext):

    chat_id = update.message.chat_id

    context.bot.send_message(chat_id=chat_id,
                             text='Send me instagram url')


def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    print(f'download {text} from {update.effective_user.id}')

    chat_id = update.message.chat_id
    message, url = get_decs_and_image_url_by_url(text.strip())
    if url:
        context.bot.send_photo(chat_id, caption=message, photo=url)
        context.bot.send_document(chat_id, document=url)
    else:
        context.bot.send_message(chat_id, text='something wrong')


def main():
    updater = Updater(config.TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, message_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
