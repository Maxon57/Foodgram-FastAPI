from pydantic import BaseSettings
from fastapi_jwt_auth import AuthJWT


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000

    database_url: str = 'sqlite:///./backend/db.sqlite'

    authjwt_secret_key: str = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access"}
    jwt_algorithm: str = 'HS256'
    access_expires: int = 1


@AuthJWT.load_config
def get_config():
    return Settings()


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
