"""Упаковывает в архив."""

import zipfile as zf
import os
from typing import Optional, Generator
import aspose.zip as az


class Zipper:
    """Основной класс упаковки в архив."""

    def __init__(self):
        """Получает число строк в одном файле и путь до архива."""
        self.num_lines = self.get_num_lines()
        self.get_path()

    def get_num_lines(self):
        """Получает число строк в файле."""
        while True:
            try:
                return int(input(
                    'Введите, на сколько строк разбить файлы: ') or 0)
            except ValueError:
                pass

    def get_path(self):
        """Получает путь до архива."""
        while True:
            self.format = input('Введите формат архива: 7z или zip: ')
            if self.format in ['7z', 'zip']:
                break
        while True:
            zip_path = input(f'Введите путь к архиву {self.format}: ')
            if os.path.exists(zip_path):
                print('Этот архив уже существует.')
            elif not zip_path.endswith(self.format):
                print('Расширение должно быть {self.format}.')
            else:
                break
        self.path = zip_path

    def write_xlsx(self, file_path: Optional[str] = None):
        """Пишет xlsx."""
        if not file_path:
            while True:
                file_path = input('Введите путь к файлу xlsx: ')
                if os.path.exists(file_path):
                    print('Этот файл уже существует.')
                elif not file_path.endswith('.xlsx'):
                    print('Расширение должно быть xslx.')
                else:
                    break
        if self.format == 'zip':
            with zf.ZipFile(self.path, mode='a') as zfile:
                zfile.write(file_path)
        else:
            with az.sevenzip.SevenZipArchive() as zfile:
                zfile.create_entry(file_path.split('.')[0], file_path)
                zfile.save(self.path)

    def write_gen_zip(self, data: Generator[list[str], None, None]):
        """Пишет zip c поданного генератора списка строк."""
        while True:
            file_name = input('Введите имя для файла в архиве: ')
            if (not file_name.endswith('.csv')
                    and not file_name.endswith('.txt')):
                print('Расширение должно быть csv/txt.')
            else:
                break
        sep = input('Введите разделитель: ') or ','
        count = 0
        file_count = 0
        while True:
            f_name = (file_name.split('.')[0] + str(file_count) + '.'
                      + file_name.split('.')[-1])
            with zf.ZipFile(self.path, mode='a') as zfile:
                for line in data:
                    try:
                        label: str | zf.ZipInfo = zfile.getinfo(f_name)
                    except KeyError:
                        label = f_name
                    zfile.writestr(label, sep.join(line))
                    count += 1
                    if count == self.num_lines:
                        file_count += 1
                        count = 0
                        break
                    else:
                        continue
                else:
                    break

    def write_file_7z(self, file_path: Optional[str] = None):
        """Пишет 7z с поданного файла."""
        if not file_path:
            while True:
                file_path = input('Введите путь к файлу csv/txt: ')
                if os.path.exists(file_path):
                    print('Этот файл уже существует.')
                elif (not file_path.endswith('.csv')
                        and not file_path.endswith('.txt')):
                    print('Расширение должно быть csv/txt.')
                else:
                    break
        if self.format == 'zip':
            with zf.ZipFile(self.path, mode='a') as zfile:
                zfile.write(file_path)
        else:
            with az.sevenzip.SevenZipArchive() as zfile:
                zfile.create_entry(file_path.split('.')[0], file_path)
                zfile.save(self.path)
