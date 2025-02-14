from telegram import Update
from telegram.ext import CommandHandler

async def start(update: Update, context):
    """Menjalankan perintah /start."""
    user = update.message.from_user
    await update.message.reply_text(f"Halo {user.first_name}! Kirimkan pesan untuk mendapatkan ID dan username kamu.")

async def get_user_info(update: Update, context):
    """Mendapatkan ID dan username pengguna."""
    user = update.message.from_user
    user_info = f"🆔 ID: {user.id}\n👤 Username: @{user.username if user.username else 'Tidak ada'}"
    await update.message.reply_text(user_info)
