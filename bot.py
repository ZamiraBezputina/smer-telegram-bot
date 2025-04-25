import logging
import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Шаги диалога
SOBYTIE, MYSLI, EMOCII, REAKCII = range(4)

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Загружаем токен и ключи из переменных окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GOOGLE_CREDENTIALS = os.environ.get("GOOGLE_CREDENTIALS")  # JSON как строка

# Подключаемся к Google Таблице
creds_dict = json.loads(GOOGLE_CREDENTIALS)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("PIRUSdiary").sheet1

# Временное хранилище
user_data = {}

# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Привет! Начнём СМЭР-дневник ✨\nЧто случилось?")
    return SOBYTIE

async def sobytie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data[update.effective_user.id] = {'sobytie': update.message.text}
    await update.message.reply_text("Какие были мысли?")
    return MYSLI

async def mysli(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data[update.effective_user.id]['mysli'] = update.message.text
    await update.message.reply_text("Какие эмоции ты испытала?")
    return EMOCII

async def emocii(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data[update.effective_user.id]['emocii'] = update.message.text
    await update.message.reply_text("Какие телесные или поведенческие реакции ты заметила?")
    return REAKCII

async def reakcii(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data[update.effective_user.id]['reakcii'] = update.message.text
    data = user_data[update.effective_user.id]
    row = [datetime.now().strftime("%Y-%m-%d %H:%M"), data['sobytie'], data['mysli'], data['emocii'], data['reakcii']]
    sheet.append_row(row)
    await update.message.reply_text("Готово! ✅\nХочешь записать ещё — напиши /start.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Окей, в другой раз!")
    return ConversationHandler.END

# Запуск
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SOBYTIE: [MessageHandler(filters.TEXT & ~filters.COMMAND, sobytie)],
            MYSLI: [MessageHandler(filters.TEXT & ~filters.COMMAND, mysli)],
            EMOCII: [MessageHandler(filters.TEXT & ~filters.COMMAND, emocii)],
            REAKCII: [MessageHandler(filters.TEXT & ~filters.COMMAND, reakcii)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)
    print("Бот запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()
