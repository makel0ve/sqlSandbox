from typing import Sequence

import sqlparse
from sql_metadata import Parser
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from config import SQLALCHEMY_DATABASE_URL


engine: AsyncEngine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


async def get_tables_name() -> list[str]:
    """Возвращает список названий таблиц в базе данных."""

    async with engine.connect() as conn:
        result = await conn.execute(
            text("SELECT name FROM sqlite_master WHERE type = 'table'")
        )

        return [row[0] for row in result]


async def get_column_names(table_name: str) -> list[str]:
    """Возвращает список названий колонок для указанной таблицы."""

    async with engine.connect() as conn:
        result = await conn.execute(text(f"PRAGMA table_info({table_name})"))

        return [row[1] for row in result]


async def validate_table_name(table_name: str) -> bool:
    """Проверяет, что таблица существует в базе данных."""

    tables = await get_tables_name()

    return table_name in tables


async def get_table_data(query: str) -> tuple[Sequence, list[str], str]:
    """
    Выполняет SQL-запрос и возвращает результат.

    Args:
        query: SQL-запрос.

    Returns:
        Кортеж (записи, названия колонок, имя таблицы).

    Raises:
        ValueError: если запрос некорректен или таблица не найдена.
    """

    parsed = sqlparse.parse(query)
    if not parsed:
        raise ValueError("Пустой запрос")

    query_type = parsed[0].get_type()

    try:
        table_names = Parser(query).tables

    except Exception:
        raise ValueError("Не удалось определить таблицу в запросе")

    if not table_names:
        raise ValueError("Не удалось определить таблицу в запросе")

    table_name = table_names[0]

    if not await validate_table_name(table_name):
        raise ValueError(f"Таблица '{table_name}' не найдена")

    column_names = await get_column_names(table_name)

    async with engine.connect() as conn:
        await conn.execute(text("PRAGMA foreign_keys = ON;"))
        await conn.commit()

        if query_type == "SELECT":
            result = await conn.execute(text(query))
            records = result.fetchall()

        else:
            async with conn.begin():
                await conn.execute(text(query))
                result = await conn.execute(
                    text(f"SELECT * FROM {table_name}")
                )
                records = result.fetchall()

    return records, column_names, table_name


def dispose_engine():
    """Закрывает соединение с БД (для lifespan)."""
    
    return engine.dispose()