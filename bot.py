
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor


API_TOKEN = '7846747880:AAHg1aRxkPrJAD0g0I-DcZ5wZogvVfzw2Nk'
    
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.chat.id, "Привет! Я простой бот. Задайте мне вопрос.")

@dp.message_handler()
async def echo(message: types.Message):
    print(message.text)
    user_message = message.text.lower()
    if 'привет' in user_message:
        await bot.send_message(message.chat.id, 'Привет!')
    elif 'как дела' in user_message:
        await bot.send_message(message.chat.id, 'У меня все хорошо, спасибо!')
    elif 'что ты умеешь' in user_message:
        await bot.send_message(message.chat.id, 'Я умею общаться с людьми и отвечать на вопросы.')
    elif 'какой твой любимый цвет' in user_message:
        await bot.send_message(message.chat.id, 'Хороший вопрос! Мой любимый цвет - зелёный.')
    elif 'каких животных ты любишь' in user_message:
        await bot.send_message(message.chat.id, 'Я очень люблю кошек.')
    elif 'игрок' in user_message:
        await bot.send_message(message.chat.id, 'Воооооооооооооот так ты игрок заявил.')
    elif 'что ты весь бой делал' in user_message:
        await bot.send_message(message.chat.id, 'Я базу дефал')
    elif 'зачем ты базу дефал' in user_message:
        await bot.send_message(message.chat.id, 'А у меня геймплей такой')
    else:
        await bot.send_message(message.chat.id, 'Извините, я не понимаю ваш вопрос.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

