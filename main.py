import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import Config
import bot_handlers


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Khởi động bot"""
    

    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"Khởi tạo lỗi: {e}")
        logger.error("Vui lòng sao chép file .env.example thành .env và điền đầy đủ các keys.")
        return


    application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()


    application.add_handler(CommandHandler("start", bot_handlers.start_handler))
    application.add_handler(CommandHandler("help", bot_handlers.help_handler))
    

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.text_message_handler))

    application.add_handler(MessageHandler(filters.Document.ALL, bot_handlers.document_handler))

    application.add_handler(MessageHandler(filters.PHOTO, bot_handlers.photo_handler))


    application.add_handler(MessageHandler(filters.VIDEO, bot_handlers.video_handler))
    

    application.add_handler(CommandHandler("list", bot_handlers.list_handler))
    application.add_handler(CommandHandler("download", bot_handlers.download_handler))


    logger.info("Bot đang chạy... Bấm Ctrl-C để dừng.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    # Fix import error for Update from polling args if needed
    from telegram import Update
    main()
