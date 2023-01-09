# SoundProducerClient

## Установка и запуск

- Скачать исходник как zip-архив и распаковать в любую удобную папку

![скрин](https://i.imgur.com/SCE4sLO.png)

- В любом удобном терминале(pycharm, cmd) перейти в папку с проектом
- Создать виртуальное окружение
```
python -m venv venv
```
- Активировать виртуальное окружение
```
venv\Scripts\activate
```
- Установить все зависимости в виртуальное окружение
```
python -m pip install -r requirements.txt
```
- Запустить код
```
python .\src\main.py
```
- Вы восхитительны!
![Скрин](https://i.imgur.com/UZ9CpAT.png)


## Обучение модели диктора
- Нажать Создать диктора
- Максимально избавиться от посторонних звуков
- Поговорить примерно минуту все, что душе угодно
- Помолчать 2-3 секунды ОБЯЗАТЕЛЬНО
- Нажать Остановить запись
- В папке с проектом в папке speakers появится файлик с именем {Имя пользователя}.json
- Json файл нужно загрузить на сервер, информация по загрузке в README сервера


## Запись голоса и отправка данных на сервер

- Нажать Начать запись
- Поговорить что-нибудь
- Помолчать 2-3 секунды ОБЯЗАТЕЛЬНО
- Нажать Остановить запись
- Нажать Отправить данные
- Обрадоваться зеленой надписи "Успешно отправлено!"

![скрин](https://i.imgur.com/GHbRtYI.png)