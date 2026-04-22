import logging
from telegram import Update
from telegram.ext import ContextTypes
import os

import gemini_client
import shelby_client

# Basic logging configuration
logger = logging.getLogger(__name__)

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    welcome_text = (
        f"Hello {user.first_name}!\n\n"
        "I am the Shelby Tele-Archive Bot. \n"
        "Send me a long text, document, or image. "
        "I will scan it, summarize it using AI, and permanently archive it on the Shelby Web3 network."
    )
    await update.message.reply_text(welcome_text)

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = (
        "📖 User Guide:\n"
        "1. Send Text: I will summarize and archive it.\n"
        "2. Send File (PDF, DOCX, TXT): I will analyze and upload it to Shelby.\n"
        "3. Send Image: I will archive the image binary on the network.\n"
        "4. Send Video: (<20MB) I will archive video on the decentralized network.\n\n"
        "You will receive a direct link to the Shelby Explorer!"
    )
    await update.message.reply_text(help_text)

async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle normal text messages"""
    text = update.message.text
    if not text:
        return
        
    status_message = await update.message.reply_text("⏳ Analyzing and summarizing text with AI...")
    
    # 1. Summarize with Gemini
    summary = gemini_client.summarize_text(text)
    
    await status_message.edit_text("⏳ Connecting to Node.js bridge to upload blob data to Web3 Shelby...")
    
    # 2. Upload to Shelby
    content_bytes = text.encode('utf-8')
    shelby_res = shelby_client.upload_to_shelby(
        content=content_bytes,
        metadata_summary=summary,
        content_type="text/plain"
    )
    
    if shelby_res["success"]:
        response_text = (
            "✅ Upload Successful!\n\n"
            f"AI Summary: {summary}\n"
            f"Blob ID: {shelby_res['blob_id']}\n\n"
            f"🔍 View On-Chain: {shelby_res['url']}"
        )
    else:
        response_text = f"❌ Upload Error: {shelby_res['error']}"
        
    await status_message.edit_text(response_text)

async def document_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document files sent to the bot"""
    document = update.message.document
    if document.file_size > 20 * 1024 * 1024: # Limit 20MB
        await update.message.reply_text("❌ File size too large. Please send files under 20MB.")
        return
        
    status_message = await update.message.reply_text("⏳ Downloading file to system...")
    
    try:
        # Download file from Telegram Server
        file_obj = await update.message.document.get_file()
        file_bytes = await file_obj.download_as_bytearray()
        
        await status_message.edit_text("⏳ Analyzing file to generate metadata...")
        
        summary = gemini_client.generate_metadata_for_file(
            filename=document.file_name,
            file_size=document.file_size,
            extra_info="Document format"
        )
        
        await status_message.edit_text("⏳ Packaging data and calling Node.js to upload to Shelby...")
        
        # Upload
        shelby_res = shelby_client.upload_to_shelby(
            content=file_bytes,
            metadata_summary=summary,
            content_type=document.mime_type
        )
        
        if shelby_res["success"]:
            response_text = (
                "✅ File Archived Successfully!\n\n"
                f"File: {document.file_name}\n"
                f"AI Metadata: {summary}\n"
                f"Blob ID: {shelby_res['blob_id']}\n\n"
                f"🔍 Explorer URL: {shelby_res['url']}"
            )
        else:
            response_text = f"❌ Document Upload Error: {shelby_res['error']}"
            
        await status_message.edit_text(response_text)
        
    except Exception as e:
        logger.error(f"Error handling document: {e}")
        await status_message.edit_text(f"❌ System error during file processing: {e}")

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle image files sent to the bot"""
    photo = update.message.photo[-1] # Get highest resolution
    
    status_message = await update.message.reply_text("⏳ Downloading image and calling Node.js to upload to Shelby...")
    
    try:
        file_obj = await photo.get_file()
        file_bytes = await file_obj.download_as_bytearray()
        
        summary = "Image sent via Telegram Bot archived as a Blob."
        
        shelby_res = shelby_client.upload_to_shelby(
            content=file_bytes,
            metadata_summary=summary,
            content_type="image/jpeg"
        )
        
        if shelby_res["success"]:
            response_text = (
                "✅ Image uploaded to blockchain successfully!\n\n"
                f"Blob ID: {shelby_res['blob_id']}\n\n"
                f"🔍 View On-Chain: {shelby_res['url']}"
            )
        else:
            response_text = f"❌ Image Upload Error: {shelby_res['error']}"
            
        await status_message.edit_text(response_text)
        
    except Exception as e:
        logger.error(f"Error handling photo: {e}")
        await status_message.edit_text(f"❌ System error during image processing: {e}")

async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle video files sent to the bot"""
    video = update.message.video
    if video.file_size > 20 * 1024 * 1024:
        await update.message.reply_text("❌ Video size too large. Please send videos under 20MB.")
        return
        
    status_message = await update.message.reply_text("⏳ Downloading video to system...")
    
    try:
        file_obj = await video.get_file()
        file_bytes = await file_obj.download_as_bytearray()
        
        await status_message.edit_text("⏳ Interacting via Node.js to upload video to Web3...")
        
        summary = "Video uploaded via Shelby Tele-archive"
        
        shelby_res = shelby_client.upload_to_shelby(
            content=file_bytes,
            metadata_summary=summary,
            content_type=video.mime_type or "video/mp4"
        )
        
        if shelby_res["success"]:
            response_text = (
                "✅ Video Upload Successful!\n\n"
                f"Blob ID: {shelby_res['blob_id']}\n\n"
                f"🔍 View On-Chain: {shelby_res['url']}"
            )
        else:
            response_text = f"❌ Upload Error: {shelby_res['error']}"
            
        await status_message.edit_text(response_text)
        
    except Exception as e:
        logger.error(f"Error handling video: {e}")
        await status_message.edit_text(f"❌ System error during video processing: {e}")

async def list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /list command to view uploaded blobs"""
    status_msg = await update.message.reply_text("⏳ Scanning document list on Web3...")
    
    res = shelby_client.list_blobs()
    if not res.get("success"):
        await status_msg.edit_text(f"❌ Error fetching list: {res.get('error')}")
        return
        
    blobs = res.get("blobs", [])
    if not blobs:
        await status_msg.edit_text("🗂 Your storage vault is currently empty!")
        return
        
    # Get top 15 blobs
    top_blobs = blobs[:15]
    
    lines = ["🗂 Vault Documents:\n"]
    for i, b in enumerate(top_blobs, 1):
        name = b.get("name", "Unknown").split("/")[-1]
        size = b.get("size", 0) / (1024 * 1024)
        lines.append(f"{i}. ID: {name} | {size:.2f} MB")
        
    lines.append("\n⬇️ Type: /download <ID> to fetch your file.")
    await status_msg.edit_text("\n".join(lines))

async def download_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /download <blob_id> command"""
    if not context.args:
        await update.message.reply_text("❌ Missing Blob ID. Example: /download blob_abc")
        return
        
    blob_id = context.args[0].split("/")[-1]
    status_msg = await update.message.reply_text(f"⏳ Calling network to download blob ID: {blob_id}...")
    
    res = shelby_client.download_from_shelby(blob_id)
    if not res.get("success"):
        await status_msg.edit_text(f"❌ Download Error: {res.get('error')}")
        return
        
    path = res.get("path")
    if not path or not os.path.exists(path):
        await status_msg.edit_text(f"❌ Error: File not found locally after fetching.")
        return
        
    await status_msg.edit_text("⏳ Sending file to Telegram...")
    try:
        with open(path, "rb") as f:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=f,
                filename=blob_id,
                caption="📥 Your document has been successfully extracted from the Shelby network!"
            )
        await status_msg.delete()
    except Exception as e:
        logger.error(f"Error sending file via Telegram: {e}")
        await status_msg.edit_text(f"❌ Error delivering file: {e}")
    finally:
        if os.path.exists(path):
            os.remove(path)
