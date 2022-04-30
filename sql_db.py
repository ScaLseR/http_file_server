"""sqlite3 database operation"""
import sqlite3


class SqlStorage:
    """сlass for creating and working with the database sqlite3"""
    _PARAMS = ['id', 'name', 'tag', 'mimetype', 'modificationtime']

    def __init__(self, db_name='DefaultName'):
        """name our database, set up a connection"""
        self._db_name = db_name
        self._connection = sqlite3.connect(self._db_name)
        self._cr_table()

    def _cr_table(self) -> None:
        """If there is no table - create it, if there is already - skip it"""
        cursor = self._connection.cursor()
        cursor.execute('create table if not exists fileserver(id text, name text, '
                       'tag text, size int, mimeType text, modificationTime text , unique(id))')
        self._connection.commit()

    @staticmethod
    def _gef_find_string(data: dict) -> str:
        """pack the resulting dictionary into an expression for SQL"""
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
        """save file parameters to the database"""
        cursor = self._connection.cursor()
        cursor.execute('insert into fileserver(id, name, tag, size, mimeType,'
                       ' modificationTime) values (?, ?, ?, ?, ?, ?)',
                       (ids, name, tag, size, mime_type, modification_time))
        self._connection.commit()

    def update_to_db(self, ids: str, name: str, tag: str, size: int,#pylint: disable=too-many-arguments
                     mime_type: str, modification_time: str) -> None:
        """update if there is already such a file in the database"""
        cursor = self._connection.cursor()
        cursor.execute(f"update fileserver set name='{name}', tag='{tag}', size='{str(size)}',"
                       f" mimeType='{mime_type}', modificationTime='{modification_time}' "
                       f"where id='{ids}'")
        self._connection.commit()

    def load_from_db(self, data: dict) -> list:
        """Get the files that meet the conditions from the database"""
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
        """remove the record from the database"""
        cursor = self._connection.cursor()
        cursor.execute(f"delete from fileserver where id ='{kwargs['id']}'")
        self._connection.commit()
