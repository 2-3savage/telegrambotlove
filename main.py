import os
import random
from typing import List

import requests as req
import telebot
from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from bs4 import BeautifulSoup as soup

TOKEN = "5148042073:AAHRofvIz7wYpHOnzx8mCPt0Q8dWEubQdhs"
menu_user = ReplyKeyboardMarkup(resize_keyboard=True).add("виу!").add("миу!").add("гиу!")
bot2 = telebot.TeleBot(__name__)
bot2.config['api_key'] = TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


def images(url):
    r = req.get(url)
    b = soup(r.content, "html.parser")
    image = b.find_all("img", class_ = 'serp-item__thumb justifier__thumb')
    images = []
    for i in image:
        images.append(i.get("src")[2:])
    return images


def get_text(url, headers) -> List:
    """Парсинг фраз"""
    phrases = []
    rs = req.get(url, headers = headers)
    root = soup(rs.content, "html.parser")
    answer = root.find('div', class_="content-inner").find_all("p")
    for i in answer:
        try:
            int(i.text.split(".")[0])
            phrases.append(" ".join(i.text.split(" ")[1:]))
        except ValueError:
            pass
    return phrases


@dp.message_handler(state='*', commands='start')
async def process_start_command(msg: types.Message):
    await msg.reply("привет, пупс, нажимай на кнопку и получай любовь 💖", reply_markup=menu_user)


@dp.message_handler(state='*', content_types=["text"])
async def main(msg: types.Message):
    url_cats = images("https://yandex.ru/images/search?text=%D0%BC%D0%B8%D0%BB%D1%8B%D0%B5%20%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8%20%D0%BB%D1%8E%D0%B1%D0%BE%D0%B2%D0%BD%D1%8B%D0%B5%20%D0%BA%D0%BE%D1%82%D1%8F%D1%82%D0%B0&lr=62")
    phrases = get_text('https://mensby.com/women/relations/300-krasivyh-slov-devushke-luchshie-komplimenty-devushke', {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50 (Edition Yx GX 03)"
})
    url_dogs = images("https://yandex.ru/images/search?from=tabbar&text=%D0%BC%D0%B8%D0%BB%D1%8B%D0%B5%20%D0%BA%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D0%BA%D0%B8%20%D1%81%20%D1%81%D0%BE%D0%B1%D0%B0%D1%87%D0%BA%D0%B0%D0%BC%D0%B8%20%D0%BB%D1%8E%D0%B1%D0%BE%D0%B2%D1%8C")
    text = msg.text.lower()
    if text == "виу!":
        await bot.send_message(msg.from_user.id, phrases[random.randint(0, len(phrases) - 1)])
    elif text == "миу!":
        with open(f"1.jpg", "wb") as out:
            photo = req.get(f"http://{url_cats[random.randint(0, len(url_cats)) - 1]}").content
            out.write(photo)
        with open("1.jpg", 'rb') as out:
            await bot.send_photo(msg.from_user.id, photo = out)
    elif text == "гиу!":
        with open(f"1.jpg", "wb") as out:
            photo = req.get(f"http://{url_dogs[random.randint(0, len(url_dogs)) - 1]}").content
            out.write(photo)
        with open("1.jpg", 'rb') as out:
            await bot.send_photo(msg.from_user.id, photo = out)
    else:
        await bot.send_message(msg.from_user.id, "ты пупс дурак шоле, для кого кнопка а???")


if __name__ == "__main__":
    executor.start_polling(dp, on_shutdown=shutdown, skip_updates=shutdown)