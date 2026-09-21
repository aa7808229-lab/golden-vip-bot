import os
import threading
import secrets

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

BOT_TOKEN = os.getenv("
8971754803:AAHSFO7xvHIuql644py6RarhCEVRxwQiflg")

ADMIN_ID = 6773856976
CHANNEL_ID = "@betwen211"

CHANNEL_URL = "https://t.me/betwen211"
TIKTOK_URL = "https://www.tiktok.com/@betwen211"

pending_payments = {}


# =========================
# FLASK
# =========================

app = Flask(__name__)


@app.route("/")
def home():
    return "Golden VIP Bot is running!"


def run_flask():
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)


# =========================
# 5 MAIN BUTTONS
# =========================

def main_buttons():
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
                url=CHANNEL_URL
            )
        ],
        [
            InlineKeyboardButton(
                "🎵 TikTok",
                url=TIKTOK_URL
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
# ADMIN APPROVE / REJECT
# =========================

def admin_payment_buttons(payment_id):
    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Approve",
                callback_data=f"approve:{payment_id}"
            ),
            InlineKeyboardButton(
                "❌ Reject",
                callback_data=f"reject:{payment_id}"
            ),
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    args = context.args

    # From VIP button in channel
    if args and args[0] == "vip":
        await update.message.reply_text(
            "💎 VIP Predictions\n\n"
            "پلانی VIP هەڵبژێرە:",
            reply_markup=vip_buttons()
        )
        return

    # From FREE button in channel
    if args and args[0] == "free":
        await update.message.reply_text(
            "🆓 Free Predictions\n\n"
            "⚽ Free Predictions بەردەستن."
        )
        return

    # From PAYMENT button in channel
    if args and args[0] == "payment":
        await update.message.reply_text(
            "💳 VIP Payment\n\n"
            "پلانی VIP هەڵبژێرە:",
            reply_markup=vip_buttons()
        )
        return

    # Normal start
    await update.message.reply_text(
        "🔥 GOLDEN VIP 🔥\n\n"
        "👑 بەخێربێیت\n\n"
        "💎 VIP Predictions\n"
        "🆓 Free Predictions\n"
        "💳 VIP Payment\n\n"
        "بەشەکەت هەڵبژێرە 👇",
        reply_markup=main_buttons()
    )


# =========================
# ADMIN POST
# =========================

async def post_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    context.user_data["admin_post_mode"] = True

    await update.message.reply_text(
        "📢 POST MODE چالاک کرا.\n\n"
        "🖼️ ئێستا وێنەکە بنێرە.\n"
        "✍️ Caption ـەکەت لەگەڵ وێنەکە بنووسە.\n\n"
        "بۆتەکە خۆکارانە:\n"
        "🖼️ وێنە + ✍️ دەق + ٥ دوگمە\n"
        "دەنێرێتە کەناڵ."
    )


# =========================
# BUTTON HANDLER
# =========================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    # VIP
    if data == "vip":

        await query.message.reply_text(
            "💎 VIP Predictions\n\n"
            "ماوەی VIP هەڵبژێرە:",
            reply_markup=vip_buttons()
        )

    # FREE
    elif data == "free":

        await query.message.reply_text(
            "🆓 Free Predictions\n\n"
            "⚽ Free Predictions بەردەستن."
        )

    # PAYMENT
    elif data == "payment":

        await query.message.reply_text(
            "💳 VIP Payment\n\n"
            "پلانی VIP هەڵبژێرە:",
            reply_markup=vip_buttons()
        )

    # 1 MONTH
    elif data == "plan_1":

        context.user_data["plan"] = "1 Month"
        context.user_data["price"] = "$100"

        await query.message.reply_text(
            "💎 1 Month — $100\n\n"
            "شێوازی پارەدان هەڵبژێرە:",
            reply_markup=payment_buttons()
        )

    # 3 MONTHS
    elif data == "plan_3":

        context.user_data["plan"] = "3 Months"
        context.user_data["price"] = "$250"

        await query.message.reply_text(
            "💎 3 Months — $250\n\n"
            "شێوازی پارەدان هەڵبژێرە:",
            reply_markup=payment_buttons()
        )

    # 1 YEAR
    elif data == "plan_12":

        context.user_data["plan"] = "1 Year"
        context.user_data["price"] = "$500"

        await query.message.reply_text(
            "💎 1 Year — $500\n\n"
            "شێوازی پارەدان هەڵبژێرە:",
            reply_markup=payment_buttons()
        )

    # KOREK
    elif data == "pay_korek":

        context.user_data["payment"] = "Korek"

        await query.message.reply_text(
            "📱 Korek\n\n"
            "📸 تکایە وێنەی پسوڵەکە بنێرە."
        )

    # ZAIN
    elif data == "pay_zain":

        context.user_data["payment"] = "Zain"

        await query.message.reply_text(
            "📱 Zain\n\n"
            "📸 تکایە وێنەی پسوڵەکە بنێرە."
        )

    # ASIACELL
    elif data == "pay_asiacell":

        context.user_data["payment"] = "Asiacell"

        await query.message.reply_text(
            "📱 Asiacell\n\n"
            "📸 تکایە وێنەی پسوڵەکە بنێرە."
        )

    # BACK
    elif data == "back":

        context.user_data.clear()

        await query.message.reply_text(
            "🏠 سەرەکی:",
            reply_markup=main_buttons()
        )


# =========================
# PHOTO HANDLER
# =========================

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    user = update.effective_user
    photo = update.message.photo[-1]

    # =========================
    # ADMIN → CHANNEL
    # =========================

    if user.id == ADMIN_ID:

        if context.user_data.get("admin_post_mode"):

            caption = update.message.caption or "🔥 GOLDEN VIP"

            await context.bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=photo.file_id,
                caption=caption,
                reply_markup=main_buttons()
            )

            context.user_data["admin_post_mode"] = False

            await update.message.reply_text(
                "✅ پۆستەکە بە سەرکەوتوویی نێردرا بۆ کەناڵ."
            )

            return

        await update.message.reply_text(
            "بۆ ناردنی پۆست بۆ کەناڵ:\n\n"
            "/post\n\n"
            "پاشان وێنەکە بنێرە."
        )

        return

    # =========================
    # CUSTOMER RECEIPT
    # =========================

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

    payment_id = secrets.token_hex(6)

    pending_payments[payment_id] = {
        "user_id": user.id,
        "name": name,
        "username": username,
        "plan": plan,
        "price": price,
        "payment": payment,
    }

    admin_caption = (
        "💳 NEW VIP PAYMENT\n\n"
        f"👤 Name: {name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 User ID: {user.id}\n\n"
        f"💎 Plan: {plan}\n"
        f"💵 Price: {price}\n"
        f"📱 Payment: {payment}"
    )

    # ONLY ADMIN
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=admin_caption,
        reply_markup=admin_payment_buttons(payment_id)
    )

    # CUSTOMER
    await update.message.reply_text(
        "✅ پسوڵەکەت وەرگیرا.\n\n"
        "⏳ چاوەڕێ بکە تا Admin پشتڕاستی بکاتەوە."
    )

    context.user_data.clear()


# =========================
# APPROVE / REJECT
# =========================

async def admin_payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    if query.from_user.id != ADMIN_ID:
        await query.answer(
            "❌ تۆ Admin نیت.",
            show_alert=True
        )
        return

    await query.answer()

    action, payment_id = query.data.split(":", 1)

    payment = pending_payments.get(payment_id)

    if not payment:
        await query.message.reply_text(
            "❌ ئەم داواکارییە نەدۆزرایەوە."
        )
        return

    user_id = payment["user_id"]
    plan = payment["plan"]
    price = payment["price"]
    method = payment["payment"]

    # APPROVE
    if action == "approve":

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "✅ VIP Payment Approved\n\n"
                "🎉 پارەدانەکەت پشتڕاست کرایەوە.\n\n"
                f"💎 Plan: {plan}\n"
                f"💵 Price: {price}\n"
                f"📱 Payment: {method}\n\n"
                "👑 بەخێربێیت بۆ Golden VIP."
            )
        )

        await query.message.edit_caption(
            caption=(
                "✅ APPROVED\n\n"
                f"👤 Name: {payment['name']}\n"
                f"🔗 Username: {payment['username']}\n"
                f"🆔 User ID: {user_id}\n\n"
                f"💎 Plan: {plan}\n"
                f"💵 Price: {price}\n"
                f"📱 Payment: {method}"
            )
        )

    # REJECT
    elif action == "reject":

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "❌ VIP Payment Rejected\n\n"
                "ببورە، پسوڵەکەت پشتڕاست نەکرایەوە.\n\n"
                "تکایە پسوڵەی دروست دووبارە بنێرە."
            )
        )

        await query.message.edit_caption(
            caption=(
                "❌ REJECTED\n\n"
                f"👤 Name: {payment['name']}\n"
                f"🔗 Username: {payment['username']}\n"
                f"🆔 User ID: {user_id}\n\n"
                f"💎 Plan: {plan}\n"
                f"💵 Price: {price}\n"
                f"📱 Payment: {method}"
            )
        )

    pending_payments.pop(payment_id, None)


# =========================
# HELP
# =========================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📌 GOLDEN VIP\n\n"
        "/start - دەستپێکردن\n"
        "/help - یارمەتی\n"
        "/post - ناردنی پۆست بۆ کەناڵ"
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
        CommandHandler("post", post_command)
    )

    # Approve / Reject
    application.add_handler(
        CallbackQueryHandler(
            admin_payment_handler,
            pattern=r"^(approve|reject):"
        )
    )

    # Normal buttons
    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    # Photos
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
