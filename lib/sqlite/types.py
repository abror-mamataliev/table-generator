from datetime import date
from sqlite3 import (
    connect,
    Connection,
    Cursor
)
from typing import Union

from .exceptions import SQLiteAttributeError


class SQLite:

    def __init__(self, path: str) -> None:
        self.path: str = path
        self._connect()
    
    def _build_select_query(self, **kwargs) -> str:
        if 'table' not in kwargs or kwargs['table'] is None:
            raise SQLiteAttributeError("Table name is required.")
        query: str = f"SELECT {', '.join(kwargs['fields'] if 'fields' in kwargs else '*')} FROM {kwargs['table']}"
        if 'where' in kwargs:
            query += f" WHERE {kwargs['where']}"
        if 'group_by' in kwargs:
            query += f" GROUP BY {kwargs['group_by']}"
        if 'order_by' in kwargs:
            query += f" ORDER BY {kwargs['order_by']}"
        query += ";"
        return query
    
    def _build_insert_query(self, **kwargs) -> str:
        if 'table' not in kwargs or kwargs['table'] is None:
            raise SQLiteAttributeError("Table name is required.")
        keys: str = ", ".join([key for key in kwargs if key != 'table'])
        values: str = ", ".join([f"'{value}'" if isinstance(value, str) or isinstance(value, date) else str(value) for key, value in kwargs.items() if key != 'table'])
        query: str = f"INSERT INTO {kwargs['table']} ({keys}) VALUES ({values});"
        return query

    def _commit(self) -> None:
        self.connection.commit()
    
    def _connect(self) -> None:
        self.connection: Connection = connect(self.path)
        self.cursor: Cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS region (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR NOT NULL);")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR NOT NULL, region VARCHAR, district VARCHAR, key VARCHAR NOT NULL, value DOUBLE, date DATE NOT NULL);")
        self._commit()
        rows: int = self.cursor.execute("SELECT COUNT(*) FROM region;").fetchone()[0]
        if rows == 0:
            self._execute("INSERT INTO region (id, name) VALUES (1, 'Қорақалпоғистон Республикаси');")
            self._execute("INSERT INTO region (id, name) VALUES (2, 'Андижон вилояти');")
            self._execute("INSERT INTO region (id, name) VALUES (3, 'Бухоро вилояти');")
            self._execute("INSERT INTO region (id, name) VALUES (4, 'Жиззах вилояти');")
            self._execute("INSERT INTO region (id, name) VALUES (5, 'Қашқадарё вилояти');")
            self._execute("INSERT INTO region (id, name) VALUES (6, 'Навоий вилояти');")
            self._execute("INSERT INTO region (id, name) VALUES (7, 'Наманган вилояти');")
            self._execute("INSERT INTO region (id, name) VALUES (8, 'Самарқанд вилояти');")
            self._execute("INSERT INTO region (id, name) VALUES (9, 'Сурхондарё вилояти');")
            self._execute("INSERT INTO region (id, name) VALUES (10, 'Сирдарё вилояти');")
            self._execute("INSERT INTO region (id, name) VALUES (11, 'Тошкент вилояти');")
            self._execute("INSERT INTO region (id, name) VALUES (12, 'Фарғона вилояти');")
            self._execute("INSERT INTO region (id, name) VALUES (13, 'Хоразм вилояти');")
            self._commit()
    
    def _execute(self, query: str) -> None:
        self.cursor.execute(query)
    
    def select(self, first: bool = False, table: str = None, **kwargs) -> Union[list, tuple]:
        query: str = self._build_select_query(table=table, **kwargs)
        self._execute(query)
        return self.cursor.fetchone() if first else self.cursor.fetchall()
    
    def insert(self, table: str = None, **kwargs) -> None:
        query: str = self._build_insert_query(table=table, **kwargs)
        self._execute(query)
        self._commit()
    
    def update(self, query: str, *args) -> None:
        self._execute(query)
        self._commit()
    
    def delete(self, query: str, *args) -> None:
        self._execute(query)
        self._commit()
    
    def close(self) -> None:
        self.connection.close()
