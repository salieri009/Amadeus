"""
adapters/file_io.py - 로컬 파일 I/O 어댑터 (Local File I/O Adapter)

이 파일의 역할:
    데이터를 읽고 쓰는 "방법"을 캡슐화(Encapsulate)하는 어댑터 계층입니다.
    파이프라인의 핵심 로직(pipeline.py)은 "데이터가 어디서 오고 어디로 가는지"를
    전혀 신경 쓸 필요 없이, 이 어댑터만 교체하면 됩니다.

확장성 (왜 어댑터 패턴을 쓰는가):
    현재:    로컬 파일 시스템에서 읽고 쓰기 (LocalFileReader / LocalFileWriter)
    향후:    S3FileReader, KafkaReader, DatabaseWriter 등으로 교체 가능
    핵심:    pipeline.py의 코드는 단 한 줄도 수정할 필요 없음!

실무 적용:
    향후 다른 프로젝트에서 S3Reader, KafkaReader 등으로 교체하면 됩니다.
"""

import os
from typing import Iterator


class LocalFileReader:
    """
    로컬 파일에서 데이터를 한 줄씩 읽어오는 Reader 어댑터.

    사용 예:
        reader = LocalFileReader("input_logs/server_logs.jsonl")
        for line in reader.read_lines():
            print(line)  # JSON 문자열 한 줄씩 출력
    """

    def __init__(self, file_path: str):
        """
        Args:
            file_path (str): 읽어올 파일의 경로 (예: "input_logs/server_logs.jsonl")
        """
        self.file_path = file_path

    def read_lines(self) -> Iterator[str]:
        """
        파일을 한 줄씩 읽어서 반환하는 제너레이터(Generator).

        - yield를 사용하므로 파일 전체를 메모리에 올리지 않고,
          한 줄씩 처리할 수 있어 대용량 파일에도 안전합니다.
        - 앞뒤 공백/개행 문자를 strip()으로 제거합니다.

        Yields:
            str: 파일에서 읽어온 한 줄 (공백 제거됨)

        Raises:
            FileNotFoundError: 파일이 존재하지 않을 경우
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                yield line.strip()


class LocalFileWriter:
    """
    로컬 파일 시스템에 데이터를 한 줄씩 기록하는 Writer 어댑터.

    사용 예:
        writer = LocalFileWriter("processed_logs")
        writer.write_line("valid_logs.jsonl", '{"ip": "1.2.3.4", "status": 200}')
    """

    def __init__(self, directory: str):
        """
        Args:
            directory (str): 파일을 저장할 디렉토리 경로 (예: "processed_logs")
        """
        self.directory = directory
        # 디렉토리가 없으면 자동 생성 (exist_ok=True: 이미 있어도 에러 안 남)
        os.makedirs(self.directory, exist_ok=True)

    def write_line(self, filename: str, line: str):
        """
        지정된 파일에 한 줄을 추가(append) 모드로 기록합니다.

        Args:
            filename (str): 저장할 파일 이름 (예: "valid_logs.jsonl")
            line (str): 기록할 데이터 문자열 (JSON 한 줄)

        Note:
            "a" (append) 모드로 열기 때문에 기존 내용을 덮어쓰지 않고
            파일 끝에 계속 추가됩니다.
        """
        file_path = os.path.join(self.directory, filename)
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
