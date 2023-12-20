from butler_offline.core import file_system
from typing import List
import os
import glob


class FileSystemImpl:
    def read(self, file_path: str) -> List[str] | None:
        if not os.path.isfile(file_path):
            return None

        with open(file_path) as file:
            file_content = []

            for line in file:
                file_content.append(line)
        return file_content

    def write(self, file_path: str, file_content: str) -> None:
        with open(file_path, 'w') as file:
            file.write(file_content)

    def list_files(self, path: str) -> List[str]:
        return sorted(glob.glob(path))


INSTANCE: FileSystemImpl | None = None


def instance() -> FileSystemImpl:
    if file_system.INSTANCE is None:
        file_system.INSTANCE = FileSystemImpl()
    return file_system.INSTANCE


IMPORT_PATH = './Import/'
ABRECHNUNG_PATH = './Abrechnungen/'


def write_import(file_name: str, file_content: str, filesystem: file_system.FileSystemImpl) -> None:
    filesystem.write(IMPORT_PATH + file_name, file_content)


def write_abrechnung(file_name: str, file_content: str, filesystem: file_system.FileSystemImpl) -> None:
    filesystem.write(
        file_path=ABRECHNUNG_PATH + file_name,
        file_content=file_content,
    )


def all_abrechnungen(filesystem: FileSystemImpl):
    filenames = filesystem.list_files(ABRECHNUNG_PATH + '*') + filesystem.list_files(IMPORT_PATH + '*')
    all_contents = []
    for filename in filenames:
        all_contents.append({
            'name': filename,
            'content': filesystem.read(filename)
        })
    return all_contents
