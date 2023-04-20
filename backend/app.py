import api
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

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


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.include_router(api.router)
