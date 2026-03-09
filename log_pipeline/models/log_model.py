from pydantic import BaseModel, ConfigDict, model_validator
from typing import Self

class ServerLog(BaseModel):
    ip: str
    status: int
    user_agent: str
    response_time_ms: int

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="after")
    def check_anomaly(self) -> Self:
        if self.status >= 500:
            raise ValueError(f"Anomaly detected: Server error status {self.status}")
        if self.response_time_ms >= 5000:
            raise ValueError(f"Anomaly detected: High latency {self.response_time_ms}ms")
        return self
