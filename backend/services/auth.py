import hashlib
import os
import uuid
from datetime import datetime, timedelta
from typing import List
from typing_extensions import Annotated

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_session
import tables
from settings import settings
from pydantic import ValidationError
from fastapi_jwt_auth import AuthJWT

from models import auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token/login/')


def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session),
        Authorize: AuthJWT = Depends()
) -> auth.User:
    """Выдает текущего пользователя."""

    Authorize.jwt_required()

    user_data_from_token = AuthUsers.verify_token(token)

    user = (
            session
            .query(tables.User)
            .filter(tables.User.username == user_data_from_token.username)
            .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user


class AuthUsers:
    @classmethod
    def verify_password(cls, plain_password: str,
                        hashed_password: str) -> bool:
        """Проверяет сырой пароль и хешированный"""
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Хеширует сырой пароль."""
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls, token: str) -> auth.User:
        """Проверка корректности токена. Выдача пользователя из токена"""
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[settings.jwt_algorithm]
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = auth.User.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: tables.User) -> auth.GetToken:
        """Создает токен, взяв за основу данные пользователя."""
        user_data = auth.User.from_orm(user)
        now = datetime.utcnow()
        hash_str = f"{user.id}:{str(uuid.uuid4())}"
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(days=settings.access_expires),
            'sub': str(user_data.id),
            'type': 'access',
            'jti': hashlib.sha256(hash_str.encode()).hexdigest(),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.authjwt_secret_key,
            algorithm=settings.jwt_algorithm
        )
        return auth.GetToken(auth_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: auth.UserCreate) -> auth.User:
        """Создание нового пользователя."""
        user = tables.User(
            email=user_data.email,
            username=user_data.username,
            password=self.hash_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        self.session.add(user)
        self.session.commit()
        return user

    def authenticate_user(self, email: str, password: str) -> auth.GetToken:
        """Аутентификация пользователя."""
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        user = (
            self.session
                .query(tables.User)
                .filter(tables.User.email == email)
                .first()
        )

        if not user:
            raise exception

        if not self.verify_password(password, user.password):
            raise exception

        return self.create_token(user)

    def get_users_all(self) -> List[auth.User]:
        """Выдача всех имеющихся пользователей."""
        return self.session.query(tables.User).all()

    def get_user(self, id: int) -> auth.User:
        """Получение пользователя из БД."""
        user = self.__get_user(id)
        return auth.User.from_orm(user)

    def __get_user(self, id: int) -> tables.User:
        """Получет объект ORM пользователя."""
        user = (
            self.session
                .query(tables.User)
                .filter(tables.User.id == id)
                .first()
        )

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return user

    def set_password(
            self,
            user: auth.User,
            data_password: auth.UserSetPassword
    ):
        """Изменение пароля пользователя."""
        exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        user = self.__get_user(user.id)

        if not self.verify_password(
                data_password.current_password, user.password
        ):
            raise exception

        user.password = self.hash_password(data_password.new_password)

        self.session.commit()
        self.session.refresh(user)