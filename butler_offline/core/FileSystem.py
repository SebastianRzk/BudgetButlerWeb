from butler_offline.core import FileSystem
import os
import glob

INSTANCE = None


def instance():
    if FileSystem.INSTANCE == None:
        FileSystem.INSTANCE = FileSystemImpl()
    return FileSystem.INSTANCE


IMPORT_PATH = '../Import/'
ABRECHNUNG_PATH = '../Abrechnungen/'


def write_import(file_name, file_content):
    instance().write(IMPORT_PATH + file_name, file_content)


def write_abrechnung(file_name, file_content):
    instance().write(ABRECHNUNG_PATH + file_name, file_content)


class FileSystemImpl:
    def read(self, file_path):

        if not os.path.isfile(file_path):
            return None

        with open(file_path) as file:
            file_content = []

            for line in file:
                file_content.append(line)
        return file_content

    def write(self, file_path, file_content):
        with open(file_path, 'w') as file:
            file.write(file_content)

    def list_files(self, path):
        return glob.glob(path)
