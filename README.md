# SQL Sandbox

Веб-приложение для выполнения SQL-запросов в браузере. Загрузи свою SQLite базу данных, просматривай таблицы и тестируй запросы в редакторе с подсветкой синтаксиса.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-async-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-async-red)

## Возможности

- Загрузка собственной SQLite базы данных через браузер
- Просмотр списка таблиц и их содержимого
- Выполнение произвольных SQL-запросов (SELECT, INSERT, UPDATE, DELETE)
- Редактор запросов на базе Monaco Editor (тот же что в VS Code)
- Отображение результатов в виде таблицы
- Сообщения об ошибках при некорректных запросах
- Автоматическое удаление загруженной БД при завершении сервера

## Стек

- **FastAPI** — асинхронный веб-фреймворк
- **SQLAlchemy (async)** — выполнение SQL-запросов
- **aiosqlite** — асинхронный драйвер SQLite
- **sqlparse** — парсинг и определение типа SQL-запроса
- **sql-metadata** — извлечение имён таблиц из запроса
- **Monaco Editor** — редактор кода с подсветкой SQL
- **Jinja2** — HTML-шаблоны

## Структура проекта

```
sqlSandbox/
├── main.py            # FastAPI-приложение, роуты
├── db.py              # Работа с базой данных
├── config.py          # Конфигурация подключения
├── static/            # CSS, JS, Monaco Editor
├── templates/         # HTML-шаблоны (Jinja2)
├── requirements.txt   # Зависимости
└── README.md
```

## Установка и запуск

```bash
git clone https://github.com/makel0ve/sqlSandbox.git
cd sqlSandbox
pip install -r requirements.txt
python main.py
```

Открыть в браузере: `http://127.0.0.1:8000`

## Как использовать

1. Открой главную страницу
2. Загрузи `.sqlite` файл
3. Выбери таблицу из списка или напиши SQL-запрос в редакторе
4. Результат отобразится в виде таблицы