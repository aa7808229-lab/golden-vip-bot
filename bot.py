import os
import threading

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

# =========================
# SETTINGS
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 6773856976
CHANNEL_ID = "@betwen211"


# =========================
# FLASK
# =========================

app = Flask(__name__)


@app.route("/")
def home():
    return "Golden VIP Bot is running!"


def run_flask():
    app.run(host="0.0.0.0", port=8080)


# =========================
# CHANNEL BUTTONS
# =========================

def channel_buttons():

    keyboard = [
        [
            InlineKeyboardButton(
                "💎 VIP Predictions",
                callback_data="vip"
            )
        ],
        [
            InlineKeyboardButton(
                "🆓 Free Predictions",
                callback_data="free"
            )
        ],
        [
            InlineKeyboardButton(
                "💳 VIP Payment",
                callback_data="payment"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Telegram Channel",
                url="https://t.me/betwen211"
            )
        ],
        [
            InlineKeyboardButton(
                "🎵 TikTok",
                url="https://www.tiktok.com/@betwen211"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# VIP PLANS
# =========================

def vip_buttons():

    keyboard = [
        [
            InlineKeyboardButton(
                "💎 1 Month — $100",
                callback_data="plan_1"
            )
        ],
        [
            InlineKeyboardButton(
                "💎 3 Months — $250",
                callback_data="plan_3"
            )
        ],
        [
            InlineKeyboardButton(
                "💎 1 Year — $500",
                callback_data="plan_12"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="back"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# PAYMENT METHODS
# =========================

def payment_buttons():

    keyboard = [
        [
            InlineKeyboardButton(
                "📱 Korek",
                callback_data="pay_korek"
            )
        ],
        [
            InlineKeyboardButton(
                "📱 Zain",
                callback_data="pay_zain"
            )
        ],
        [
            InlineKeyboardButton(
                "📱 Asiacell",
                callback_data="pay_asiacell"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="back"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 GOLDEN VIP\n\n"
        "بەخێربێیت 👑",
        reply_markup=channel_buttons()
    )


# =========================
# BUTTON HANDLER
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    # VIP
    if query.data == "vip":

        await query.message.reply_text(
            "💎 VIP Predictions\n\n"
            "ماوەی VIP هەڵبژێرە:",
            reply_markup=vip_buttons()
        )

    # FREE
    elif query.data == "free":

        await query.message.reply_text(
            "🆓 Free Predictions\n\n"
            "⚽ Free Predictions بەردەستن."
        )

    # VIP PAYMENT
    elif query.data == "payment":

        await query.message.reply_text(
            "💳 VIP Payment\n\n"
            "شێوازی پارەدان هەڵبژێرە:",
            reply_markup=payment_buttons()
        )

    # 1 MONTH
    elif query.data == "plan_1":

        context.user_data["plan"] = "1 Month"
        context.user_data["price"] = "$100"

        await query.message.reply_text(
            "💎 1 Month — $100\n\n"
            "ئێستا شێوازی پارەدان هەڵبژێرە:",
            reply_markup=payment_buttons()
        )

    # 3 MONTHS
    elif query.data == "plan_3":

        context.user_data["plan"] = "3 Months"
        context.user_data["price"] = "$250"

        await query.message.reply_text(
            "💎 3 Months — $250\n\n"
            "ئێستا شێوازی پارەدان هەڵبژێرە:",
            reply_markup=payment_buttons()
        )

    # 1 YEAR
    elif query.data == "plan_12":

        context.user_data["plan"] = "1 Year"
        context.user_data["price"] = "$500"

        await query.message.reply_text(
            "💎 1 Year — $500\n\n"
            "ئێستا شێوازی پارەدان هەڵبژێرە:",
            reply_markup=payment_buttons()
        )

    # KOREK
    elif query.data == "pay_korek":

        context.user_data["payment"] = "Korek"

        await query.message.reply_text(
            "📱 Korek\n\n"
            "📸 تکایە وێنەی پسوڵەی پارەدان بنێرە."
        )

    # ZAIN
    elif query.data == "pay_zain":

        context.user_data["payment"] = "Zain"

        await query.message.reply_text(
            "📱 Zain\n\n"
            "📸 تکایە وێنەی پسوڵەی پارەدان بنێرە."
        )

    # ASIACELL
    elif query.data == "pay_asiacell":

        context.user_data["payment"] = "Asiacell"

        await query.message.reply_text(
            "📱 Asiacell\n\n"
            "📸 تکایە وێنەی پسوڵەی پارەدان بنێرە."
        )

    # BACK
    elif query.data == "back":

        context.user_data.clear()

        await query.message.reply_text(
            "🏠 سەرەکی:",
            reply_markup=channel_buttons()
        )


# =========================
# PHOTO HANDLER
# =========================

async def photo_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    user = update.effective_user
    photo = update.message.photo[-1]

    # ==================================================
    # ADMIN → POST TO CHANNEL
    # ==================================================

    if user.id == ADMIN_ID:

        caption = update.message.caption or ""

        await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo.file_id,
            caption=caption,
            reply_markup=channel_buttons()
        )

        await update.message.reply_text(
            "✅ وێنەکە لە @betwen211 بڵاوکرایەوە."
        )

        return

    # ==================================================
    # CUSTOMER PAYMENT → ADMIN ONLY
    # ==================================================

    payment = context.user_data.get("payment")

    if not payment:

        await update.message.reply_text(
            "❗ تکایە سەرەتا VIP Payment هەڵبژێرە."
        )

        return

    plan = context.user_data.get(
        "plan",
        "Not selected"
    )

    price = context.user_data.get(
        "price",
        "Not selected"
    )

    username = (
        f"@{user.username}"
        if user.username
        else "No username"
    )

    name = user.full_name or "Unknown"

    admin_caption = (
        "💳 NEW VIP PAYMENT\n\n"
        f"👤 Name: {name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 User ID: {user.id}\n\n"
        f"💎 Plan: {plan}\n"
        f"💵 Price: {price}\n"
        f"📱 Payment: {payment}"
    )

    # تەنها بۆ Admin
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=admin_caption
    )

    await update.message.reply_text(
        "✅ پسوڵەکەت وەرگیرا.\n\n"
        "⏳ تکایە چاوەڕێ بکە تا پشتڕاست بکرێتەوە."
    )

    context.user_data.clear()


# =========================
# HELP
# =========================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "📌 Help\n\n"
        "/start - دەستپێکردن\n"
        "/help - یارمەتی"
    )


# =========================
# MAIN
# =========================

def main():

    threading.Thread(
        target=run_flask,
        daemon=True
    ).start()

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    # تەنها یەک photo handler
    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo_handler
        )
    )

    print("🤖 GOLDEN VIP BOT IS RUNNING...")

    application.run_polling()


if __name__ == "__main__":
    main()
