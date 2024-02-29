"""Основной модуль программы-упаковщика. 

Тестирование выявило проблемы:
при записи в zip каждая строка пишется отдельным файлом,
несколько раз с одинаковым названием. Эти файлы не читаются.
Запись 7z аварийно останавливается, создавая пустой файл.
Протестировано не всё, что касается упаковки в архив.
Генерация, запись в файлы вроде работает.
"""

from modules import InputDataSource, GeneratorDataSource, FileDataSource
from modules import Writer
from modules import CSVFileWriter, XlsxFileWriter, XlsxDataSource, Zipper

if __name__ == '__main__':
    print('Добро пожаловать в упаковщик архивов!')
    while True:
        user_choice = input("""Выберите:
                            1 - ввести данные с клавиатуры,
                            2 - взять данные из файла txt/csv,
                            3 - взять данные из файла xlsx,
                            4 - сгенерировать данные:
                            """)
        if user_choice not in ['1', '2', '3', '4']:
            print('Неверный ввод.')
        else:
            break
    # Отдает данные построчно списками строк.
    match user_choice:
        case '1':
            ids = InputDataSource().get_data()
        case '2':
            ids = FileDataSource().get_data()
        case '3':
            ids = XlsxDataSource().get_data()
        case '4':
            ids = GeneratorDataSource().get_data()
    while True:
        user_choice = input("""Выберите формат выходных данных:
                            1 - xlsx,
                            2 - csv,
                            3 - txt:
                            """)
        if user_choice not in ['1', '2', '3']:
            print('Неверный ввод.')
        else:
            break
    zfile = Zipper()
    match user_choice:
        case '1':  # xlsx пишет сперва файл, причем одним куском.
            wr: Writer = XlsxFileWriter()
            wr.write_data(ids)
            zfile.write_xlsx(wr.filepath)
        case _:  # csv/txt
            if zfile.format == 'zip':   # может писать по частям, без файла.
                zfile.write_gen_zip(ids)
            else:  # 7z пишет сперва файл и не по частям.
                wr = CSVFileWriter()
                wr.write_data(ids)
                zfile.write_file_7z(wr.filepath)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print('Создан архив.', file=f)
