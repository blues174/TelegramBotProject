# Бот погоды
Telegram-бот, который составляет прогноз погоды для любого города мира.

## Описание проекта
Telegram-бот обращается к сайту с погодой, и сообщает погоду на сегодняшний день. Бот пишет название города, облачность, температуру, как ощущается эта температура, скорость ветра и влажность. 

## Стек технологий
* [Python 3.7+](https://www.python.org/downloads/)
* [Python-dotenv](https://pypi.org/project/python-dotenv/)
* [requests 2.26.0](https://pypi.org/project/requests/)
* [pytelegrambotapi](https://pypi.org/project/pyTelegramBotAPI/)
* [AIOHTTP](https://docs.aiohttp.org/en/stable/index.html)

## Как запустить проект
1. Перед запуском убедитесь, что у вас есть установленный python версии >= 3.7
2. Используя командную строку, загрузите все используемые библиотеки командой: pip install python-telegram-bot requests python-dotenv aiohttp 
3. Зайдите в @BotFather в телеграме и напишите /newbot, дайте имя и тэг вашему боту, после чего скопируйте полученный токен вашего
бота
5. В строчке BOT_TOKEN добавьте свой токен
7. В строчке OPENWEATHER_API_KEY добавьте свой токен [Open Weather API](https://openweathermap.org/forecast5)
8. Запустите файл weather_bot.py
9. Отправьте боту команду /start
10. Чтобы получить погоду, отправьте /weather "название города", например /weather Ижевск.
