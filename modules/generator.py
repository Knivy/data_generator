"""Генерирует синтетические данные."""

from faker import Faker
from random import choice


class Generator:
    """Базовый класс генератора данных."""

    def __init__(self, language='ru_RU'):
        """
        Инициализируем.

        language - язык.
        """
        self.language: str = language

    def generate(self, num_lines: int = 500_000):
        """
        Генерируем.

        num_lines - число строк.
        """
        raise NotImplementedError('Этот метод должен быть переопределён.')


class FakerGenerator(Generator):
    """Этот класс генерирует с помощью Faker."""

    def __init__(self, language: str = 'ru_RU', format: str = 'general'):
        """
        Инициализирует генератор.

        fake - объект Faker.
        format - строковый флаг, нужны ли мужские или женские данные.
        """
        super().__init__(language)
        self.fake: Faker = Faker(self.language)
        self.format: str = format

    def gen_data(self):
        """Генерирует строку данных в виде словаря."""
        raise NotImplementedError('Метод должен быть переопреден.')

    def generate(self, num_lines: int = 500_000, header: bool = True):
        """
        Генерирует данные и отдает построчно в виде списка строк.

        num_lines - число строк.
        header - флаг, что требуется строка заголовков.
        """
        if header:
            format_dict = self.gen_data()
            yield list(format_dict.keys())

        for _ in range(num_lines):
            format_dict = self.gen_data()
            yield list(format_dict.values())


class MaleFemaleGenerator(FakerGenerator):
    """Задает определенный формат генерируемых данных."""

    def gen_data(self) -> dict:
        """
        Генерирует одну строку в виде словаря по заданному формату.
        Доступны варианты: мужские данные, женские, вперемешку.
        """
        format_dict_male: dict = {
            'Фамилия': self.fake.last_name_male(),
            'Имя': self.fake.first_name_male(),
            'Пол': 'мужской'
        }
        format_dict_female: dict = {
            'Фамилия': self.fake.last_name_female(),
            'Имя': self.fake.first_name_female(),
            'Пол': 'женский'
        }
        format_dict_general: dict = {
            'Индекс': self.fake.postcode(),
            'Название города': self.fake.city(),
            'Адрес': self.fake.street_address(),
            'Профессия': self.fake.job(),
            'Номер телефона': self.fake.phone_number(),
            'Сайт': self.fake.hostname(),
            'Почта': self.fake.ascii_free_email(),
            'Компания': self.fake.company()
        }
        if self.format not in ('male', 'female'):
            format: str = choice(('male', 'female'))
        else:
            format = self.format

        match format:
            case 'male':
                format_dict: dict = format_dict_male
            case _:
                format_dict = format_dict_female
        format_dict.update(format_dict_general)
        return format_dict
