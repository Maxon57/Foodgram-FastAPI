from typing import List

from fastapi import APIRouter, Depends
from models import recipe, auth
from services.auth import get_current_user
from services.recipe import Recipes

router = APIRouter(
    prefix='',
    tags=['recipes']
)


@router.get('/ingredients/', response_model=List[recipe.Ingredient])
def get_ingredients(recipe_service: Recipes = Depends()):
    return recipe_service.get_ingredients()


@router.get('/ingredients/{id}', response_model=recipe.Ingredient)
def get_ingredient(id: int, recipe_service: Recipes = Depends()):
    return recipe_service.get_ingredient(id)


@router.get('/tags/', response_model=List[recipe.BaseTag])
def get_tags(recipe_service: Recipes = Depends()):
    return recipe_service.get_tags()


@router.get('/tags/{id}/', response_model=recipe.BaseTag)
def get_tags(id: int, recipe_service: Recipes = Depends()):
    return recipe_service.get_tag(id)


@router.post('/recipes/', response_model=recipe.Recipe)
def create_recipe(
        recipe: recipe.CreateRecipe,
        user: auth.User = Depends(get_current_user),
        recipe_service: Recipes = Depends()
):
    return recipe_service.create_recipe(recipe.dict(), user)
