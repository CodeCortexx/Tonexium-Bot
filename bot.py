import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

# --- Konfigurationsbereich ---
TELEGRAM_BOT_TOKEN = "8048781787:AAHEO8-c1wr_TY9daN3pXfMfTAaXQPas2mE"  # Dein Bot Token
TON_API_BASE_URL = "https://toncenter.com/api/v2/"  # TON API Endpunkt
TON_API_KEY = "67830af0ba91d1d066a2585641eb7123192d5a4a3dcb16bc494b8a01b84c3c95"  # Dein TON API-Schlüssel
CHANNEL_ID = "@tonexiumchannel"  # Dein Telegram Kanal (öffentliche Kanal-ID)

# Bot- und Dispatcher-Objekte erstellen
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

# --- Funktion zum Abrufen von Wallet-Daten ---
def get_wallet_info(wallet_address):
    """Ruhe Wallet-Daten ab (z. B. Kontostand und Transaktionshistorie)"""
    try:
        # API-Request für Wallet-Informationen
        response = requests.get(f"{TON_API_BASE_URL}getAddressInformation", 
                                params={"address": wallet_address, "api_key": TON_API_KEY})
        
        # Überprüfen, ob der HTTP-Request erfolgreich war
        if response.status_code == 200:
            data = response.json()
            # Überprüfen, ob das "result" Feld in der Antwort vorhanden ist
            if "result" in data:
                result = data["result"]
                balance = result.get("balance", "Nicht verfügbar")
                transactions = result.get("transactions", [])
                transaction_count = len(transactions)
                return (
                    f"🔑 Wallet-Adresse: {wallet_address}\n"
                    f"💰 Kontostand: {balance} TON\n"
                    f"📊 Transaktionen: {transaction_count} insgesamt"
                )
            else:
                return "⚠️ Fehler beim Abrufen der Wallet-Daten (keine Ergebnisse)."
        else:
            return f"⚠️ Fehler beim Abrufen der Wallet-Daten: HTTP {response.status_code}"

    except requests.exceptions.RequestException as e:
        return f"⚠️ Es gab ein Problem mit der Anfrage: {str(e)}"

# --- Command-Handler ---
@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """Begrüßungsnachricht senden."""
    await message.reply("👋 Willkommen! Ich bin der Tonexium-Bot. Ich halte dich über die TON Blockchain auf dem Laufenden.")

@dp.message_handler(commands=["wallet"])
async def send_wallet_info(message: types.Message):
    """Wallet-Informationen an den Benutzer senden."""
    wallet_address = message.get_args()  # Adresse aus der Nachricht extrahieren
    if wallet_address:
        wallet_info = get_wallet_info(wallet_address)
        await message.reply(f"🗂 Wallet-Informationen:\n\n{wallet_info}", parse_mode=ParseMode.HTML)
    else:
        await message.reply("⚠️ Bitte gib eine Wallet-Adresse an.")

# --- Funktion: News an den Kanal posten ---
async def post_news_to_channel():
    """Postet regelmäßig Updates an den Kanal."""
    while True:
        try:
            # Hier könntest du die Funktion für Neuigkeiten von der TON Blockchain einfügen
            # Zum Beispiel: news = get_ton_news() 
            news = "Aktuelle Neuigkeiten von der TON Blockchain"  # Beispiel-Text
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
