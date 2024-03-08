"""
Модуль для записи данных в файл.

Получает генератор списков строк и пишет в нужный формат файла.
"""

from typing import Generator

import xlsxwriter  # type: ignore[import-untyped]


class Writer:
    """Базовый класс записи файлов."""

    file_formats: tuple

    def __init__(self, file_path: str):
        """Получает путь к файлу нужного формата."""
        self.file_path = file_path

    def write_data(self, data: Generator):
        """Запись файла."""
        raise NotImplementedError('Этот метод должен быть переопределен.')


class CSVFileWriter(Writer):
    """Запись csv/txt."""

    file_formats = ('csv', 'txt')
    default_separator: str = ','

    def __init__(self, file_path: str, separator: str = default_separator):
        super().__init__(file_path)
        self.separator = separator

    def write_data(self, data: Generator):
        """Запись файла."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            for line in data:
                print(self.separator.join(line), file=f)


class XlsxFileWriter(Writer):
    """Запись xlsx."""
    file_formats = ('xlsx',)

    def write_data(self, data: Generator):
        """Запись файла."""
        workbook = xlsxwriter.Workbook(self.file_path)
        worksheet = workbook.add_worksheet()
        i = 0
        for line in data:
            worksheet.write_row(i, 0, line)
            i += 1
        workbook.close()
