from dataclasses import dataclass


@dataclass
class GenerateTokenResponse:
    refresh_token: str
    access_token: str
    expired_at: int
