from django.core.management import BaseCommand
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackQueryHandler
from bot.views import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        TOKEN = ""
        updater = Updater(TOKEN)
        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
        updater.start_polling()
        updater.idle()

