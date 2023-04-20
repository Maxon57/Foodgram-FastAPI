from typing import List
from fastapi import APIRouter, Depends, status

from services.auth import (
    AuthUsers, get_current_user)
from models import auth

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post(
    '/',
    response_model=auth.User,
    status_code=status.HTTP_201_CREATED,
)
def sign_up(
        user_data: auth.UserCreate,
        auth_service: AuthUsers = Depends()
):
    """Регистрация пользователя."""
    return auth_service.register_new_user(user_data)


@router.get('/', response_model=List[auth.User])
def get_users(auth_service: AuthUsers = Depends()):
    """Выдача пользователей"""
    return auth_service.get_users_all()


@router.get(
    '/me/',
    response_model=auth.User
)
def get_user_me(user: auth.User = Depends(get_current_user)):
    """Получение текущего пользователя"""
    return user


@router.get('/{id}/', response_model=auth.User)
def get_user(
        id: int,
        user: auth.User = Depends(get_current_user),
        auth_service: AuthUsers = Depends()
):
    """Выдача пользователя по id."""
    return auth_service.get_user(id)


@router.post(
    '/set_password/',
    status_code=status.HTTP_201_CREATED
)
def set_password(
        data_password: auth.UserSetPassword,
        user: auth.User = Depends(get_current_user),
        auth_service: AuthUsers = Depends()
):
    return auth_service.set_password(user, data_password)