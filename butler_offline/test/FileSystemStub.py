class FileSystemStub:

    def __init__(self):
        self._fs_stub = {}
        self._file_name_stub = {}

    def read(self, file_path):
        if not file_path in self._fs_stub:
            return None

        return self._fs_stub[file_path].split('\n')

    def write(self, file_path, file_content):
        print('FileSystemStub WRITE:', file_path)
        print(file_content)
        self._fs_stub[file_path] = file_content

    def set_file(self, path, list_of_filenames):
        print('Adding adding files', list_of_filenames, 'for path', path)
        self._file_name_stub[path] = list_of_filenames

    def list_files(self, path):
        return self._file_name_stub[path]
