# Бот погоды
Telegram-бот, который составляет прогноз погоды для определённого региона Российской Федерации

## Описание проекта
Telegram-бот обращается к сайту с погодой, составляет прогноз погоды на сегодняшний день, завтрашний день, на 3 дня, на 10 дней, на 2 недели, и на месяц. В прогнозе будут предоставлены такие данные как: температура воздуха 
°C; Порывы ветра, м/с; влажность, %.

## Стек технологий

* [Python 3.7+](https://www.python.org/downloads/)
* [requests 2.26.0](https://pypi.org/project/requests/)
* [pytelegrambotapi](https://pypi.org/project/pyTelegramBotAPI/)
* [emoji](https://pypi.org/project/emoji/)

## Как запустить проект
1. Перед запуском убедитесь, что у вас есть установленный python версии >= 3.7
2. Загрузите все используемые библиотеки командой: <br>
`pip3 install requests pytelegrambotapi emoji`
3. Зайдите в @BotFather в телеграме и напишите /newbot, дайте имя и тэг вашему боту, после чего скопируйте полученный токен вашего
бота
5. В строчке `API_TOKEN = ''` добавьте свой токен
6. В строчке `YANDEX_GEOCODER_API_TOKEN` добавьте свой токен [Yandex API](https://yandex.ru/maps-api/products/geocoder-api)
7. В строчке `OPEN_WEATHER_API_TOKEN` добавьте свой токен [Open Weather API](https://openweathermap.org/forecast5)
8. Запустите файл bot.py
