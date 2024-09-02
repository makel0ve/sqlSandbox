from typing import Tuple

import sqlparse
from sqlalchemy import text, Sequence
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sql_metadata import Parser
 
import config
 

async def create_engine_db() -> AsyncEngine:
    engine = create_async_engine(
        config.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    return engine


async def get_tables_name() -> list:
    engine = await create_engine_db()
    async with engine.connect() as conn:
        tables = await conn.execute(text("SELECT NAME FROM sqlite_master WHERE type = 'table'"))
        tables = [t for table in tables for t in table]
    
    return tables


async def get_column(table_name: str) -> list:
    engine = await create_engine_db()
    async with engine.connect() as conn:
        column_query = f"pragma table_info({table_name})"
        column_names = await conn.execute(text(column_query))
        column_names = [title[1] for title in column_names]

        return column_names


async def get_table_data(text_query: str) -> Tuple[Sequence, list]:
    engine = await create_engine_db()
    
    query_type = sqlparse.parse(text_query)[0].get_type()
    table_names = Parser(text_query).tables
    
    column_names = await get_column(table_names[0]) if query_type == 'SELECT' else []
    
    async with engine.connect() as conn:
        if query_type == "SELECT":
            result = await conn.execute(text(text_query))
            records = result.fetchall()

            return records, column_names, table_names[0]

        else:
            async with conn.begin():
                await conn.execute(text(text_query))
            
            result = conn.execute(f"SELECT * FROM {table_names[0]}")

            return records, column_names, table_names[0]