from datetime import date, timedelta, datetime
from typing import List
from emoji import emojize

from bot import Bot
from natasha_utils import NatashaExtractor
from constants import BOT_TOKEN, BOT_MESSAGES, DATE_FORMAT, find_bye_messages_regexp, check_all_tokens_set
from weather_forecast_utils import get_weather_forecast, get_pretty_html_forecast_message

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor


API_TOKEN = ''
    
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.chat.id, "Привет! Я бот погоды, я составляю прогноз погоды для каждого региона РФ. Какой регион вас интересует?")

@dp.message_handler()
async def echo(message: types.Message):
    print(message.text)
    user_message = message.text.lower()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

