"""file operations"""
import os


def save_file_to_disk(name: str, body: bytes) -> None:
    """writing file to disk"""
    with open(name, mode="wb") as file:
        file.write(body)


def load_file_from_disk(name: str) -> bytes:
    """downloading file from disk"""
    with open(name, mode="rb") as file:
        body = file.read()
    return body


def delete_file_from_disk(name: str) -> None:
    """deleting file from disk"""
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), name)
    os.remove(path)
    print(name + ' - file deleted')
