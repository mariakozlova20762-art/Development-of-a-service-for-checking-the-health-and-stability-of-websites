from pydantic import BaseModel, HttpUrl


class HealthCheckRequest(BaseModel):
    url: HttpUrl


class HealthCheckResponse(BaseModel):
    url: HttpUrl
    status_code: int
    response_time_ms: float
    healthy: bool