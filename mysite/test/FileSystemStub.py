
class FileSystemStub:


    def __init__(self):
        self._fs_stub = {}

    def read(self, file_path):

        if not file_path in self._fs_stub:
            return None

        return self._fs_stub[file_path].split('\n')

    def write(self, file_path, file_content):
        print('FileSystemStub WRITE:', file_path)
        print(file_content)
        self._fs_stub[file_path] = file_content
