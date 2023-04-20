import datetime

from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sq
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """
    Модель User.
    """
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key=True)
    email = sq.Column(sq.String(254), unique=True)
    password = sq.Column(sq.String(150))
    username = sq.Column(sq.String(150), unique=True)
    first_name = sq.Column(sq.String(150))
    last_name = sq.Column(sq.String(150))

    recipe = relationship(
        'Recipe',
        back_populates='author'
    )
    follower = relationship(
        'Follow',
        back_populates='users',
        foreign_keys='Follow.user_id'
    )
    following = relationship(
        'Follow',
        back_populates='followers',
        foreign_keys='Follow.author_id'
    )
    favorite_user = relationship('Favorite', back_populates='user')
    purchase_user = relationship('Purchase', back_populates='user')

    def __str__(self):
        return self.username


class Follow(Base):
    """
    Модель с подписками.
    """
    __tablename__ = 'follow'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.ForeignKey('user.id', ondelete='CASCADE'))
    author_id = sq.Column(sq.ForeignKey('user.id', ondelete='CASCADE'))

    users = relationship(
        'User',
        back_populates='follower',
        foreign_keys=[user_id]
    )
    followers = relationship(
        'User',
        back_populates='following',
        foreign_keys=[author_id]
    )

    __table_args__ = (
        sq.UniqueConstraint(
            'user_id',
            'author_id',
            name='unique_user_author'
        ),
    )

    def __str__(self):
        return f'{self.user.username} подписался на {self.author.username}'


class Tag(Base):
    """
    Модель с тегами к рецептам.
    """
    __tablename__ = 'tag'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(50), unique=True, nullable=False)
    color = sq.Column(sq.String(150), unique=True, nullable=False)
    slug = sq.Column(sq.String(50), unique=True, nullable=False)

    recipes = relationship(
        'RecipeTag',
        back_populates='tag',
    )

    def __str__(self):
        return self.name


class Ingredient(Base):
    """
    Модель с ингредиентами к рецептам.
    """
    __tablename__ = 'ingredient'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(150), index=True)
    measurement_unit = sq.Column(sq.String(10))

    recipes = relationship(
        'RecipeIngredient',
        back_populates='ingredient'
    )

    def __str__(self):
        return self.name


class Recipe(Base):
    """
    Модель с рецептами.
    """
    __tablename__ = 'recipe'

    id = sq.Column(sq.Integer, primary_key=True)
    author_id = sq.Column(sq.ForeignKey('user.id', ondelete='CASCADE'))
    tags = relationship(
        'RecipeTag',
        back_populates='recipe'
    )
    ingredients = relationship(
        'RecipeIngredient',
        back_populates='recipe'
    )
    name = sq.Column(sq.String(200))
    image = sq.Column(sq.String, nullable=False)
    text = sq.Column(sq.Text)
    cooking_time = sq.Column(sq.SmallInteger)
    pub_date = sq.Column(sq.DateTime, default=datetime.datetime.now)

    author = relationship('User', back_populates='recipe')
    favorite_recipe = relationship('Favorite', back_populates='recipe')
    purchase_recipe = relationship('Purchase', back_populates='recipe')

    def __str__(self):
        return self.name


class RecipeTag(Base):
    """
    Промежуточная модель многие ко многим
    для поля tags модели Recipes
    """
    __tablename__ = 'recipes_tags'

    recipe_id = sq.Column(sq.ForeignKey('recipe.id'), primary_key=True)
    tag_id = sq.Column(sq.ForeignKey('tag.id'), primary_key=True)

    recipe = relationship('Recipe', back_populates='tags')
    tag = relationship('Tag', back_populates='recipes')


class RecipeIngredient(Base):
    """
    Промежуточная модель многие ко многим
    для поля ingredients модели Recipe.
    """
    __tablename__ = 'recipes_ingredients'

    recipe_id = sq.Column(
        sq.ForeignKey('recipe.id', ondelete='CASCADE'),
        primary_key=True
    )
    ingredient_id = sq.Column(
        sq.ForeignKey('ingredient.id', ondelete='CASCADE'),
        primary_key=True
    )
    amount = sq.Column(sq.SmallInteger)

    recipe = relationship('Recipe', back_populates='ingredients')
    ingredient = relationship('Ingredient', back_populates='recipes')

    __table_args__ = (
        sq.UniqueConstraint(
            'recipe_id',
            'ingredient_id',
            name='unique_recipe_ingredient'
        ),
    )

    def __str__(self):
        return f'{self.recipe}: {self.ingredient} - {self.amount}'


class Favorite(Base):
    """
    Модель для избранных рецептов.
    """
    __tablename__ = 'favorite'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.ForeignKey('user.id', ondelete='CASCADE'))
    recipe_id = sq.Column(sq.ForeignKey('recipe.id', ondelete='CASCADE'))

    user = relationship('User', back_populates='favorite_user')
    recipe = relationship('Recipe', back_populates='favorite_recipe')

    __table_args__ = (
        sq.UniqueConstraint(
            'user_id',
            'recipe_id',
            name='unique_favorite'
        ),
    )

    def __str__(self):
        return f'Избранное: {self.user} - {self.recipe}'


class Purchase(Base):
    """
    Модель со списком рецептов.
    """
    __tablename__ = 'purchase'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.ForeignKey('user.id', ondelete='CASCADE'))
    recipe_id = sq.Column(sq.ForeignKey('recipe.id', ondelete='CASCADE'))

    user = relationship('User', back_populates='purchase_user')
    recipe = relationship('Recipe', back_populates='purchase_recipe')

    __table_args__ = (
        sq.UniqueConstraint(
            'user_id',
            'recipe_id',
            name='unique_purchase'
        ),
    )

    def __str__(self):
        return f'Покупка: {self.user} -  {self.recipe}'
