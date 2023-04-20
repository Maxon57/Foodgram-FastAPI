from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models import recipe
from tables import Ingredient, Tag
from database import Session, get_session

router = APIRouter(
    prefix='',
    tags=['recipes']
)


@router.get('/ingredients/', response_model=List[recipe.BaseIngredient])
def get_ingredient_all(session: Session = Depends(get_session)):
    ingredients = session.query(Ingredient).all()
    return ingredients


@router.get('/ingredients/{id}', response_model=recipe.BaseIngredient)
def get_ingredient_item(id: int, session: Session = Depends(get_session)):
    ingredient = session.query(Ingredient).filter_by(id=id).first()
    if not ingredient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return ingredient


@router.get('/tags/', response_model=List[recipe.BaseTag])
def get_ingredient_all(session: Session = Depends(get_session)):
    ingredients = session.query(Tag).all()
    return ingredients


@router.get('/tags/{id}', response_model=recipe.BaseTag)
def get_ingredient_item(id: int, session: Session = Depends(get_session)):
    tag = session.query(Tag).filter_by(id=id).first()
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return tag


