from auth import TOKEN
import bot
from telegram.ext import Updater, CommandHandler, InlineQueryHandler


def main():
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    # se añaden los métodos que controlan cada comando
    dispatcher.add_handler(CommandHandler('start', bot.start))
    dispatcher.add_handler(CommandHandler('total', bot.total))
    # for inline queries
    dispatcher.add_handler(InlineQueryHandler(bot.inline_query))
    dispatcher.add_error_handler(bot.error)

    # iniciar bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()