from pydantic.fields import Field
from pydantic import BaseModel, validator, EmailStr


class BaseUser(BaseModel):
    email: EmailStr
    username: str = Field(min_length=2, max_length=150)
    first_name: str = Field(max_length=150)
    last_name: str = Field(max_length=150)

    class Config:
        orm_mode = True


class User(BaseUser):
    id: int
    is_subscribed: bool = False


class UserCreate(BaseUser):
    password: str = Field(min_length=8, max_length=150)

    @validator('password')
    def check_passwords(cls, v, values, **kwargs):
        if 'username' in values and values['username'] == v:
            raise ValueError('Введённый пароль слишком похож на username.')
        return v


class UserSignIn(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class UserSetPassword(BaseModel):
    new_password: str = Field(min_length=8, max_length=150)
    current_password: str

    @validator('current_password')
    def check_passwords(cls, v, values, **kwargs):
        if 'new_password' in values and values['new_password'] == v:
            raise ValueError('Пароли должны быть уникальными!')
        return v


class GetToken(BaseModel):
    auth_token: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str = 'bearer'
