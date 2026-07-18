import os
import io
import logging
import requests
from PIL import Image
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# ---------------------------
# /start command
# ---------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Welcome to Jerry Bay Bot!\n\n"
        "Here's what I can do:\n\n"
        "🖼 *Image Convert*\n"
        "Send me a photo, then use /convert <format> "
        "(e.g. /convert png) as a reply to that photo.\n\n"
        "🎨 *AI Image Generate*\n"
        "/generate <your prompt>\n"
        "Example: /generate a cat riding a bicycle\n\n"
        "🔗 *URL Shorten*\n"
        "/shorten <long url>\n"
        "Example: /shorten https://example.com/very/long/link\n"
    )
    await update.message.reply_markdown(text)


# ---------------------------
# Image Converter
# ---------------------------
async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text(
            "⚠️ Please reply to a photo with /convert <format>\n"
            "Example: /convert png"
        )
        return

    if not context.args:
        await update.message.reply_text("⚠️ Please specify a format, e.g. /convert png")
        return

    target_format = context.args[0].lower()
    supported = ["png", "jpeg", "jpg", "webp", "bmp", "gif"]
    if target_format not in supported:
        await update.message.reply_text(
            f"⚠️ Unsupported format. Choose from: {', '.join(supported)}"
        )
        return

    await update.message.reply_text("🔄 Converting...")

    photo = update.message.reply_to_message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    photo_bytes = await file.download_as_bytearray()

    image = Image.open(io.BytesIO(photo_bytes))
    if target_format in ("jpg", "jpeg") and image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    output = io.BytesIO()
    save_format = "JPEG" if target_format in ("jpg", "jpeg") else target_format.upper()
    image.save(output, format=save_format)
    output.seek(0)
    output.name = f"converted.{target_format}"

    await update.message.reply_document(document=output, filename=output.name)


# ---------------------------
# AI Image Generator (Pollinations.ai - free, no API key needed)
# ---------------------------
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "⚠️ Please provide a prompt.\nExample: /generate a cat riding a bicycle"
        )
        return

    prompt = " ".join(context.args)
    await update.message.reply_text("🎨 Generating your image, please wait...")

    try:
        url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}"
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        image_bytes = io.BytesIO(response.content)
        image_bytes.name = "generated.png"
        await update.message.reply_photo(photo=image_bytes, caption=f'"{prompt}"')
    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        await update.message.reply_text("❌ Failed to generate image. Please try again.")


# ---------------------------
# URL Shortener (TinyURL - free, no API key needed)
# ---------------------------
async def shorten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "⚠️ Please provide a URL.\nExample: /shorten https://example.com"
        )
        return

    long_url = context.args[0]

    try:
        response = requests.get(
            "https://tinyurl.com/api-create.php",
            params={"url": long_url},
            timeout=15,
        )
        response.raise_for_status()
        short_url = response.text
        await update.message.reply_text(f"🔗 Shortened URL:\n{short_url}")
    except Exception as e:
        logger.error(f"URL shortening failed: {e}")
        await update.message.reply_text("❌ Failed to shorten URL. Please check the link and try again.")


# ---------------------------
# Fallback for unrecognized messages
# ---------------------------
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤔 I didn't understand that. Send /start to see what I can do."
    )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable is not set")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("convert", convert))
    app.add_handler(CommandHandler("generate", generate))
    app.add_handler(CommandHandler("shorten", shorten))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    logger.info("Jerry Bay Bot is starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
