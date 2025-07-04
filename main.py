import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from googletrans import Translator

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

translator = Translator()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("你好！我是一个中英互译机器人。请直接发送消息，我会帮你翻译。")

async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        return

    detected = translator.detect(text)
    src_lang = detected.lang
    target_lang = "zh-cn" if src_lang == "en" else "en"

    translated = translator.translate(text, src=src_lang, dest=target_lang)
    await update.message.reply_text(translated.text)

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("❌ 请设置 BOT_TOKEN 环境变量")
        return

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_message))
    app.run_polling()

if __name__ == "__main__":
    main()
