from pydantic import BaseModel


class BaseIngredient(BaseModel):
    id: int
    name: str
    measurement_unit: str

    class Config:
        orm_mode = True


class BaseTag(BaseModel):
    id: int
    name: str
    color: str
    slug: str

    class Config:
        orm_mode = True