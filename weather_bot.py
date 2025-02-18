import telegram
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode
import aiohttp
import json
import os
from dotenv import load_dotenv
import datetime

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
<b>Текущая погода от OpenWeatherMap:</b>
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

async def get_weather_forecast(city_name: str, days: int) -> str:
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                if data and data.get("list"):
                    forecast_list = data["list"]
                    forecast_text = f"<b>Прогноз погоды для города {city_name}:</b>\n"
                    for i in range(min(days * 8, len(forecast_list))):
                        forecast = forecast_list[i]
                        date_time_str = forecast["dt_txt"]
                        date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
                        formatted_date = date_time_obj.strftime("%d %B %H:%M")
                        month_names_ru = {
                            "January": "Января",
                            "February": "Февраля",
                            "March": "Марта",
                            "April": "Апреля",
                            "May": "Мая",
                            "June": "Июня",
                            "July": "Июля",
                            "August": "Августа",
                            "September": "Сентября",
                            "October": "Октября",
                            "November": "Ноября",
                            "December": "Декабря",
                        }
                        for en, ru in month_names_ru.items():
                            formatted_date = formatted_date.replace(en, ru)

                        temp = forecast["main"]["temp"]
                        condition = forecast["weather"][0]["description"]
                        forecast_text += f"📅 {formatted_date}: ❄ {temp}°C, ☁ {condition}\n"
                    return forecast_text
                elif data and data.get("message"):
                    return f"❌ Ошибка: {data['message']}"
                else:
                    return "⚠ Не удалось получить данные о прогнозе от OpenWeatherMap"
    except aiohttp.ClientError as e:
        return f"⚠ Ошибка при запросе прогноза: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("Старт 🚀"), KeyboardButton("Погода ☀️"), KeyboardButton("Прогноз 📅")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋Привет! Я бот, который показывает погоду. Нажмите на кнопку Погода ☀️ или Прогноз 📅.",
        reply_markup=reply_markup
    )

async def openweather_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🌍 Введите название города для текущей погоды:")
    context.user_data['waiting_for_city'] = "current"

async def forecast_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🌍 Введите название города для прогноза:")
    context.user_data['waiting_for_city'] = "forecast"

async def get_city_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    city_name = update.message.text
    if context.user_data.get('waiting_for_city') == "current":
        weather_info = await get_weather_openweather(city_name)
        await update.message.reply_text(weather_info, parse_mode=ParseMode.HTML)
        context.user_data['waiting_for_city'] = None
    elif context.user_data.get('waiting_for_city') == "forecast":
        keyboard = [
            [KeyboardButton("Завтра 🗓️"), KeyboardButton("На 3 дня 🗓️🗓️🗓️"), KeyboardButton("На неделю 🗓️🗓️🗓️🗓️🗓️🗓️🗓️")],
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Выберите период прогноза:", reply_markup=reply_markup)
        context.user_data['city_name'] = city_name
        context.user_data['waiting_for_period'] = True
    else:
        await update.message.reply_text("Пожалуйста, сначала нажмите Погода ☀️ или Прогноз 📅.")

async def get_forecast_period(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('waiting_for_period'):
        period = update.message.text
        city_name = context.user_data.get('city_name')
        context.user_data['waiting_for_period'] = False
        keyboard = [
                [KeyboardButton("Старт 🚀"), KeyboardButton("Погода ☀️"), KeyboardButton("Прогноз 📅")],
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        if period == "Завтра 🗓️":
            forecast_info = await get_weather_forecast(city_name, 1)

            await update.message.reply_text(forecast_info, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
        elif period == "На 3 дня 🗓️🗓️🗓️":
            forecast_info = await get_weather_forecast(city_name, 3)

            await update.message.reply_text(forecast_info, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
        elif period == "На неделю 🗓️🗓️🗓️🗓️🗓️🗓️🗓️":
            forecast_info = await get_weather_forecast(city_name, 7)

            await update.message.reply_text(forecast_info, parse_mode=ParseMode.HTML, reply_markup=reply_markup)
        else:
            await update.message.reply_text("Неверный период прогноза.")
    else:
        await update.message.reply_text("Пожалуйста, сначала нажмите Прогноз 📅 и введите город.")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Update {update} caused error {context.error}")

async def handle_start_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['waiting_for_city'] = None
    context.user_data['waiting_for_period'] = False
    await start(update, context)

async def handle_weather_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['waiting_for_period'] = False
    await openweather_weather(update, context)

async def handle_forecast_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
     context.user_data['waiting_for_period'] = False
     await forecast_weather(update, context)

def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Старт 🚀$"), handle_start_button))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Погода ☀️$"), handle_weather_button))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Прогноз 📅$"), handle_forecast_button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^(Завтра 🗓️|На 3 дня 🗓️🗓️🗓️|На неделю 🗓️🗓️🗓️🗓️🗓️🗓️🗓️)$"), get_city_name))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(Завтра 🗓️|На 3 дня 🗓️🗓️🗓️|На неделю 🗓️🗓️🗓️🗓️🗓️🗓️🗓️)$"), get_forecast_period))
    application.add_error_handler(error)

    application.run_polling()

if __name__ == "__main__":
    main()
