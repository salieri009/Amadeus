"""
generator.py - 가짜 서버 로그 생성기 (Fake Log Generator)

이 파일의 역할:
    파이프라인을 테스트하기 위한 가짜(Mock) 서버 접속 로그를 JSON Lines(.jsonl) 형식으로 생성합니다.
    실제 운영 환경에서는 이 파일 대신 Nginx, Apache 등의 웹 서버가 로그를 생성하게 됩니다.

생성되는 데이터 예시:
    {"ip": "192.168.1.5", "status": 200, "user_agent": "Chrome", "response_time_ms": 150}

비정상 데이터 비율:
    - 약 10%의 확률로 에러 상태 코드 (500, 502, 503, 504)
    - 약 10%의 확률로 높은 응답 시간 (5000ms ~ 10000ms)
    - 두 조건은 독립적이므로, 약 1%는 둘 다 해당될 수 있음
"""

import json
import random
import os


def generate_logs(num_logs: int = 100, output_dir: str = "input_logs"):
    """
    가짜 서버 접속 로그를 생성하여 JSONL 파일로 저장합니다.

    Args:
        num_logs (int): 생성할 로그 개수 (기본값: 100)
        output_dir (str): 로그 파일을 저장할 디렉토리 경로 (기본값: "input_logs")

    Output:
        {output_dir}/server_logs.jsonl 파일이 생성됩니다.
    """

    # 출력 디렉토리가 없으면 자동 생성
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "server_logs.jsonl")

    # ── 가짜 데이터 풀(Pool) 정의 ──
    # 가상의 내부 네트워크 IP 주소 목록 (192.168.1.1 ~ 192.168.1.19)
    ips = [f"192.168.1.{i}" for i in range(1, 20)]

    # 실제 웹에서 볼 수 있는 User-Agent 문자열 목록
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",  # Windows Chrome
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",                # Mac Safari
        "curl/7.68.0",                                                    # 터미널 curl 요청
        "python-requests/2.25.1"                                          # Python 스크립트 요청
    ]

    # ── JSONL 파일 생성 ──
    # JSONL(JSON Lines): 한 줄에 하나의 JSON 객체를 저장하는 형식
    # 대량 로그 처리에 적합 (한 줄씩 스트리밍 읽기 가능)
    with open(file_path, "w", encoding="utf-8") as f:
        for _ in range(num_logs):
            # 10% 확률로 에러 상태 코드 생성
            is_error = random.random() < 0.1
            # 10% 확률로 느린 응답 시간 생성
            is_slow = random.random() < 0.1

            log = {
                "ip": random.choice(ips),
                # 에러면 5xx, 정상이면 2xx/3xx/4xx 중 랜덤 선택
                "status": random.choice([500, 502, 503, 504]) if is_error
                          else random.choice([200, 201, 301, 302, 400, 401, 403, 404]),
                "user_agent": random.choice(user_agents),
                # 느리면 5000~10000ms, 정상이면 10~1000ms
                "response_time_ms": random.randint(5000, 10000) if is_slow
                                    else random.randint(10, 1000)
            }
            # JSON 한 줄 + 개행문자로 기록
            f.write(json.dumps(log) + "\n")

    print(f"Generated {num_logs} logs at {file_path}")


# 이 파일을 직접 실행하면 기본값(100개)으로 로그 생성
if __name__ == "__main__":
    generate_logs()
