import os
from threading import Thread

from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)


@app.route("/")
def home():
    return "Golden VIP Bot is running!"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ بەخێربێیت بۆ Golden VIP!\n\n"
        "🆓 Free Predictions\n"
        "💎 VIP Predictions\n"
        "💳 Buy VIP"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "فەرمانەکان:\n"
        "/start - دەستپێکردن\n"
        "/help - یارمەتی"
    )


def run_flask():
    app.run(host="0.0.0.0", port=8080)


def main():
    Thread(target=run_flask, daemon=True).start()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling()


if __name__ == "__main__":
    main()
