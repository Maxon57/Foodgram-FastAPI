import os.path
from typing import List, Dict
import base64
from PIL import Image
from io import BytesIO
from pathlib import Path

import tables
from . import MEDIA_ROOT
from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_session
from tables import Ingredient, Tag
from models import recipe, auth
from fastapi import HTTPException, status

from random import choices

class Recipes:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_ingredients(self) -> List[recipe.Ingredient]:
        return self.session.query(Ingredient).all()

    def get_ingredient(self, id: int) -> recipe.Ingredient:
        return self.__get_ingredient(id)

    def get_tags(self) -> List[recipe.BaseTag]:
        return self.session.query(Tag).all()

    def get_tag(self, id: int) -> recipe.BaseTag:
        return self.__get_tag(id)

    def recipe_create_or_update(
            self,
            instance,
            raw_data
    ) -> recipe.Recipe:
        """
        Метод для создания или обновления ингредиентов и тегов.
        """
        ingredients, tags = (
            raw_data.pop('ingredients'), raw_data.pop('tags')
        )

        for item in ingredients:
            ingredient = tables.RecipeIngredient(
                recipe=instance,
                ingredient=self.__get_ingredient(item['id']),
                amount=item['amount']
            )
            self.session.add(ingredient)

        for item in tags:
            tag = tables.RecipeTag(
                recipe=instance,
                tag=self.__get_tag(item)
            )

            self.session.add(tag)

        self.session.commit()

        return instance

    def create_recipe(
            self,
            recipe_data,
            user: auth.User
    ) -> recipe.Recipe:
        raw_data = {
            'ingredients': recipe_data.pop('ingredients'),
            'tags': recipe_data.pop('tags'),
        }

        image = UploadFile(recipe_data.pop('image')).file_base64
        recipe = tables.Recipe(**recipe_data, image=image, author=user)

        self.session.add(recipe)
        self.session.commit()

        return self.recipe_create_or_update(recipe, raw_data)

    def __get_ingredient(self, id: int) -> Ingredient:
        ingredient = self.session.query(Ingredient).filter_by(id=id).first()
        if not ingredient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return ingredient

    def __get_tag(self, id: int) -> Tag:
        tag = self.session.query(Tag).filter_by(id=id).first()
        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return tag


class UploadFile:
    save_directory: str = Path(__file__).stem

    def __init__(self, file_base64: str):
        self.file_base64 = self.decode_file(file_base64)

    def decode_file(self, file):
        format, imgstr = file.split(';base64,')
        ext = format.split('/')[-1]
        image_data = base64.b64decode(imgstr)
        image: Image = Image.open(BytesIO(image_data))
        image.filename = f'temp_{"".join(w for w in choices(imgstr, k=10) if w != "/")}.' + ext

        return self.__save_file(image)

    def __save_file(self, file: Image):
        path = os.path.join(MEDIA_ROOT, self.save_directory)

        if not os.path.exists(path):
            os.mkdir(path)

        file.save(path + f'/{file.filename}')

        return path + f'/{file.filename}'

