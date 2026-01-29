import os
import time
import requests
from bs4 import BeautifulSoup
import telegram

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = telegram.Bot(token=TOKEN)

KEYWORDS = ["air force", "dunk", "air max", "tn", "campus", "samba", "gazelle", "530", "550", "2002"]
MAX_PRICE = 40

def extract_price(text):
    import re
    match = re.search(r'\d+', text)
    return int(match.group()) if match else None

def check_site():
    url = "https://www.vinted.it/catalog?search_text=nike"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    for item in soup.find_all("a", href=True):
        text = item.text.lower()
        for key in KEYWORDS:
            if key in text:
                price = extract_price(text)
                if price and price <= MAX_PRICE:
                    link = "https://www.vinted.it" + item["href"]
                    msg = f"👟 AFFARE TROVATO\n{key}\n💰 {price}€\n🔗 {link}"
                    bot.send_message(chat_id=CHAT_ID, text=msg)

while True:
    try:
        check_site()
        time.sleep(300)
    except Exception as e:
        print(e)
        time.sleep(60)
