"""работа с БД sqlite3"""
import sqlite3
import datetime


class SqlStorage:
    """класс создания и работы с БД sqlite3"""
    def __init__(self, db_name='DefaultName'):
        """присваиваем имя нашей БД, настраиваем коннект"""
        self._db_name = db_name
        self._connection = sqlite3.connect(self._db_name)
        self._cr_table()

    def _cr_table(self):
        """если таблицы нет - создаем, если уже есть то пропускаем"""
        cursor = self._connection.cursor()
        cursor.execute('create table if not exists fileserver(id text, name text, '
                       'tag text, size int, mimeType text, location text, modificationTime text , unique(id))')
        self._connection.commit()

    def save_to_db(self, ids: str, name: str, tag: str, size: int, mime_type: str, modification_time: str):
        """сохраняем в базу параметры файла"""
        cursor = self._connection.cursor()
        cursor.execute('insert into fileserver(id, name, tag, size, mimeType, '
                       'location, modificationTime) values (?, ?, ?, ?, ?, ?, ?)',
                       (ids, name, tag, size, mime_type, '/', modification_time))
        self._connection.commit()

    def load_from_db(self, **kwargs) -> dict:
        """получаем из базы файлы соответствующие условиям"""
        if len(kwargs) == 0:
            cursor = self._connection.cursor()
            cursor.execute("select * from fileserver")
            result = cursor.fetchall()
            self._connection.commit()
        else:
            result = kwargs
        return result
