import os
import asyncio
import logging
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, ContextTypes,
    ChatJoinRequestHandler, CommandHandler
)

# ---------- Sozlamalar ----------
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "8417542679:AAGew1K8sbt3RJrKNaZKhS2f0aB-9-FMvmM"
VIDEO_FILE_ID = "BAACAgIAAxkBAAMaaJdCog2I67Q7uQ0SXmBcJnSSr_0AAmVoAAJypClLVFYOWL7XvMs2BA"

# ---------- Telegram Handlers ----------
async def on_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jr = update.chat_join_request
    user_id = jr.from_user.id
    chat_id = jr.chat.id

    # 1) Salom
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text="👋 Assalomu alaykum! Zayavkangiz qabul qilinmoqda. Mana bepul darslik videosi:"
        )
    except Exception as e:
        logging.warning(f"DM xabar yuborilmadi ({user_id}): {e}")

    # 2) Video
    try:
        await context.bot.send_video(
            chat_id=user_id,
            video=VIDEO_FILE_ID,
            caption="Yoqsa, keyingi darslar uchun tayyor bo‘ling!"
        )
    except Exception as e:
        logging.warning(f"Video yuborilmadi ({user_id}): {e}")

    # 3) Approve
    try:
        await context.bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
    except Exception as e:
        logging.error(f"Approve xato ({user_id}): {e}")

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot ishga tushgan. Join requestlarni avtomatik qabul qiladi.")

# Pollingni alohida task sifatida yurgizamiz
async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(on_join_request))
    app.add_handler(CommandHandler("start", cmd_start))
    logging.info("🚀 Bot polling boshlandi…")
    await app.run_polling(allowed_updates=["message", "chat_join_request"])

# ---------- Flask (healthcheck uchun) ----------
web = Flask(__name__)

@web.get("/")
def health():
    return "OK", 200

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())

    port = int(os.environ.get("PORT", "8080"))
    web.run(host="0.0.0.0", port=port)
