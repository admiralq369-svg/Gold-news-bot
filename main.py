import os
import asyncio
import feedparser
import aiohttp
from telegram import Bot
from googletrans import Translator
from datetime import datetime

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID") # ايدي القناة
LANG = os.getenv("LANG", "en") # اللغة ar

bot = Bot(token=TOKEN)
translator = Translator()
seen_links = set()

# مصادر اخبار اقتصادية و ذهب
FEEDS = [
    "https://www.cnbc.com/id/10000664/device/rss/rss.html", # CNBC Markets
    "https://www.kitco.com/rss/rss.xml", # Kitco Gold
    "https://feeds.reuters.com/reuters/businessNews" # Reuters Business
]

async def translate_text(text):
    if LANG == "ar" and text:
        try:
            translated = translator.translate(text, dest='ar')
            return translated.text
        except:
            return text
    return text

async def send_news():
    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]: # بجيب اخر 3 اخبار من كل مصدر
            if entry.link not in seen_links:
                seen_links.add(entry.link)
                
                title = await translate_text(entry.title)
                summary = await translate_text(entry.summary[:300]) # باخد اول 300 حرف بس
                source = entry.get("source", {}).get("title", "مصدر")
                
                message = f"**{title}**\n\n"
                message += f"{summary}...\n\n"
                message += f"**التأثير المحتمل**: "
                if "gold" in entry.title.lower() or "ذهب" in title:
                    message += "إيجابي للذهب"
                else:
                    message += "متابعة للاسواق"
                message += f"\n**المصدر**: {source}"
                message += f"\n#ذهب #اقتصاد"
                
                # ابعت على القناة
                if CHANNEL_ID:
                    await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")
                
                # ابعتلك انت كمان
                # await bot.send_message(chat_id="حط_ايديك_هون", text=message, parse_mode="Markdown")
                
                await asyncio.sleep(2)

async def main():
    print("Bot started...")
    while True:
        await send_news()
        await asyncio.sleep(600) # بفحص كل 10 دقايق

if __name__ == "__main__":
    asyncio.run(main())
