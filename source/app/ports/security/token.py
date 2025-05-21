from abc import ABC, abstractmethod
from datetime import timedelta


class TokenService(ABC):
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    @abstractmethod
    def create_token(
        self, user_name: str, role: str, expires_delta: timedelta | None = None
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        raise NotImplementedError
