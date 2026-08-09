
import os
import feedparser
import time
import asyncio
from telegram import Bot
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
NEWS_SOURCES = os.getenv("NEWS_SOURCE", "").split(",")

bot = Bot(token=TOKEN)
sent_links = set() # عشان ما يكرر الاخبار

async def fetch_news():
    for source in NEWS_SOURCES:
        source = source.strip()
        if not source: continue
        try:
            feed = feedparser.parse(source)
            for entry in feed.entries[:3]: # يجيب اول 3 اخبار من كل مصدر
                if entry.link not in sent_links:
                    sent_links.add(entry.link)
                    title = entry.title
                    link = entry.link
                    source_name = feed.feed.get('title', 'اخبار')
                    message = f"**{source_name}**\n\n{title}\n\n{link}"
                    await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")
                    print(f"Sending news from {source_name}")
                    await asyncio.sleep(5) # ينتظر 5 ثواني بين كل خبر
                    return # يبعت خبر واحد بس كل ساعة
        except Exception as e:
            print(f"Error with {source}: {e}")

async def main():
    print("Bot started")
    while True:
        print(f"Checking news at {datetime.now()}")
        await fetch_news()
        await asyncio.sleep(3600) # ينتظر ساعة

if __name__ == "__main__":
    asyncio.run(main())    Update to multi-source bot
