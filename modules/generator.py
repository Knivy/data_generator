"""
Генерирует синтетические данные и отдает в виде генератора строк.

Faker медленней, чем Mimesis. Здесь он на каждой строке выбирает, сгенерировать
данные мужские или женские.
"""

from random import choice

from faker import Faker
from mimesis import Generic
from mimesis.locales import Locale
from mimesis.builtins import RussiaSpecProvider
from mimesis.enums import Gender


class BaseGenerator:
    """Базовый класс генератора данных."""

    default_num_lines: int = 500_000  # Сколько нужно строк.
    default_language: str = 'русский'  # На каком языке.
    header = True  # Нужна ли строка заголовков.
    default_format: str = 'general'  # Формат по умолчанию.

    def __init__(self, language: str = default_language,
                 format: str = default_format):
        """
        Инициализирует генератор.

        language - язык.
        format - строковый флаг, нужны ли мужские или женские данные.
        """
        self.get_language(language)
        self.format: str = format

    def get_language(self, language: str = default_language) -> None:
        """Получает настройку языка и создает объект для движка."""
        raise NotImplementedError('Метод должен быть переопреден.')

    def generate_line(self) -> dict:
        """Генерирует строку данных в виде словаря."""
        raise NotImplementedError('Метод должен быть переопреден.')

    def generate(self, num_lines: int = default_num_lines,
                 header: bool = header):
        """
        Генерирует данные и отдает построчно в виде списка строк.

        num_lines - число строк.
        header - флаг, что требуется строка заголовков.
        """
        if header:
            yield list(self.generate_line().keys())

        for _ in range(num_lines):
            yield list(self.generate_line().values())


class FakerGenerator(BaseGenerator):
    """Этот класс генерирует с помощью Faker."""

    def get_language(self, language: str = BaseGenerator.default_language):
        """Получает настройку языка и создает объект Faker."""
        if language == 'русский':
            self.language: str = 'ru_RU'
        else:
            self.language = 'en_EN'
        self.fake: Faker = Faker(self.language)


class MaleFemaleFakerGenerator(FakerGenerator):
    """Задает определенный формат генерируемых данных."""
    format_styles = ('male', 'female')

    def generate_line(self) -> dict:
        """
        Генерирует одну строку в виде словаря по заданному формату.
        Доступны варианты: мужские данные, женские, вперемешку.
        """
        if self.format not in self.format_styles:
            format: str = choice(self.format_styles)
        else:
            format = self.format
        format_dict: dict = {
            'Фамилия': self.fake.last_name_male() if format == 'male'
            else self.fake.last_name_female(),
            'Имя': self.fake.first_name_male() if format == 'male'
            else self.fake.first_name_female(),
            'Пол': 'мужской' if format == 'male' else 'женский',
            'Индекс': self.fake.postcode(),
            'Название города': self.fake.city(),
            'Адрес': self.fake.street_address(),
            'Профессия': self.fake.job(),
            'Номер телефона': self.fake.phone_number(),
            'Сайт': self.fake.hostname(),
            'Почта': self.fake.ascii_free_email(),
            'Компания': self.fake.company(),
        }
        return format_dict


class MimesisGenerator(BaseGenerator):
    """Этот класс генерирует с помощью Mimesis."""

    def get_language(self, language: str = BaseGenerator.default_language):
        """Получает настройку языка и создает объект Mimesis."""
        if language == 'русский':
            self.language: Locale = Locale.RU
            self.mimesis: Generic = Generic(locale=self.language)
            RussiaSpecProvider.Meta.name = 'rus'
            self.mimesis.add_provider(RussiaSpecProvider)
        else:
            self.language = Locale.EN
            self.mimesis = Generic(locale=self.language)


class MaleFemaleMimesisGenerator(MimesisGenerator):
    """Задает определенный формат генерируемых данных."""

    format_styles = ('male', 'female')

    def generate_line(self) -> dict:
        """
        Генерирует одну строку в виде словаря по заданному формату.
        Доступны варианты: мужские данные, женские, вперемешку.
        """
        if self.format not in self.format_styles:
            format: str = choice(self.format_styles)
        else:
            format = self.format
        gender: Gender = Gender.MALE if format == 'male' else Gender.FEMALE
        format_dict: dict = {
            'Фамилия': self.mimesis.last_name(gender),
            'Имя': self.mimesis.first_name(gender),
            'Пол': 'мужской' if format == 'male' else 'женский',
            'Индекс': self.mimesis.postal_code(),
            'Название города': self.mimesis.city(),
            'Дата рождения': self.mimesis.birthdate(),
            'Академическая степень': self.mimesis.academic_degree(),
            'Национальность': self.mimesis.nationality(gender),
            'Профессия': self.mimesis.occupation(),
            'Номер телефона': self.mimesis.phone_number(),
            'Почта': self.mimesis.email(unique=True),
        }
        if self.language == Locale.RU:
            format_dict.update(
                {
                    'Отчество': self.mimesis.rus.patronymic(gender),
                    'ИНН': self.mimesis.rus.inn(),
                    'Паспорт': self.mimesis.rus.series_and_number(),
                    'СНИЛС': self.mimesis.rus.snils(),
                }
            )
        return format_dict
