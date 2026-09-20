import os
from threading import Thread

from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)


@app.route("/")
def home():
    return "Golden VIP Bot is running!"


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("💎 VIP Predictions", callback_data="vip"),
        ],
        [
            InlineKeyboardButton("🆓 Free Predictions", callback_data="free"),
        ],
        [
            InlineKeyboardButton("💳 Buy VIP", callback_data="buy"),
        ],
        [
            InlineKeyboardButton("📢 Telegram Channel", url="https://t.me/betwen211"),
        ],
        [
            InlineKeyboardButton("🎵 TikTok", url="https://www.tiktok.com/@betwen211"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👑 GOLDEN VIP\n\n"
        "⚽ بەخێربێیت بۆ GOLDEN VIP\n\n"
        "🔥 پێشبینییەکانی ڕۆژ\n"
        "💎 VIP Predictions\n"
        "🎯 پێشبینی تایبەت\n"
        "🏆 Daily Football Tips\n\n"
        "👇 یەکێک لە هەڵبژاردەکان هەڵبژێرە:",
        reply_markup=reply_markup,
    )


# =========================
# BUTTONS
# =========================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "vip":
        await query.edit_message_text(
            "💎 GOLDEN VIP\n\n"
            "🔥 VIP Predictions\n"
            "⚽ پێشبینی تایبەت و ڕۆژانە\n"
            "🎯 High Quality Picks\n\n"
            "💳 بۆ کڕینی VIP کلیک لەسەر Buy VIP بکە."
        )

    elif query.data == "free":
        await query.edit_message_text(
            "🆓 FREE PREDICTIONS\n\n"
            "⚽ پێشبینییە فرییەکان لەم بەشەدا بڵاودەکرێنەوە.\n\n"
            "🔥 بۆ پێشبینییە تایبەتەکان → VIP"
        )

    elif query.data == "buy":
        await query.edit_message_text(
            "💳 BUY GOLDEN VIP\n\n"
            "💎 بۆ بەدەستهێنانی VIP پەیوەندیمان پێوە بکە.\n\n"
            "📩 Telegram: @YOUR_USERNAME\n"
            "🎟 CODE: VIP"
        )


# =========================
# HELP
# =========================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 GOLDEN VIP\n\n"
        "فەرمانەکان:\n\n"
        "/start - دەستپێکردن\n"
        "/help - یارمەتی"
    )


# =========================
# FLASK
# =========================

def run_flask():
    app.run(host="0.0.0.0", port=8080)


# =========================
# MAIN
# =========================

def main():
    Thread(target=run_flask, daemon=True).start()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()


if __name__ == "__main__":
    main()
