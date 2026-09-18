import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ بەخێربێیت بۆ Golden VIP!\n\n"
        "🆓 Free Predictions\n"
        "💎 VIP Predictions\n"
        "💳 Buy VIP"
    )


telegram_app.add_handler(CommandHandler("start", start))


@app.route("/")
def home():
    return "Golden VIP Bot is running!"


@app.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return "OK"


if __name__ == "__main__":
    import asyncio

    async def run():
        await telegram_app.initialize()
        await telegram_app.start()

        port = int(os.getenv("PORT", 10000))
        app.run(host="0.0.0.0", port=port)

    asyncio.run(run()) 
