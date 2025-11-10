from src.config import settings
from passlib.context import CryptContext
from datetime import timedelta, timezone, datetime
from fastapi import HTTPException
import jwt


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def create_access_token(self, data: dict) -> str:
        """Создание токена при аутентификации"""
        to_encode = data.copy()
        expire = (
                datetime.now(timezone.utc) +
                timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    def hashed_password(self, password: str) -> str:
        """Перевод пароля в хэш-значение"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Проверка пароля при аутентификации"""
        return self.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный токен")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Время действия токена истекло")


auth_service = AuthService()
