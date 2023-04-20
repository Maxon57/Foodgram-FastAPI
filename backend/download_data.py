import json
import os

from typing import List
from database import Session
from tables import Ingredient, Tag


def open_file_json(file: str) -> List[dict]:
    path = os.path.join(os.getcwd(), 'data/', file + '.json')
    try:
        with open(path, 'r', encoding='UTF-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f'Файла с путем {path} не существует!')


def main():
    data_files = [
        'ingredients',
        'tag'
    ]
    tables = [
        Ingredient,
        Tag
    ]

    with Session() as session:
        try:
            for num in range(len(tables)):
                collect = [tables[num](**data) for data in
                           open_file_json(data_files[num])]
                session.add_all(collect)
                session.commit()

        except Exception as err:
            print(f'Возникла ошибка: {err}')


if __name__ == '__main__':
    main()
