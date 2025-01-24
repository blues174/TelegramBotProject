
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor


API_TOKEN = '7846747880:AAHg1aRxkPrJAD0g0I-DcZ5wZogvVfzw2Nk'
    
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

