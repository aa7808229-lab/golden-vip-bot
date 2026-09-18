import os
from telegram import Bot

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

bot = Bot(token=BOT_TOKEN)

bot.send_message(
    chat_id=CHANNEL_ID,
    text=make_post()
)
