from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, filters
from config import TOKEN
from handlers.admin import add_admin, list_admins, del_admin, handle_admin_deletion, cancel_list_admins, DELADM_SELECT_ADMIN
from handlers.user import start, get_user_info

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    del_admin_handler = ConversationHandler(
        entry_points=[CommandHandler('deladm', del_admin)],
        states={DELADM_SELECT_ADMIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_deletion)]},
        fallbacks=[CommandHandler("cancel", cancel_list_admins)]
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_user_info))
    application.add_handler(CommandHandler("addadmin", add_admin))
    application.add_handler(CommandHandler("listadm", list_admins))
    application.add_handler(del_admin_handler)

    print("Bot berjalan...")
    application.run_polling()

if __name__ == "__main__":
    main()
