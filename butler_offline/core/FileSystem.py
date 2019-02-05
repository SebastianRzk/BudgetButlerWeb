from butler_offline.core import FileSystem
import os

INSTANCE = None

def instance():
    if FileSystem.INSTANCE == None:
        FileSystem.INSTANCE = FileSystemImpl()
    return FileSystem.INSTANCE


class FileSystemImpl:

    def read(self, file_path):

        if not os.path.isfile(file_path):
            return None

        file = open(file_path, 'r')
        file_content = []

        for line in file:
            file_content.append(line)

        file.close()

        return file_content

    def write(self, file_path, file_content):
        file = open(file_path, 'w')
        file.write(file_content)
        file.close()
