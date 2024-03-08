"""
Модуль, собирающий с пользователя все параметры перед запуском
основной программы.
"""

import os

from .data_source import BaseDataSource, CsvDataSource, InputDataSource
from .data_source import GeneratorDataSource, XlsDataSource, XlsxDataSource
from .generator import BaseGenerator
from .writer import CSVFileWriter, Writer, XlsxFileWriter


class ParamsObject:
    """Класс, собирающий и хранящий объекты с параметрами."""

    data_source: BaseDataSource
    num_lines: int = BaseDataSource.default_num_lines
    data_writer: Writer
    destination_type: str = 'file'

    def __init__(self):
        print('Добро пожаловать в упаковщик архивов!')
        self.get_data_source()
        self.get_data_destination()

    def get_data_source(self) -> None:
        """Получает источник данных."""

        user_choices: dict = {
             '1': ('ввести данные с клавиатуры', self.get_input),
             '2': ('взять данные из файла txt/csv', self.get_csv),
             '3': ('взять данные из файла xlsx', self.get_xlsx),
             '4': ('взять данные из файла xls', self.get_xls),
             '5': ('сгенерировать данные', self.get_generate),
             '6': ('выйти из программы', ParamsObject.exit_program),
        }

        user_choice: str = self.get_user_choice(user_choices)

        if (user_choices[user_choice][1].__name__
                != ParamsObject.exit_program.__name__):
            self.num_lines: int = self.get_num_lines()
        user_choices[user_choice][1]()

    def get_int(self, prompt: str, default_value: int) -> int:
        """Запрашивает целое неотрицательное число."""
        while True:
            number_str: str = input(prompt)
            if not number_str:
                return default_value
            try:
                number: int = int(number_str)
            except ValueError:
                print('Введите целое число.')
            if number < 0:
                print('Введите неотрицательное число.')
            else:
                return number

    def get_num_lines(self) -> int:
        """Запрашивает число строк."""
        return self.get_int(prompt='Введите число строк: ',
                            default_value=BaseDataSource.default_num_lines)

    def get_input(self):
        """Создает объект ввода с клавиатуры."""
        self.data_source = InputDataSource(self.num_lines)

    def get_file_path(self, extensions: tuple, input_file: bool = True) -> str:
        """Получает путь к файлу."""
        while True:
            if input_file:
                invite: str = 'Введите путь к файлу-источнику через /: '
            else:
                invite = 'Введите путь к файлу на запись через /: '
            file_path: str = input(invite)
            if not file_path:
                print('Это обязательный параметр.')
            elif file_path.split('.')[-1] not in extensions:
                print('Неверное расширение файла.')
            elif not input_file and os.path.exists(file_path):
                print('Файл уже существует. Введите другой путь.')
            elif input_file and not os.path.exists(file_path):
                print('Файл не существует. Введите другой путь.')
            else:
                return file_path

    def get_csv(self) -> None:
        """Создает объект ввода из csv."""
        file_path: str = self.get_file_path(CsvDataSource.file_formats,
                                            input_file=True)
        separator: str = (input('Введите символ разделителя при чтении: ') or
                          CsvDataSource.default_separator)
        self.data_source = CsvDataSource(file_path, self.num_lines, separator)

    def get_xlsx(self) -> None:
        """Создает объект ввода из xlsx."""
        file_path: str = self.get_file_path(XlsxDataSource.file_formats,
                                            input_file=True)
        self.data_source = XlsxDataSource(file_path, self.num_lines)

    def get_xls(self) -> None:
        """Создает объект ввода из xls."""
        file_path: str = self.get_file_path(XlsDataSource.file_formats,
                                            input_file=True)
        sheet_number: int = self.get_int(
            prompt='Введите номер листа в файле: ',
            default_value=XlsDataSource.default_sheet_number)
        self.data_source = XlsDataSource(file_path, self.num_lines,
                                         sheet_number)

    def get_generate(self) -> None:
        """Создает объект генерации данных."""

        generator_type: str = (input('Выберите генератор (Faker/Mimesis): ') or
                               GeneratorDataSource.default_generator_type)
        language: str = (input('Выберите язык (русский/английский): ') or
                         BaseGenerator.default_language)
        format: str = (input('Выберите формат (мужские/женские/вперемешку): ')
                       or BaseGenerator.default_format)
        header_choice: str = input('Нужна ли строка заголовков (да/нет): ')
        header = (header_choice == 'да' if header_choice
                  else BaseGenerator.header)
        self.data_source = GeneratorDataSource(
            generator_type=generator_type,
            language=language,
            format=format,
            header=header,
            num_lines=self.num_lines,
        )

    @staticmethod
    def exit_program():
        """Выходит из программы."""
        exit()

    def get_user_choice(self, user_choices: dict) -> str:
        while True:
            choices_list: list = (
                [' - '.join([key, value[0]])
                 for key, value in user_choices.items()])
            choices_string: str = ',\n'.join(choices_list)
            user_choice = input(f"""Выберите:
                                {choices_string}:
                                """)
            if user_choice not in user_choices.keys():
                print('Неверный ввод.')
            else:
                return user_choice

    def get_data_destination(self) -> None:
        """Получает объект записи/архивации данных."""

        user_choices: dict = {
             '1': ('записать в файл txt/csv', self.write_csv),
             '2': ('записать в файл xlsx', self.write_xlsx),
             '6': ('выйти из программы', ParamsObject.exit_program),
        }
        user_choice: str = self.get_user_choice(user_choices)
        user_choices[user_choice][1]()

    def write_csv(self) -> None:
        """Создает объект записи csv/txt."""

        file_path = self.get_file_path(CSVFileWriter.file_formats,
                                       input_file=False)
        separator: str = (input('Введите символ разделителя на запись: ') or
                          CSVFileWriter.default_separator)
        self.data_writer = CSVFileWriter(
            file_path=file_path,
            separator=separator,
        )

    def write_xlsx(self) -> None:
        """Создает объект записи xlsx."""
        file_path = self.get_file_path(XlsxFileWriter.file_formats,
                                       input_file=False)
        self.data_writer = XlsxFileWriter(
            file_path=file_path,
        )
