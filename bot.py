import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import requests

# --- Konfigurationsbereich ---
TELEGRAM_BOT_TOKEN = "8048781787:AAHEO8-c1wr_TY9daN3pXfMfTAaXQPas2mE"  # Von BotFather erhalten
TON_API_BASE_URL = "https://toncenter.com/api/v2/"  # Beispiel-API-Endpunkt
TON_API_KEY = "67830af0ba91d1d066a2585641eb7123192d5a4a3dcb16bc494b8a01b84c3c95"  # Dein TON API-Schlüssel
CHANNEL_ID = "@Tonexium"  # Dein Telegram-Kanalname oder ID

# Bot- und Dispatcher-Objekte erstellen
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# --- Funktion zum Abrufen von TON Blockchain-Daten ---
def get_ton_news():
    """Ruhe aktuelle TON News ab (Beispieldaten)"""
    # Beispiel-API-Request (anpassen je nach API-Dokumentation)
    response = requests.get(f"{TON_API_BASE_URL}getTransactions", params={"api_key": TON_API_KEY})
    if response.status_code == 200:
        data = response.json()
        # Extrahiere relevante Informationen
        transactions = data.get("result", [])
        news = []
        for tx in transactions[:5]:  # Nur die letzten 5 Transaktionen
            news.append(
                f"💸 Neue Transaktion:\n"
                f"- Von: {tx.get('source')}\n"
                f"- An: {tx.get('destination')}\n"
                f"- Betrag: {tx.get('value')} TON\n"
                f"- Zeit: {tx.get('utime')}\n"
            )
        return "\n\n".join(news)
    else:
        return "⚠️ Fehler beim Abrufen der TON-Daten."

# --- Command-Handler ---
@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """Begrüßungsnachricht senden."""
    await message.reply("👋 Willkommen! Ich bin der Tonexium-Bot. Ich halte dich über die TON Blockchain auf dem Laufenden.")

@dp.message_handler(commands=["news"])
async def send_news(message: types.Message):
    """TON-News an den Benutzer senden."""
    news = get_ton_news()
    await message.reply(f"📰 Aktuelle Nachrichten:\n\n{news}", parse_mode=ParseMode.HTML)

# --- Funktion: News an den Kanal posten ---
async def post_news_to_channel():
    """Postet regelmäßig Updates an den Kanal."""
    while True:
        try:
            news = get_ton_news()
            if news:
                await bot.send_message(CHANNEL_ID, f"🔔 Update von der TON Blockchain:\n\n{news}", parse_mode=ParseMode.HTML)
        except Exception as e:
            print(f"Fehler beim Posten von News: {e}")
        await asyncio.sleep(3600)  # Alle 1 Stunde aktualisieren

# --- Startpunkt ---
if __name__ == "__main__":
    # Hintergrundtask für das Posten in den Kanal starten
    loop = asyncio.get_event_loop()
    loop.create_task(post_news_to_channel())
    # Telegram-Bot starten
    executor.start_polling(dp, skip_updates=True)
