import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import Config
import bot_handlers

# Bật tính năng ghi nhật ký (logging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Khởi động bot"""
    
    # Kiểm tra biến môi trường
    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"Khởi tạo lỗi: {e}")
        logger.error("Vui lòng sao chép file .env.example thành .env và điền đầy đủ các keys.")
        return

    # Tạo Application
    application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()

    # Đăng ký các handler
    application.add_handler(CommandHandler("start", bot_handlers.start_handler))
    application.add_handler(CommandHandler("help", bot_handlers.help_handler))
    
    # Xử lý tin nhắn văn bản thông thường
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot_handlers.text_message_handler))
    
    # Xử lý document
    application.add_handler(MessageHandler(filters.Document.ALL, bot_handlers.document_handler))
    
    # Xử lý ảnh
    application.add_handler(MessageHandler(filters.PHOTO, bot_handlers.photo_handler))

    # Xử lý video
    application.add_handler(MessageHandler(filters.VIDEO, bot_handlers.video_handler))
    
    # Các lệnh tra cứu metadata
    application.add_handler(CommandHandler("list", bot_handlers.list_handler))
    application.add_handler(CommandHandler("download", bot_handlers.download_handler))

    # Chạy bot cho đến khi nhấn Ctrl-C
    logger.info("Bot đang chạy... Bấm Ctrl-C để dừng.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    # Fix import error for Update from polling args if needed
    from telegram import Update
    main()
