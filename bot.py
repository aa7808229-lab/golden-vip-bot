import os
from threading import Thread

from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("8971754803:AAGU52_PUi_hLqfbQTuWAbHT3kvCSRDDq4o")
ADMIN_ID = 6773856976

app = Flask(__name__)


@app.route("/")
def home():
    return "Golden VIP Bot is running!"


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💎 VIP Predictions", callback_data="vip")],
        [InlineKeyboardButton("🆓 Free Predictions", callback_data="free")],
        [InlineKeyboardButton("💳 VIP Payment", callback_data="payment")],
        [InlineKeyboardButton(
            "📢 Telegram Channel",
            url="https://t.me/betwen211"
        )],
        [InlineKeyboardButton(
            "🎵 TikTok",
            url="https://www.tiktok.com/@betwen211"
        )],
    ]

    await update.message.reply_text(
        "👑 GOLDEN VIP\n\n"
        "⚽ بەخێربێیت بۆ GOLDEN VIP\n\n"
        "🔥 پێشبینییەکانی ڕۆژ\n"
        "💎 VIP Predictions\n"
        "🎯 پێشبینی تایبەت\n"
        "🏆 Daily Football Tips\n\n"
        "👇 یەکێک لە هەڵبژاردەکان هەڵبژێرە:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# =========================
# BUTTONS
# =========================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # VIP
    if query.data == "vip":
        keyboard = [
            [InlineKeyboardButton("💳 VIP Payment", callback_data="payment")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")],
        ]

        await query.edit_message_text(
            "💎 GOLDEN VIP\n\n"
            "🔥 VIP Predictions\n"
            "⚽ پێشبینی تایبەت و ڕۆژانە\n"
            "🎯 High Quality Picks\n\n"
            "💳 بۆ بەدەستهێنانی VIP، شێوازی پارەدان هەڵبژێرە:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # FREE
    elif query.data == "free":
        await query.edit_message_text(
            "🆓 FREE PREDICTIONS\n\n"
            "⚽ پێشبینییە فرییەکان لەم بەشەدا بڵاودەکرێنەوە.\n\n"
            "🔥 بۆ پێشبینییە تایبەتەکان → VIP"
        )

    # PAYMENT METHODS
    elif query.data == "payment":
        keyboard = [
            [InlineKeyboardButton("📱 Korek", callback_data="korek")],
            [InlineKeyboardButton("📱 Zain", callback_data="zain")],
            [InlineKeyboardButton("📱 Asiacell", callback_data="asiacell")],
            [InlineKeyboardButton("🔙 Back", callback_data="back")],
        ]

        await query.edit_message_text(
            "💳 GOLDEN VIP PAYMENT\n\n"
            "تکایە شێوازی پارەدان هەڵبژێرە:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # KOREK
    elif query.data == "korek":
        context.user_data["payment_method"] = "Korek"

        await query.edit_message_text(
            "📱 KOREK\n\n"
            "💳 تکایە پارەدانەکەت بکە.\n\n"
            "📸 پاش پارەدان، وێنەی کارت/پسووڵەکە بنێرە بۆ بۆتەکە.\n\n"
            "⬅️ دوای ناردنی وێنەکە، Admin پشکنینی دەکات."
        )

    # ZAIN
    elif query.data == "zain":
        context.user_data["payment_method"] = "Zain"

        await query.edit_message_text(
            "📱 ZAIN\n\n"
            "💳 تکایە پارەدانەکەت بکە.\n\n"
            "📸 پاش پارەدان، وێنەی کارت/پسووڵەکە بنێرە بۆ بۆتەکە.\n\n"
            "⬅️ دوای ناردنی وێنەکە، Admin پشکنینی دەکات."
        )

    # ASIACELL
    elif query.data == "asiacell":
        context.user_data["payment_method"] = "Asiacell"

        await query.edit_message_text(
            "📱 ASIACELL\n\n"
            "💳 تکایە پارەدانەکەت بکە.\n\n"
            "📸 پاش پارەدان، وێنەی کارت/پسووڵەکە بنێرە بۆ بۆتەکە.\n\n"
            "⬅️ دوای ناردنی وێنەکە، Admin پشکنینی دەکات."
        )

    # BACK
    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("💎 VIP Predictions", callback_data="vip")],
            [InlineKeyboardButton("🆓 Free Predictions", callback_data="free")],
            [InlineKeyboardButton("💳 VIP Payment", callback_data="payment")],
            [InlineKeyboardButton(
                "📢 Telegram Channel",
                url="https://t.me/betwen211"
            )],
            [InlineKeyboardButton(
                "🎵 TikTok",
                url="https://www.tiktok.com/@betwen211"
            )],
        ]

        await query.edit_message_text(
            "👑 GOLDEN VIP\n\n"
            "👇 یەکێک لە هەڵبژاردەکان هەڵبژێرە:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


# =========================
# RECEIVE PAYMENT PHOTO
# =========================

async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    payment_method = context.user_data.get(
        "payment_method",
        "Unknown"
    )

    user = update.effective_user

    caption = (
        "💳 NEW VIP PAYMENT\n\n"
        f"📱 Method: {payment_method}\n"
        f"👤 Name: {user.full_name}\n"
        f"🆔 User ID: {user.id}\n"
        f"🔗 Username: @{user.username if user.username else 'None'}"
    )

    photo = update.message.photo[-1]

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=caption,
    )

    await update.message.reply_text(
        "✅ وێنەکەت بە سەرکەوتوویی نێردرا.\n\n"
        "⏳ تکایە چاوەڕێی پشکنینی Admin بکە."
    )


# =========================
# HELP
# =========================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 GOLDEN VIP\n\n"
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

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    application.add_handler(
        MessageHandler(filters.PHOTO, receive_photo)
    )

    application.run_polling()


if __name__ == "__main__":
    main()
