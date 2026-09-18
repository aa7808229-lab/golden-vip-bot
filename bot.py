import os
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

matches = [
    "Bayern Munich vs Union Berlin",
    "Monza vs Sassuolo",
    "Monaco vs Lens",
    "Brentford vs Chelsea",
    "Bristol City vs Watford",
    "Espanyol vs Elche",
]


def make_post():
    text = "⚽ AP PREDICTOR ⚽\n\n"
    text += "🔐 VIP PREDICTIONS\n\n"

    for match in matches:
        text += f"⚽ {match}\n"
        text += "Prediction: VIP\n\n"

    return text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ بەخێربێیت بۆ Golden VIP!\n\n"
        "🔐 VIP Predictions"
    )


async def send_channel_post():
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=make_post()
    )


async def main():
    await send_channel_post()

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    import asyncio
    await asyncio.Event().wait()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
