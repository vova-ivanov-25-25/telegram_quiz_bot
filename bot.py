import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
import config
from handlers import start, help_command, quiz_command, answer_callback, stats_command

logging.basicConfig(level=logging.INFO)

def main():
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('quiz', quiz_command))
    app.add_handler(CommandHandler('stats', stats_command))

    app.add_handler(CallbackQueryHandler(answer_callback))

    print("Bot started")
    app.run_polling()

if __name__ == '__main__':
    main()
