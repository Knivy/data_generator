"""Модуль, собирающий с пользователя все параметры перед запуском основной программы."""

class ParamsObject:
    """Класс, собирающий и хранящий параметры."""

    def get_num_lines(self):
        """Запрашивает число строк."""
        while True:
            try:
                num_lines = int(input('Введите число строк: '))
            except ValueError:
                print('Неверный ввод.')
            if num_lines >= 0:
                break
            else:
                print('Введите неотрицательное число.')
        return num_lines   
    

    lang = input('Введите язык (по умолчанию ru_RU): ') or 'ru_RU'
        format = input('Введите формат male/female/general: ') or 'general'
    file_path = input('Введите путь к файлу через /: ')
        sep = input('Введите символ разделителя: ')
    
            if file_path.split('.')[-1] not in self.file_formats:
            raise WrongExtension

class WrongExtension(Exception):
    """Класс пользовательского исключения при неверном расширении."""

    def __str__(self):
        return 'Неверное расширение файла.'