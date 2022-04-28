"""работа с БД sqlite3"""
import sqlite3


class SqlStorage:
    """класс создания и работы с БД sqlite3"""
    _PARAMS = ['id', 'name', 'tag']

    def __init__(self, db_name='DefaultName'):
        """присваиваем имя нашей БД, настраиваем коннект"""
        self._db_name = db_name
        self._connection = sqlite3.connect(self._db_name)
        self._cr_table()

    def _cr_table(self) -> None:
        """если таблицы нет - создаем, если уже есть то пропускаем"""
        cursor = self._connection.cursor()
        cursor.execute('create table if not exists fileserver(id text, name text, '
                       'tag text, size int, mimeType text, modificationTime text , unique(id))')
        self._connection.commit()

    @staticmethod
    def _gef_find_string(data: dict) -> str:
        """упаковываем полученный словарь в выражение для SQL"""
        keys = list(data.keys())
        rez_str = ''
        for key in keys:
            if key in SqlStorage._PARAMS:
                rez_str += " and "
                if len(data[key]) == 1:
                    rez_str += key + "='" + data[key][0] + "'"
                else:
                    rez_str += "("
                    for i in range(len(data[key])):
                        rez_str += key + "='" + data[key][i] + "'"
                        if i < len(data[key]) - 1:
                            rez_str += " or "
                    rez_str += ")"
        rez_str = rez_str[5:]
        return rez_str

    def save_to_db(self, ids: str, name: str, tag: str, size: int,#pylint: disable=too-many-arguments
                   mime_type: str, modification_time: str) -> None:
        """сохраняем в базу параметры файла"""
        cursor = self._connection.cursor()
        cursor.execute('insert into fileserver(id, name, tag, size, mimeType,'
                       ' modificationTime) values (?, ?, ?, ?, ?, ?)',
                       (ids, name, tag, size, mime_type, modification_time))
        self._connection.commit()

    def update_to_db(self, ids: str, name: str, tag: str, size: int,#pylint: disable=too-many-arguments
                     mime_type: str, modification_time: str) -> None:
        """update если в базе уже есть такой файл"""
        cursor = self._connection.cursor()
        cursor.execute(f"update fileserver set name='{name}', tag='{tag}', size='{str(size)}',"
                       f" mimeType='{mime_type}', modificationTime='{modification_time}' "
                       f"where id='{ids}'")
        self._connection.commit()

    def load_from_db(self, data: dict) -> list:
        """получаем из базы файлы соответствующие условиям"""
        if len(data) == 0:
            #если в запросе нет параметров возвращаем все значения из таблицы
            cursor = self._connection.cursor()
            cursor.execute("select * from fileserver")
            result = cursor.fetchall()
            self._connection.commit()
            return result
        #если получили параметры в словаре
        find_data = self._gef_find_string(data)
        cursor = self._connection.cursor()
        cursor.execute("select * from fileserver where " + find_data)
        result = cursor.fetchall()
        self._connection.commit()
        return result

    def del_from_db(self, **kwargs) -> None:
        """удаляем запись из базы"""
        cursor = self._connection.cursor()
        cursor.execute(f"delete from fileserver where id ='{kwargs['id']}'")
        self._connection.commit()
