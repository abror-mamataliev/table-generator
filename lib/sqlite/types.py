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
        if 'table' not in kwargs:
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

    def _commit(self) -> None:
        self.connection.commit()
    
    def _connect(self) -> None:
        self.connection: Connection = connect(self.path)
        self.cursor: Cursor = self.connection.cursor()
    
    def _execute(self, query: str) -> None:
        self.cursor.execute(query)
    
    def select(self, first: bool = False, table: str = None, **kwargs) -> Union[list, tuple]:
        query: str = self._build_select_query(table=table, **kwargs)
        self._execute(query)
        return self.cursor.fetchone() if first else self.cursor.fetchall()
    
    def insert(self, query: str, *args) -> None:
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
