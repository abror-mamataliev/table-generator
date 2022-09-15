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
        query: str = f"INSERT INTO {kwargs['table']} ({', '.join([key for key in kwargs.keys() if key != 'table'])}) VALUES ({', '.join([value for key, value in kwargs if key != 'table'])});"
        return query

    def _commit(self) -> None:
        self.connection.commit()
    
    def _connect(self) -> None:
        self.connection: Connection = connect(self.path)
        self.cursor: Cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS region (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR NOT NULL);
            CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR NOT NULL, region VARCHAR, district VARCHAR, key VARCHAR NOT NULL, value VARCHAR, date DATE NOT NULL);
        """)
        rows: int = self.cursor.execute("SELECT COUNT(*) FROM region;").fetchone()[0]
        if rows == 0:
            self._execute("""
                INSERT INTO region (id, name) VALUES (1, 'Қорақалпоғистон Республикаси');
                INSERT INTO region (id, name) VALUES (2, 'Андижон вилояти');
                INSERT INTO region (id, name) VALUES (3, 'Бухоро вилояти');
                INSERT INTO region (id, name) VALUES (4, 'Жиззах вилояти');
                INSERT INTO region (id, name) VALUES (5, 'Қашқадарё вилояти');
                INSERT INTO region (id, name) VALUES (6, 'Навоий вилояти');
                INSERT INTO region (id, name) VALUES (7, 'Наманган вилояти');
                INSERT INTO region (id, name) VALUES (8, 'Самарқанд вилояти');
                INSERT INTO region (id, name) VALUES (9, 'Сурхондарё вилояти');
                INSERT INTO region (id, name) VALUES (10, 'Сирдарё вилояти');
                INSERT INTO region (id, name) VALUES (11, 'Тошкент вилояти');
                INSERT INTO region (id, name) VALUES (12, 'Фарғона вилояти');
                INSERT INTO region (id, name) VALUES (13, 'Хоразм вилояти');
            """)
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
