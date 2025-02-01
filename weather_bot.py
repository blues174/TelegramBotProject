import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


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


def start(update, context):
    update.message.reply_text(
        "Привет! Я бот, который показывает погоду. Используй команду /weather [город] для запроса погоды."
    )



def openweather_weather(update, context):
    if not context.args:
        update.message.reply_text(
            "Пожалуйста, укажите город, для которого вы хотите узнать погоду. Пример: /weather Москва"
        )
        return

    city_name = " ".join(context.args)
    weather_info = get_weather_openweather(city_name)
    update.message.reply_text(weather_info, parse_mode=telegram.ParseMode.HTML)


def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("weather", openweather_weather))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
