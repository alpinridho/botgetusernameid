from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
import asyncio
import re

# Ganti dengan token bot kamu
TOKEN = "7870248619:AAEVVd85yasA4lYKNpJAPLO4vrsEVL9Pvyg"

async def start(update: Update, context) -> None:
    user = update.message.from_user
    await update.message.reply_text(f"Halo {user.first_name}! Kirimkan pesan apa saja untuk mendapatkan ID dan username kamu.")

async def get_user_info(update: Update, context) -> None:
    user = update.message.from_user
    user_info = f"🆔 ID: {user.id}\n👤 Username: @{user.username if user.username else 'Tidak ada'}"
    await update.message.reply_text(user_info)

# =================================== MAIN =============================================================
async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_user_info))
    
    print("Bot berjalan...")
    application.run_polling()

if __name__ == "__main__":
    (main()
 
