from config.config_telegram import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import requests
import config
from datetime import datetime

def enviar_mensaje(mensaje: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"⚠️ Error enviando mensaje a Telegram: {e}")

def formato_log(mensaje: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"🧾 <b>LOG {timestamp}</b>\n{mensaje}"
