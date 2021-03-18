import sqlite3
from typing import Dict, List, Tuple


def db_insert(db: str, table: str, data: dict):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    print(type(data))
    columns_joined = ", ".join(data.keys())
    value_joined = [tuple(data.values())]
    placeholders = ", ".join( "?" * len(data.keys()) )
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns_joined}) "
        f"VALUES ({placeholders})",
        value_joined
    )
    conn.commit()


def db_fetchall(db: str, table: str, columns: list[str]):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    columns_joined = ", ".join(columns)
    src_data = cursor.execute(
        f"SELECT {columns_joined} "
        f"FROM {table}"
    ).fetchall()
    data = []
    for item in src_data:
        data.append(item)
    return data


def db_delete_by_id(db: str, table: str, row_id: int) -> None:
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    row_id = int(row_id)
    cursor.execute(f"DELETE FROM {table} WHERE ID={row_id}")
    conn.commit()


def db_check(db: str):
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master")
    table_exists = cursor.fetchall()
    if table_exists:
        return True
    return False
