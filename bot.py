import os
import threading
import secrets

from flask import Flask
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ==================================================
# SETTINGS
# ==================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 6773856976
CHANNEL_ID = "@betwen211"

CHANNEL_URL = "https://t.me/betwen211"
TIKTOK_URL = "https://www.tiktok.com/@betwen211"

# ئەگەر وێنەی Start هەیە دەتوانیت Telegram file_id لێرە دابنێیت
START_IMAGE = os.getenv("START_IMAGE", "")

# بۆ هەڵگرتنی داواکارییەکانی پارەدان
pending_payments = {}


# ==================================================
# FLASK
# ==================================================

app = Flask(__name__)


@app.route("/")
def home():
    return "Golden VIP Bot is running!"


def run_flask():
    port = int(os.getenv("PORT", "8080"))
    app.run(
        host="0.0.0.0",
        port=port
    )


# ==================================================
# MAIN BUTTONS
# ==================================================

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


# ==================================================
# VIP PLANS
# ==================================================

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


# ==================================================
# PAYMENT METHODS
# ==================================================

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


# ==================================================
# ADMIN APPROVE / REJECT BUTTONS
# ==================================================

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


# ==================================================
# START
# ==================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = (
        "🔥 GOLDEN VIP 🔥\n\n"
        "👑 بەخێربێیت بۆ Golden VIP\n\n"
        "💎 VIP Predictions\n"
        "⚽ Free Predictions\n"
        "💳 VIP Payment\n\n"
        "لە خوارەوە بەشەکەت هەڵبژێرە 👇"
    )

    if START_IMAGE:

        await update.message.reply_photo(
            photo=START_IMAGE,
            caption=text,
            reply_markup=main_buttons()
        )

    else:

        await update.message.reply_text(
            text,
            reply_markup=main_buttons()
        )


# ==================================================
# ADMIN POST COMMAND
# ==================================================

async def post_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user.id != ADMIN_ID:
        return

    context.user_data["admin_post_mode"] = True

    await update.message.reply_text(
        "📢 POST MODE\n\n"
        "ئێستا وێنەی پێشبینی بنێرە.\n\n"
        "وێنەکە بە caption ـەکەیەوە دەچێتە:\n"
        "@betwen211\n\n"
        "⚠️ ئەمە تەنها بۆ Admin ـە."
    )


# ==================================================
# BUTTON HANDLER
# ==================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    data = query.data

    # ==============================================
    # VIP
    # ==============================================

    if data == "vip":

        await query.message.reply_text(
            "💎 VIP Predictions\n\n"
            "ماوەی VIP هەڵبژێرە:",
            reply_markup=vip_buttons()
        )

    # ==============================================
    # FREE
    # ==============================================

    elif data == "free":

        await query.message.reply_text(
            "🆓 Free Predictions\n\n"
            "⚽ Free Predictions بەردەستن."
        )

    # ==============================================
    # PAYMENT
    # ==============================================

    elif data == "payment":

        await query.message.reply_text(
            "💳 VIP Payment\n\n"
            "سەرەتا پلانی VIP هەڵبژێرە:",
            reply_markup=vip_buttons()
        )

    # ==============================================
    # 1 MONTH
    # ==============================================

    elif data == "plan_1":

        context.user_data["plan"] = "1 Month"
        context.user_data["price"] = "$100"

        await query.message.reply_text(
            "💎 1 Month — $100\n\n"
            "ئێستا شێوازی پارەدان هەڵبژێرە:",
            reply_markup=payment_buttons()
        )

    # ==============================================
    # 3 MONTHS
    # ==============================================

    elif data == "plan_3":

        context.user_data["plan"] = "3 Months"
        context.user_data["price"] = "$250"

        await query.message.reply_text(
            "💎 3 Months — $250\n\n"
            "ئێستا شێوازی پارەدان هەڵبژێرە:",
            reply_markup=payment_buttons()
        )

    # ==============================================
    # 1 YEAR
    # ==============================================

    elif data == "plan_12":

        context.user_data["plan"] = "1 Year"
        context.user_data["price"] = "$500"

        await query.message.reply_text(
            "💎 1 Year — $500\n\n"
            "ئێستا شێوازی پارەدان هەڵبژێرە:",
            reply_markup=payment_buttons()
        )

    # ==============================================
    # KOREK
    # ==============================================

    elif data == "pay_korek":

        context.user_data["payment"] = "Korek"

        await query.message.reply_text(
            "📱 Korek\n\n"
            "💳 پارەکە بنێرە.\n"
            "📸 پاشان وێنەی پسوڵەکە بنێرە."
        )

    # ==============================================
    # ZAIN
    # ==============================================

    elif data == "pay_zain":

        context.user_data["payment"] = "Zain"

        await query.message.reply_text(
            "📱 Zain\n\n"
            "💳 پارەکە بنێرە.\n"
            "📸 پاشان وێنەی پسوڵەکە بنێرە."
        )

    # ==============================================
    # ASIACELL
    # ==============================================

    elif data == "pay_asiacell":

        context.user_data["payment"] = "Asiacell"

        await query.message.reply_text(
            "📱 Asiacell\n\n"
            "💳 پارەکە بنێرە.\n"
            "📸 پاشان وێنەی پسوڵەکە بنێرە."
        )

    # ==============================================
    # BACK
    # ==============================================

    elif data == "back":

        context.user_data.clear()

        await query.message.reply_text(
            "🏠 سەرەکی:",
            reply_markup=main_buttons()
        )


# ==================================================
# ADMIN APPROVE / REJECT
# ==================================================

async def admin_payment_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    if query.from_user.id != ADMIN_ID:
        await query.answer(
            "❌ تۆ Admin نیت.",
            show_alert=True
        )
        return

    await query.answer()

    data = query.data

    action, payment_id = data.split(":", 1)

    payment = pending_payments.get(payment_id)

    if not payment:

        await query.message.reply_text(
            "❌ ئەم داواکارییە نەدۆزرایەوە."
        )
        return

    customer_id = payment["user_id"]
    name = payment["name"]
    username = payment["username"]
    plan = payment["plan"]
    price = payment["price"]
    method = payment["payment"]

    # ==============================================
    # APPROVE
    # ==============================================

    if action == "approve":

        await context.bot.send_message(
            chat_id=customer_id,
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
                f"👤 Name: {name}\n"
                f"🔗 Username: {username}\n"
                f"🆔 User ID: {customer_id}\n\n"
                f"💎 Plan: {plan}\n"
                f"💵 Price: {price}\n"
                f"📱 Payment: {method}"
            )
        )

    # ==============================================
    # REJECT
    # ==============================================

    elif action == "reject":

        await context.bot.send_message(
            chat_id=customer_id,
            text=(
                "❌ VIP Payment Rejected\n\n"
                "ببورە، پسوڵەی پارەدانەکەت "
                "پشتڕاست نەکرایەوە.\n\n"
                "تکایە پسوڵەی دروست دووبارە بنێرە."
            )
        )

        await query.message.edit_caption(
            caption=(
                "❌ REJECTED\n\n"
                f"👤 Name: {name}\n"
                f"🔗 Username: {username}\n"
                f"🆔 User ID: {customer_id}\n\n"
                f"💎 Plan: {plan}\n"
                f"💵 Price: {price}\n"
                f"📱 Payment: {method}"
            )
        )

    pending_payments.pop(payment_id, None)


# ==================================================
# PHOTO HANDLER
# ==================================================

async def photo_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    user = update.effective_user
    photo = update.message.photo[-1]

    # ==================================================
    # ADMIN POST MODE
    # ==================================================

    if user.id == ADMIN_ID:

        post_mode = context.user_data.get(
            "admin_post_mode",
            False
        )

        if post_mode:

            caption = update.message.caption or (
                "🔥 GOLDEN VIP\n\n"
                "💎 VIP Prediction"
            )

            await context.bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=photo.file_id,
                caption=caption,
                reply_markup=main_buttons()
            )

            context.user_data["admin_post_mode"] = False

            await update.message.reply_text(
                "✅ پۆستەکە بە سەرکەوتوویی "
                "لە کەناڵ بڵاوکرایەوە."
            )

            return

        await update.message.reply_text(
            "📢 بۆ ناردنی پۆست بۆ کەناڵ:\n\n"
            "/post\n\n"
            "پاشان وێنەکە بنێرە."
        )

        return

    # ==================================================
    # CUSTOMER PAYMENT
    # ==================================================

    payment = context.user_data.get("payment")

    if not payment:

        await update.message.reply_text(
            "❗ تکایە سەرەتا:\n"
            "💳 VIP Payment\n"
            "هەڵبژێرە."
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

    # Unique payment ID
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

    # ==============================================
    # SEND RECEIPT ONLY TO ADMIN
    # ==============================================

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=admin_caption,
        reply_markup=admin_payment_buttons(payment_id)
    )

    # ==============================================
    # CUSTOMER CONFIRMATION
    # ==============================================

    await update.message.reply_text(
        "✅ پسوڵەکەت وەرگیرا.\n\n"
        f"💎 Plan: {plan}\n"
        f"💵 Price: {price}\n"
        f"📱 Payment: {payment}\n\n"
        "⏳ چاوەڕێ بکە تا Admin "
        "پارەدانەکەت پشتڕاست بکاتەوە."
    )

    context.user_data.clear()


# ==================================================
# TEXT HANDLER
# ==================================================

async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    # بۆ کڕیار تەنها وێنەی پسوڵە وەرگیراوە
    await update.message.reply_text(
        "📸 تکایە وێنەی پسوڵەی پارەدان بنێرە."
    )


# ==================================================
# HELP
# ==================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "📌 GOLDEN VIP HELP\n\n"
        "/start - دەستپێکردن\n"
        "/help - یارمەتی\n\n"
        "💳 بۆ پارەدان:\n"
        "VIP Payment هەڵبژێرە."
    )


# ==================================================
# MAIN
# ==================================================

def main():

    # Flask
    threading.Thread(
        target=run_flask,
        daemon=True
    ).start()

    # Telegram
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # Commands
    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CommandHandler("post", post_command)
    )

    # Admin approve/reject
    application.add_handler(
        CallbackQueryHandler(
            admin_payment_handler,
            pattern=r"^(approve|reject):"
        )
    )

    # Normal buttons
    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    # Photos
    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo_handler
        )
    )

    # Text
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler
        )
    )

    print("🤖 GOLDEN VIP BOT IS RUNNING...")

    application.run_polling()


# ==================================================
# RUN
# ==================================================

if __name__ == "__main__":
    main()
