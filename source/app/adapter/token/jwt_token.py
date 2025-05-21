from datetime import datetime, timedelta

from jose import jwt

from source.app.ports.security.token import TokenService


class JWTTokenService(TokenService):
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(
        self, user_name: str, role: str, expires_delta=None, *args, **kwargs
    ):
        to_encode = {"sub": user_name, "role": role}
        expire = datetime.now() + (expires_delta or timedelta(minutes=30))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
