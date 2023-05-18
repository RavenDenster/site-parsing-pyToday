from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram.dispatcher.filters import Text
from config import token, user_id
import json
import datetime
import asyncio
from main import check_news_update

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Все новости", "Последние 5 новостей", "Свежие новости"]
    keyboard =types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Лента новостей', reply_markup=keyboard)


@dp.message_handler(Text(equals="Все новости"))
async def get_all_news(message: types.Message):
    with open('news_dict.json', encoding='utf-8') as file:
        news_dict = json.load(file)
    
    for k, v in sorted(news_dict.items()):
        # news = f"{datetime.datetime.fromtimestamp(v['article_date_timestamp'])}\n" \
        #        f"{v['atricle_title']}\n" \
        #        f"{v['article_desc']}\n" \
        #        f"{v['article_url']}"

        news = f"{datetime.datetime.fromtimestamp(v['article_date_timestamp'])}\n" \
               f"{hlink(v['atricle_title'], v['article_url'])}"
        
        await message.answer(news)


@dp.message_handler(Text(equals="Последние 5 новостей"))
async def get_last_five_news(message: types.Message):
    with open('news_dict.json', encoding='utf-8') as file:
        news_dict = json.load(file)
    
    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{datetime.datetime.fromtimestamp(v['article_date_timestamp'])}\n" \
               f"{hlink(v['atricle_title'], v['article_url'])}"
        await message.answer(news)


@dp.message_handler(Text(equals="Свежие новости"))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()
    print(fresh_news)
    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{datetime.datetime.fromtimestamp(v['article_date_timestamp'])}\n" \
               f"{hlink(v['atricle_title'], v['article_url'])}"
        await message.answer(news)
    else:
        await message.answer('Пока нет свежих новостей...')


async def news_every_minute():
    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):
                news = f"{datetime.datetime.fromtimestamp(v['article_date_timestamp'])}\n" \
                       f"{hlink(v['atricle_title'], v['article_url'])}"
                await bot.send_message(user_id, news, disable_notification=True)
        else:
            await bot.send_message(user_id, "Пока нет свежих новостей", disable_notification=True)

        await asyncio.sleep(20)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)