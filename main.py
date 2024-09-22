import os
import asyncio
import requests
from bs4 import BeautifulSoup as BS
from telegram import Bot
import random
import schedule
import time
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("BOT_TOKEN")  # token
channel_id = '@astrocipher'  # id canala
image_folder = "./pictures"  # Путь к папке с изображениями
paths_img = [
    'oven.jpg',  # Овен
    'telec.jpg',  # Телец
    'bliznecy.jpg',  # Близнецы
    'rak.jpg',  # Рак
    'leo.jpg',  # Лев
    'deva.jpg',  # Дева
    'vesy.jpg',  # Весы
    'scorpion.jpg',  # Скорпион
    'strelec.jpg',  # Стрелец
    'kozerog.jpg',  # Козерог
    'vodoley.jpg',  # Водолей
    'ribi.jpg',  # Рыбы
]
znaky = ['Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева', 'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы']

async def send_message_async(bot, channel_id, text, photo=None):
    if photo:
        await bot.send_photo(chat_id=channel_id, photo=photo, caption=text)
    else:
        await bot.send_message(chat_id=channel_id, text=text)

async def post_horoscope():
    r = requests.get("https://www.chita.ru/horoscope/daily/")
    html = BS(r.content, 'html.parser')
    proqnoz = []

    for el in html.select(".IGRa5 > .BDPZt.KUbeq"):
        infa = el.select("div")[0].text
        proqnoz.append(infa)
    print(proqnoz[0])
    smile = ['😴', '🥱', '☺', '🤣', '😍', '😭', '😡', '😨', '🤔', '😮', '😬', '😏', '😉', '🤡', '🤠', '💝', '👑', '🤯', '👽', '🧜🏼‍♀️',
             '🧞', '🌕', '🌖', '🌗', '🌘', '🌑', '🌒', '🌓', '🌔', '🪐', '💥']

    bot = Bot(token=bot_token)
    for znak, post, img_path in zip(znaky, proqnoz, paths_img):
        image_path = os.path.join(image_folder, img_path)
        a = random.sample(smile, 3)
        emojis = ''.join(a)
        if os.path.exists(image_path):
            await send_message_async(bot, channel_id, f'\n *{znak}* \n• {post}\n\n{emojis}',
                                     photo=open(image_path, 'rb'))
        else:
            await send_message_async(bot, channel_id, f"{post}\n\n :3")
        await asyncio.sleep(2)


def schedule_task():
    # Создаем асинхронный цикл
    loop = asyncio.get_event_loop()
    # Запускаем функцию в 9 утра
    schedule.every().day.at("00:15").do(lambda: loop.run_until_complete(post_horoscope()))

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    schedule_task()
