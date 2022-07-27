from django.contrib import admin

from telegram_bot.models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    pass

