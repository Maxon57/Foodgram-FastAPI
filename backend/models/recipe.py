from typing import List

from pydantic import BaseModel, validator, Field
from .auth import User


class BaseIngredient(BaseModel):
    id: int

    class Config:
        orm_mode = True


class Ingredient(BaseIngredient):
    name: str = Field(max_length=200)
    measurement_unit: str


class GetRecipeIngredient(Ingredient):
    amount: int


class CreateRecipeIngredient(BaseIngredient):
    amount: int = Field(gte=1)


class BaseTag(BaseModel):
    id: int
    name: str
    color: str
    slug: str

    class Config:
        orm_mode = True


class BaseRecipe(BaseModel):
    image: str
    name: str
    text: str
    cooking_time: int = Field(gte=1)


class Recipe(BaseRecipe):
    id: int
    tags: List[BaseTag]
    ingredients: List[GetRecipeIngredient]
    is_favorited: bool = False
    is_in_shopping_cart: bool = False
    author: User

    class Config:
        orm_mode = True


class CreateRecipe(BaseRecipe):
    ingredients: List[CreateRecipeIngredient]
    tags: List[int]

    @validator('image')
    def check_base64(cls, v: str, values, **kwargs):
        if not v.startswith('data:image'):
            raise ValueError('Загруженный файл не является корректным файлом.')
        return v