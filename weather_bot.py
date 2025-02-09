import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN="ВАШ ТОКЕН"
OPENWEATHER_API_KEY="ВАШ ТОКЕН"


def get_weather_openweather(city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
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
            Город: {city_name}
            Состояние: {condition}
            Температура: {temp}°C
            Ощущается как: {feels_like}°C
            Скорость ветра: {wind_speed} м/с
            Влажность: {humidity}%
            """
        elif data and data.get("message"):
            return f"Ошибка: {data['message']}"
        else:
            return "Не удалось получить данные от OpenWeatherMap"
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе к OpenWeatherMap: {e}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start."""
    await update.message.reply_text(
        "Привет! Я бот, который показывает погоду. Используй команду /weather [город] для запроса погоды."
    )


async def openweather_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /weather."""
    if not context.args:
        await update.message.reply_text(
            "Пожалуйста, укажите город, для которого вы хотите узнать погоду. Пример: /weather Москва"
        )
        return

    city_name = " ".join(context.args)
    weather_info = await get_weather_openweather(city_name)
    await update.message.reply_text(weather_info, parse_mode=telegram.ParseMode.HTML)


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main() -> None:
    """Run the bot."""
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", openweather_weather))

    application.add_error_handler(error)

    application.run_polling()


if __name__ == "__main__":
    main()
