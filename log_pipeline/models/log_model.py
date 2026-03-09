"""
models/log_model.py - 서버 로그 데이터 검증 모델 (Pydantic Model)

이 파일의 역할:
    JSON 형태로 들어오는 서버 접속 로그 데이터의 "타입"과 "값"을 자동으로 검증합니다.
    Pydantic의 BaseModel을 상속받아, 각 필드의 자료형이 맞는지 확인하고,
    추가적으로 @model_validator를 통해 "이상 징후(Anomaly)"를 탐지합니다.

확장성:
    이 모델의 필드명만 바꾸면 다른 도메인(예: IoT 센서, 이미지 메타데이터 등)의
    데이터 검증 모델로 그대로 재사용할 수 있습니다.
"""

from pydantic import BaseModel, ConfigDict, model_validator
from typing import Self


class ServerLog(BaseModel):
    """
    서버 접속 로그 한 줄(JSON)을 표현하는 Pydantic 모델.

    Fields:
        ip (str): 접속자의 IP 주소 (예: "192.168.1.5")
        status (int): HTTP 응답 상태 코드 (예: 200, 404, 500)
        user_agent (str): 접속에 사용된 브라우저/클라이언트 정보 (예: "Chrome", "curl")
        response_time_ms (int): 서버 응답 시간 (밀리초 단위, 예: 150)
    """

    ip: str                  # 접속자 IP 주소
    status: int              # HTTP 상태 코드 (200: 정상, 500: 서버 에러)
    user_agent: str          # 브라우저/클라이언트 정보
    response_time_ms: int    # 응답 시간 (ms)

    # JSON에 정의되지 않은 추가 필드가 있어도 무시 (에러를 내지 않음)
    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="after")
    def check_anomaly(self) -> Self:
        """
        이상 징후(Anomaly) 탐지 로직.

        아래 두 가지 조건 중 하나라도 해당하면 ValueError를 발생시켜
        해당 로그를 '비정상 데이터'로 분류합니다.

        조건 1: status >= 500 (서버 내부 에러)
            - 500, 502, 503, 504 등의 상태 코드는 서버 장애를 의미
        조건 2: response_time_ms >= 5000 (응답 지연 5초 이상)
            - 정상적인 웹 서버라면 5초 이상 걸리는 경우는 비정상

        Returns:
            Self: 검증을 통과한 경우, 자기 자신(self)을 반환합니다.

        Raises:
            ValueError: 이상 징후가 감지되면 발생하며, pipeline.py에서
                        ValidationError로 캐치됩니다.
        """
        if self.status >= 500:
            raise ValueError(f"Anomaly detected: Server error status {self.status}")
        if self.response_time_ms >= 5000:
            raise ValueError(f"Anomaly detected: High latency {self.response_time_ms}ms")
        return self
