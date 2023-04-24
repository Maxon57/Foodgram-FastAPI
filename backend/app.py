from typing import Dict, List

import api
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.staticfiles import StaticFiles

tags_metadata = [
    {
        'name': 'auth',
        'description': 'Авторизация и регистрация'
    },
    {
        'name': 'recipes',
        'description': 'Рецепты'
    }
]

app = FastAPI(
    title='Foodgram',
    description='Сервис для просмотра рецептов',
    version='1.0.0',
    openapi_tags=tags_metadata
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
):
    errors: Dict[str, List[str]] = {}

    for error in exc.errors():

        error_field = error['loc'][1]
        error_msg = error['msg']

        if error_field in errors:
            errors[error_field].append[error_msg]

        errors[error_field] = [error_msg]

    return JSONResponse(
        content=errors,
        status_code=status.HTTP_400_BAD_REQUEST
    )


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(api.router)
