"""
Модуль для записи данных в файл.

Получает генератор списков строк и пишет в нужный формат файла.
"""

from typing import Generator
import os
import xlsxwriter


class Writer:

    file_formats: list = ['']

    def __init__(self):
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
        raise NotImplementedError('Этот метод должен быть переопределен.')

    def get_filepath(self) -> str:
        while True:
            filepath = input('Введите путь к файлу на запись: ')
            if not filepath or os.path.exists(filepath):
                print('Введите другой путь.')
            else:
                break
        return filepath


class CSVFileWriter(Writer):
    file_formats = ['csv', 'txt']

    def write_data(self, data: Generator[list[str], None, None]):
        sep = input('Введите разделитель: ') or ','
        with open(self.filepath, 'w', encoding='utf-8') as f:
            for line in data:
                print(sep.join(line), file=f)


class XlsxFileWriter(Writer):
    file_formats = ['xlsx']

    def write_data(self, data: Generator[list[str], None, None]):
        workbook = xlsxwriter.Workbook(self.filepath)
        worksheet = workbook.add_worksheet()
        i = 0 
        for line in data:
            worksheet.write_row(i, 0, line)
            i += 1
        workbook.close()
