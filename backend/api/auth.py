from database import redis_conn
from services.auth import AuthUsers, get_current_user
from fastapi import APIRouter, Depends, status
from models import auth
from fastapi_jwt_auth import AuthJWT
from datetime import timedelta
from settings import settings

router = APIRouter(
    prefix='/auth/token',
    tags=['auth'],
)


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    entry = redis_conn.get(jti)

    return entry and entry == 'true'


@router.post(
    '/login/',
    response_model=auth.GetToken,
)
def sign_in(
        auth_data: auth.UserSignIn,
        auth_service: AuthUsers = Depends()
):
    return auth_service.authenticate_user(
        auth_data.email,
        auth_data.password,
    )


@router.delete('/logout', status_code=status.HTTP_204_NO_CONTENT)
def logout(
        Authorize: AuthJWT = Depends(),
        user: auth.User = Depends(get_current_user)
):
    Authorize.jwt_required()

    jti = Authorize.get_raw_jwt()['jti']
    redis_conn.setex(jti, timedelta(days=settings.access_expires), 'true')
    return {"detail": "Access token has been revoke"}
