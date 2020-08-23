class FileSystemStub:

    def __init__(self):
        self._fs_stub = {}

    def read(self, file_path):
        if not file_path in self._fs_stub:
            return None
        return self.stub_pad_content(self._fs_stub[file_path])

    def stub_pad_content(self, content):
        content = content.split('\n')
        padded_content = [line + '\n' for line in content]
        padded_content[-1] = padded_content[-1].replace('\n', '')
        return padded_content

    def write(self, file_path, file_content):
        print('FileSystemStub WRITE:', file_path)
        print(file_content)
        self._fs_stub[file_path] = file_content

    def list_files(self, path):
        files = []
        for element in self._fs_stub:
            if element.startswith(path):
                files.append(element)
        return files
