from butler_offline.core import file_system
import os
import glob

INSTANCE = None


def instance():
    if file_system.INSTANCE == None:
        file_system.INSTANCE = FileSystemImpl()
    return file_system.INSTANCE


IMPORT_PATH = '../Import/'
ABRECHNUNG_PATH = '../Abrechnungen/'


def write_import(file_name, file_content):
    instance().write(IMPORT_PATH + file_name, file_content)


def write_abrechnung(file_name, file_content):
    instance().write(ABRECHNUNG_PATH + file_name, file_content)


def all_abrechnungen():
    filenames = instance().list_files(ABRECHNUNG_PATH + '*') + instance().list_files(IMPORT_PATH + '*')
    all_contents = []
    for filename in filenames:
        all_contents.append({
            'name': filename,
            'content': instance().read(filename)
        })
    return all_contents


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
        return sorted(glob.glob(path))
