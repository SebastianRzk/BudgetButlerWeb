import glob
import os
from typing import List


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



