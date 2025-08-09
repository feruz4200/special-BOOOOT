import os
import asyncio
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, ChatJoinRequestHandler, CommandHandler

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8417542679:AAGew1K8sbt3RJrKNaZKhS2f0aB-9-FMvmM"
VIDEO_FILE_ID = "BAACAgIAAxkBAAMaaJdCog2I67Q7uQ0SXmBcJnSSr_0AAmVoAAJypClLVFYOWL7XvMs2BA"

# ---------- Telegram handlers ----------
async def on_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jr = update.chat_join_request
    user_id = jr.from_user.id
    chat_id = jr.chat.id
    try:
        await context.bot.send_message(user_id, "👋 Assalomu alaykum! Zayavkangiz qabul qilinmoqda. Mana bepul darslik videosi:")
        await context.bot.send_video(user_id, video=VIDEO_FILE_ID, caption="Yoqsa, keyingi darslar uchun tayyor bo‘ling!")
    except Exception as e:
        logging.warning(f"DM/video yuborishda xato: {e}")
    try:
        await context.bot.approve_chat_join_request(chat_id=chat_id, user_id=user_id)
    except Exception as e:
        logging.error(f"Approve xato: {e}")

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot ishga tushgan. Join requestlarni avtomatik qabul qiladi.")

async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(on_join_request))
    app.add_handler(CommandHandler("start", cmd_start))
    logging.info("🚀 Bot polling boshlandi…")
    await app.run_polling(allowed_updates=["message", "chat_join_request"])

# ---------- Flask (healthcheck) ----------
web = Flask(__name__)

@web.get("/")
def health():
    return "OK", 200

def start_web():
    port = int(os.environ.get("PORT", "8080"))  # Railway port
    # Reloader o‘chirilgan, thread-safe
    web.run(host="0.0.0.0", port=port, use_reloader=False, threaded=True)

if __name__ == "__main__":
    # Flask'ni alohida oqimda ko‘taramiz
    threading.Thread(target=start_web, daemon=True).start()
    # Botni event-loop’da yuritamiz
    asyncio.run(run_bot())
