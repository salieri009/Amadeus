"""
main.py - 파이프라인 실행 진입점 (Pipeline Entry Point / Orchestrator)

이 파일의 역할:
    파이프라인의 모든 컴포넌트를 조립(Assemble)하고 실행(Run)하는 오케스트레이터입니다.
    각 컴포넌트(Reader, Writer, Pipeline)를 생성하고 의존성을 주입(Dependency Injection)합니다.

실행 순서:
    1. 입력 데이터가 없으면 → generator.py로 가짜 로그 자동 생성
    2. I/O 어댑터 생성 → LocalFileReader, LocalFileWriter 인스턴스화
    3. 파이프라인 엔진에 어댑터 주입 → LogPipeline 생성
    4. 파이프라인 실행 → pipeline.run()

사용법:
    $ cd log_pipeline
    $ python main.py
    또는
    $ uv run python main.py
"""

import os
from adapters.file_io import LocalFileReader, LocalFileWriter
from pipeline import LogPipeline
from generator import generate_logs


def main():
    """
    파이프라인의 전체 실행 흐름을 관리하는 메인 함수.

    디렉토리 구조:
        input_logs/       ← 원본 로그 데이터 (JSON Lines)
        processed_logs/   ← 검증 통과한 정상 로그 저장소
        quarantine_logs/  ← 검증 실패한 비정상 로그 격리소
    """

    # ── 1단계: 디렉토리 경로 설정 ──
    input_dir = "input_logs"           # 원본 로그가 들어있는 폴더
    processed_dir = "processed_logs"   # 정상 로그 저장 폴더
    quarantine_dir = "quarantine_logs" # 격리 로그 저장 폴더

    input_file = os.path.join(input_dir, "server_logs.jsonl")

    # ── 2단계: 입력 데이터 확인 및 자동 생성 ──
    # 아직 가짜 로그 파일이 없으면 generator.py를 호출하여 200개의 가짜 로그 생성
    if not os.path.exists(input_file):
        print("Fake data not found. Generating logs...")
        generate_logs(num_logs=200, output_dir=input_dir)

    # ── 3단계: I/O 어댑터 조립 (Dependency Injection) ──
    # 이 부분이 핵심! 어댑터만 교체하면 파이프라인 로직 변경 없이
    # 로컬 파일 → S3, DB, Kafka 등으로 입출력 소스를 변경할 수 있습니다.
    print("Setting up I/O Adapters...")
    reader = LocalFileReader(file_path=input_file)                # 입력 어댑터
    processed_writer = LocalFileWriter(directory=processed_dir)   # 정상 출력 어댑터
    quarantine_writer = LocalFileWriter(directory=quarantine_dir) # 격리 출력 어댑터

    # ── 4단계: 파이프라인 엔진 생성 및 실행 ──
    # Reader와 Writer를 주입하여 파이프라인 인스턴스 생성
    pipeline = LogPipeline(
        reader=reader,
        processed_writer=processed_writer,
        quarantine_writer=quarantine_writer
    )

    print("Running Log Validation Pipeline...")
    pipeline.run()  # 파이프라인 실행 → 검증 → 분류 → 저장


# 이 파일을 직접 실행했을 때만 main() 함수 호출
# (다른 파일에서 import 할 때는 실행되지 않음)
if __name__ == "__main__":
    main()
