from dataclasses import dataclass

@dataclass
class RateLimitResponse:
    limit: int
    current_requests: int
    time_to_refresh: int

    @property
    def remaining_requests(self) -> int:
        return self.limit - self.current_requests

    def __dict__(self) -> dict:
        return {
            "limit": self.limit,
            "current_requests": self.current_requests,
            "time_to_refresh": self.time_to_refresh,
            "remaining_requests": self.remaining_requests,
        }