import os
import requests
import time
import schedule
import logging
from bs4 import BeautifulSoup
from telegram import Bot

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
bot = Bot(token=TOKEN)

logging.basicConfig(level=logging.INFO)

def get_gold_news():
    url = "https://www.gold.org/news-and-events"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        news_item = soup.find('div', class_='news-item')
        title = news_item.find('h3').text.strip()
        link = "https://www.gold.org" + news_item.find('a')['href']
        return f"📰 **خبر جديد عن الذهب**\n\n**{title}**\n\n{link}"
    except Exception as e:
        logging.error(f"Error fetching news: {e}")
        return None

def send_news():
    news = get_gold_news()
    if news:
        try:
            bot.send_message(chat_id=CHANNEL_ID, text=news, parse_mode='Markdown')
            logging.info("News sent successfully")
        except Exception as e:
            logging.error(f"Error sending message: {e}")

def main():
    logging.info("Bot is starting...")
    send_news()
    schedule.every(30).minutes.do(send_news)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
