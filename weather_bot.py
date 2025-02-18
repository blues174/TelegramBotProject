import telegram
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode
import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN="7846747880:AAHg1aRxkPrJAD0g0I-DcZ5wZogvVfzw2Nk"
OPENWEATHER_API_KEY="d596221b0fdd36984e64fdb65640210b"

async def get_weather_openweather(city_name: str) -> str:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                if data and data.get("weather") and data.get("main"):
                    weather = data["weather"][0]
                    main = data["main"]
                    condition = weather.get("description")
                    temp = main.get("temp")
                    feels_like = main.get("feels_like")
                    wind_speed = data.get("wind", {}).get("speed")
                    humidity = main.get("humidity")
                    return f"""
<b>Погода от OpenWeatherMap:</b>
🏙Город: {city_name}
☁Состояние: {condition}
❄Температура: {temp}°
🌧Ощущается как: {feels_like}°C
🌬Скорость ветра: {wind_speed} м/с
💦Влажность: {humidity}%
                    """
                elif data and data.get("message"):
                    return f"❌ Ошибка: {data['message']}"
                else:
                    return "⚠ Не удалось получить данные от OpenWeatherMap"
    except aiohttp.ClientError as e:
        return f"⚠ Извините, я не знаю такого города, возможно вы написали его название с ошибкой. Попробуйте ещё раз."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("Старт 🚀"), KeyboardButton("Погода ☀️")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋Привет! Я бот, который показывает погоду. Нажмите на кнопку Погода ☀️, чтобы узнать погоду в городе.",
        reply_markup=reply_markup
    )


async def openweather_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🌍 Введите название города:")
    context.user_data['waiting_for_city'] = True


async def get_city_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('waiting_for_city'):
        city_name = update.message.text
        weather_info = await get_weather_openweather(city_name)
        await update.message.reply_text(weather_info, parse_mode=ParseMode.HTML)
        context.user_data['waiting_for_city'] = False
    else:
        await update.message.reply_text("Пожалуйста, сначала нажмите Погода ☀️.")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Update {update} caused error {context.error}")

async def handle_start_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['waiting_for_city'] = False
    await start(update, context)

async def handle_weather_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await openweather_weather(update, context)

def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Старт 🚀$"), handle_start_button))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Погода ☀️$"), handle_weather_button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_city_name))
    application.add_error_handler(error)

    application.run_polling()


if __name__ == "__main__":
    main()
