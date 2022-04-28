"""операции с файлами"""
import os


class FileOperation:
    """методы работы с файлами"""

    def save_file_to_disk(self, name: str, body: bytes) -> None:
        """запись файла на диск"""
        with open(name, mode="wb") as file:
            file.write(body)

    def load_file_from_disk(self, name: str) -> bytes:
        """загрузка файла с диска"""
        with open(name, mode="rb") as file:
            body = file.read()
        return body

    def delete_file_from_disk(self, name: str) -> None:
        """удаление файла с диска"""
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), name)
        os.remove(path)
        print(name + ' файл удален')