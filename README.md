# Async Web Services

## Сервисы

### Среднее время загрузки сайта

Сервис определяет среднее время загрузки сайта

### Парсинг txt книг

Сервис парсит сайты с книгами в формате txt, и формирует словарь с частотой повторения всех слов. 
Можно, например, узнать какие слова чаще всего встречаются в романе "Война и мир".

## Стэк

`Python 3.10`, `aiohttp`, `asyncio`, `Docker`

## Управление

### Сборка проекта

* Создайте директорию (например: `d:/async_services`)
* Откройте консольную программу и перейдите в созданную директорию (например: `PowerShell` и `cd d:/async_services`)
* Клонируйте проект с репозитория: `git clone https://github.com/amiddio/async_services.git .`
* В корне создайте `.env` файл по образу и подобию `.env.example`
* Запустите Docker
* С корня `d:/async_services` запустите: `docker-compose build`

### Запуск

* Перейдите в корень проекта `d:/async_services`
* Выполните команду: `docker-compose up`
* К сервисам можно обращаться по `localhost` и по порту указанном в `.env` файле. Например `http://localhost:8008`

### Остановка

* С корня `d:/async_services` выполните команду `docker-compose down`

### Unittests

* С корня `d:/async_services` перейти в `cd /src/tests`
* Запуск тестов для первого сервиса: `python website_speed_test.py`
* Запуск тестов для второго сервиса: `python parse_text_test.py`

## Сервис: среднее время загрузки сайта

Сервис асинхронно посылает N запросов к сайту и считает среднее время загрузки.

#### Запуск

GET `http://localhost:8008/website_speed?url=[URL]&times=[N]`

* [URL] - урл сайта
* [N] - количество запросов

#### Пример

`http://localhost:8008/website_speed?url=https://example.com&times=1000`

![Screenshot_1](/screenshots/website_speed.png)

На `https://example.com` асинхронно летят `1000` запросов. 
Среднее время загрузки сайта `2.6848` секунд. 
Скрипт отработал за `4.4101` секунды.

## Сервис: парсинг txt книг

Сперва сервис загружает txt книги для парсинга. 

Далее происходит очистка текста от ненужных символов и пробелов. Для этого он разбивается на части. 
И каждая часть как отдельная задача передается пулу процессов. По окончанию работы пула результат всех частей редуцируется в единный текст.

Следующий этап - формирование словаря с частотой повторений слов. Для этого также используется пул процессов и техника MapReduce.

В заключении происходит сортировка словаря по убыванию частоты повторений слов.

#### Запуск

POST `http://localhost:8008/parse_text`

* urls: str - список урл-ов на книги через запятую
* limit: int - количество слов в словаре. 0 (значение по умолчанию) возвращает все слова.
* exclude_words_le: int - исключает из словаря слова меньше или равно определенной длины. 0 (значение по умолчанию) возвращает все слова.
* include_words_only: str - список слов через запятую которые мы хотим видеть в словаре. Остальные слова игнорируются. '' (пустая строка) значение по умолчанию.

#### Примеры использования

Для примера пропарсим четыре тома романа "Война и мир":
* https://tululu.org/txt.php?id=77440
* https://tululu.org/txt.php?id=77441
* https://tululu.org/txt.php?id=77442
* https://tululu.org/txt.php?id=77443

![Screenshot_1](/screenshots/parse_text_1.png)

Возвращаем словарь как есть.

В секции `meta` приводится информация о работе скрипта: 
* content_loading: 0.8620 - загрузка книг (время данно в секундах)
* content_cleaning: 0.3690 - очистка текста
* words_frequencies_creating: 0.4704 - создание словаря
* dictionary_sorting: 0.1139 - сортировка
* script_loading: 1.8157 - общее время работы скрипта

В секции `data` мы видим словарь с результатом. 
Самое часто встречаемое слово/буква в "Война и мир": 'и', 'в', 'не', 'что' и т.д.

![Screenshot_1](/screenshots/parse_text_2.png)

Выводим 10 самых встречаемых слов/букв.

![Screenshot_1](/screenshots/parse_text_3.png)

Исключаем из результата слова короче четырех букв и возвращаем 10 самых встречаемых.

![Screenshot_1](/screenshots/parse_text_4.png)

Указываем список слов и возвращаем их частоту появлений в романе.

Если в `.env` выставить `LOGGING` в `True` то можно в консоли наблюдать за работой скрипта:

```
======== Running on http://0.0.0.0:8008 ========
(Press CTRL+C to quit)

Start loading website https://tululu.org/txt.php?id=77440
Start loading website https://tululu.org/txt.php?id=77441
Start loading website https://tululu.org/txt.php?id=77442
Start loading website https://tululu.org/txt.php?id=77443
Text from website https://tululu.org/txt.php?id=77443 received
Text from website https://tululu.org/txt.php?id=77440 received
Text from website https://tululu.org/txt.php?id=77441 received
Text from website https://tululu.org/txt.php?id=77442 received

Start cleaning text chunk 1 (50000)
End cleaning text chunk 1 (50000)
Start cleaning text chunk 2 (50000)
End cleaning text chunk 2 (50000)
...
End cleaning text chunk 60 (50000)
Start cleaning text chunk 61 (2335)
End cleaning text chunk 61 (2335)

Start creating words frequencies from chunk 1
End creating words frequencies from chunk 1. Done for 3201 words.
Start creating words frequencies from chunk 2
End creating words frequencies from chunk 2. Done for 3077 words.
...
Start creating words frequencies from chunk 56
End creating words frequencies from chunk 56. Done for 2251 words.
Start creating words frequencies from chunk 57
End creating words frequencies from chunk 57. Done for 1526 words.

Start merging dictionaries 3201 and 3077
End merging dictionaries 5360 and 3077
...
Start merging dictionaries 52343 and 2251
End merging dictionaries 52884 and 2251
Start merging dictionaries 52884 and 1526
End merging dictionaries 53244 and 1526

Start sorting words frequencies
End sorting words frequencies
```
