import os
from typing import Iterator

class LocalFileReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_lines(self) -> Iterator[str]:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                yield line.strip()

class LocalFileWriter:
    def __init__(self, directory: str):
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)

    def write_line(self, filename: str, line: str):
        file_path = os.path.join(self.directory, filename)
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
