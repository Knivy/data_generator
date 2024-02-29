"""
Модуль для записи данных в файл.

Получает генератор списков строк и пишет в нужный формат файла.
Нужен для случаев, когда я не знаю, как писать сразу в архив.
"""

from typing import Generator
import os
import xlsxwriter


class Writer:
    """Базовый класс записи файлов."""

    file_formats: list = ['']

    def __init__(self):
        """Получает путь к файлу нужного формата."""
        while True:
            self.filepath = self.get_filepath()
            flag = False
            for format in self.file_formats:
                if self.filepath.endswith(format):
                    flag = True
                    break
            if flag:
                break

    def write_data(self, data: Generator[list[str], None, None]):
        """Запись файла."""
        raise NotImplementedError('Этот метод должен быть переопределен.')

    def get_filepath(self) -> str:
        """Получение пути к файлу."""
        while True:
            filepath = input('Введите путь к файлу на запись: ')
            if not filepath or os.path.exists(filepath):
                print('Введите другой путь.')
            else:
                break
        return filepath


class CSVFileWriter(Writer):
    """Запись csv/txt."""
    file_formats = ['csv', 'txt']

    def write_data(self, data: Generator[list[str], None, None]):
        """Запись файла."""
        sep = input('Введите разделитель: ') or ','
        with open(self.filepath, 'w', encoding='utf-8') as f:
            for line in data:
                print(sep.join(line), file=f)


class XlsxFileWriter(Writer):
    """Запись xlsx."""
    file_formats = ['xlsx']

    def write_data(self, data: Generator[list[str], None, None]):
        """Запись файла."""
        workbook = xlsxwriter.Workbook(self.filepath)
        worksheet = workbook.add_worksheet()
        i = 0
        for line in data:
            worksheet.write_row(i, 0, line)
            i += 1
        workbook.close()
