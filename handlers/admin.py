from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, CallbackContext, filters
from utils.storage import load_admins, save_admins
from config import SUPERADMIN_ID

DELADM_SELECT_ADMIN = 1000  # State untuk ConversationHandler

async def add_admin(update: Update, context: CallbackContext):
    """Menambahkan admin baru."""
    user_id = update.effective_user.id
    if user_id != SUPERADMIN_ID:
        await update.message.reply_text("❌ Anda tidak memiliki izin untuk menambah admin.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("⚠️ Gunakan format /addadmin <user_id>.")
        return

    try:
        new_admin_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("⚠️ ID tidak valid.")
        return

    admins = load_admins()
    if new_admin_id in admins:
        await update.message.reply_text(f"⚠️ Pengguna dengan ID {new_admin_id} sudah menjadi admin.")
        return

    admins.append(new_admin_id)
    save_admins(admins)
    await update.message.reply_text(f"✅ Admin {new_admin_id} berhasil ditambahkan.")

async def list_admins(update: Update, context: CallbackContext):
    """Menampilkan daftar admin."""
    if update.effective_user.id != SUPERADMIN_ID:
        await update.message.reply_text("❌ Anda tidak memiliki izin untuk melihat daftar admin.")
        return

    admins = load_admins()
    if not admins:
        await update.message.reply_text("⚠️ Tidak ada admin yang terdaftar.")
        return

    admin_list = "\n".join([f"ID: {admin}" for admin in admins])
    await update.message.reply_text(f"📋 <b>Daftar Admin:</b>\n\n{admin_list}", parse_mode="HTML")

async def del_admin(update: Update, context: CallbackContext):
    """Memulai proses penghapusan admin."""
    if update.effective_user.id != SUPERADMIN_ID:
        await update.message.reply_text("❌ Anda tidak memiliki izin untuk menghapus admin.")
        return

    admins = load_admins()
    if not admins:
        await update.message.reply_text("⚠️ Tidak ada admin yang terdaftar.")
        return

    admin_list = "\n".join([f"{idx + 1}. ID: {admin}" for idx, admin in enumerate(admins)])
    await update.message.reply_text(f"📋 Daftar Admin:\n\n{admin_list}\n\nKetik nomor admin yang ingin dihapus.",
                                    parse_mode="HTML")
    context.user_data['admins'] = list(admins)
    return DELADM_SELECT_ADMIN

async def handle_admin_deletion(update: Update, context: CallbackContext):
    """Menangani penghapusan admin setelah nomor dipilih."""
    if 'admins' not in context.user_data:
        await update.message.reply_text("⚠️ Gunakan /deladm terlebih dahulu.")
        return ConversationHandler.END

    try:
        choice = int(update.message.text.strip())
        admins = context.user_data['admins']
        if choice < 1 or choice > len(admins):
            await update.message.reply_text("❌ Pilihan tidak valid.")
            return ConversationHandler.END

        admin_to_delete = admins.pop(choice - 1)
        save_admins(admins)
        await update.message.reply_text(f"✅ Admin dengan ID {admin_to_delete} telah dihapus.")
        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text("❌ Harap masukkan nomor yang valid.")
        return ConversationHandler.END

async def cancel_list_admins(update: Update, context: CallbackContext):
    """Membatalkan proses penghapusan admin."""
    await update.message.reply_text("❌ Proses dibatalkan.")
    return ConversationHandler.END
