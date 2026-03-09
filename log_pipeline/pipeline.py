"""
pipeline.py - 로그 검증 파이프라인 엔진 (Log Validation Pipeline Engine)

이 파일의 역할:
    파이프라인의 핵심 비즈니스 로직을 담당합니다.
    Reader 어댑터로부터 데이터를 받아, Pydantic 모델로 검증(Validation)한 뒤,
    결과에 따라 정상/비정상 Writer 어댑터로 라우팅(Routing)합니다.

핵심 설계 원칙 (Dependency Injection):
    이 클래스는 "어디서 데이터를 읽고 어디에 쓸지"를 스스로 결정하지 않습니다.
    외부(main.py)에서 Reader와 Writer를 주입(Inject)받아 사용하기 때문에,
    파이프라인 로직을 수정하지 않고도 입출력 소스를 자유롭게 교체할 수 있습니다.

데이터 흐름:
    Reader(input_logs/) → Pydantic 검증 → 정상: processed_writer
                                         → 비정상: quarantine_writer
"""

import os
from pydantic import ValidationError
from models.log_model import ServerLog
from adapters.file_io import LocalFileReader, LocalFileWriter


class LogPipeline:
    """
    로그 데이터를 검증하고 정상/비정상으로 분류하는 파이프라인 엔진.

    Args:
        reader (LocalFileReader): 원본 로그를 읽어오는 어댑터
        processed_writer (LocalFileWriter): 정상 로그를 저장하는 어댑터
        quarantine_writer (LocalFileWriter): 비정상(격리) 로그를 저장하는 어댑터
    """

    def __init__(self, reader: LocalFileReader, processed_writer: LocalFileWriter, quarantine_writer: LocalFileWriter):
        self.reader = reader                        # 입력 어댑터 (데이터 소스)
        self.processed_writer = processed_writer    # 정상 데이터 출력 어댑터
        self.quarantine_writer = quarantine_writer  # 비정상 데이터 출력 어댑터

    def run(self):
        """
        파이프라인을 실행합니다.

        1. Reader에서 JSON 데이터를 한 줄씩 읽어옵니다.
        2. 각 줄을 ServerLog Pydantic 모델로 검증합니다.
           - 검증 통과 → processed_writer로 전달 (정상 로그)
           - 검증 실패(ValidationError) → quarantine_writer로 전달 (격리 로그)
        3. 처리 완료 후 결과 통계를 출력합니다.
        """
        processed_count = 0   # 정상 로그 카운터
        quarantine_count = 0  # 격리 로그 카운터

        # Reader 어댑터에서 한 줄씩 스트리밍 처리 (메모리 효율적)
        for line in self.reader.read_lines():
            try:
                # Pydantic 모델을 통한 JSON 데이터 검증
                # → 타입 체크 + @model_validator의 Anomaly Detection 로직 실행
                ServerLog.model_validate_json(line)

                # 검증 통과: 정상 로그 폴더(processed_logs/)에 저장
                self.processed_writer.write_line("valid_logs.jsonl", line)
                processed_count += 1

            except ValidationError as e:
                # 검증 실패: 격리 폴더(quarantine_logs/)에 원본 데이터 그대로 저장
                # (향후 에러 사유를 함께 기록하는 기능 추가 가능)
                self.quarantine_writer.write_line("quarantined_logs.jsonl", line)
                quarantine_count += 1

        # ── 최종 결과 리포트 ──
        print(f"Pipeline finished processing logs.")
        print(f"Valid Logs: {processed_count}")
        print(f"Quarantined Logs: {quarantine_count}")
