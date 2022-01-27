import random
import requests as req
from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from bs4 import BeautifulSoup as soup
from typing import List
import telebot
from aiogram.types import ReplyKeyboardMarkup

TOKEN = "5148042073:AAHRofvIz7wYpHOnzx8mCPt0Q8dWEubQdhs"
menu_user = ReplyKeyboardMarkup(resize_keyboard=True).add("виу!")
async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
bot2 = telebot.TeleBot(__name__)
bot2.config['api_key'] = TOKEN
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

def get_text(url) -> List:
    """Парсинг фраз"""
    phrases = []
    rs = req.get(url)
    root = soup(rs.content, "html.parser")
    answer = root.find_all('div', style="background-color:#a0f7b3;border-color:#ffffff;color:#333333;border-radius:20px;-moz-border-radius:20px;-webkit-border-radius:20px;")
    for i in answer:
        phrases.append(i.text)
    return phrases

@dp.message_handler(state='*', commands='start')
async def process_start_command(msg: types.Message):
    await msg.reply("привет, пупс, нажимай на кнопку и получай любовь", reply_markup=menu_user)

@dp.message_handler(state='*', content_types=["text"])
async def handler_message(msg: types.Message):
    phrases = get_text('https://citatnica.ru/frazy/krasivye-frazy-dlya-lyubimoj-300-fraz')
    text = msg.text.lower()
    if text == "виу!":
        rand = random.randint(0, 42)
        await bot.send_message(msg.from_user.id, phrases[rand])
    else:
        await bot.send_message(msg.from_user.id, "ты пупс дурак шоле, для кого кнопка а???")

if __name__ == "__main__":
    executor.start_polling(dp, on_shutdown=shutdown, skip_updates=shutdown)