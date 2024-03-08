"""Основной модуль программы-упаковщика.

Тестирование выявило проблемы:
при записи в zip каждая строка пишется отдельным файлом,
несколько раз с одинаковым названием. Эти файлы не читаются.
Запись 7z аварийно останавливается, создавая пустой файл.
Протестировано не всё, что касается упаковки в архив.
Генерация, запись в файлы вроде работает, так что проблемы в модуле Zipper.
Модуль с вызовами других модулей."""

from typing import Generator

from modules.params import ParamsObject

# Собирает все параметры и создает объекты классов.
params_object: ParamsObject = ParamsObject()

# Отдает данные построчно списками строк.
data_source: Generator = params_object.data_source.get_data()
params_object.data_destination.write_data(data_source)

# zfile = Zipper()
# match user_choice:
#     case '1':  # xlsx пишет сперва файл, причем одним куском.
#         wr: Writer = XlsxFileWriter()
#         wr.write_data(ids)
#         zfile.write_xlsx(wr.filepath)
#     case _:  # csv/txt
#         if zfile.format == 'zip':   # может писать по частям, без файла.
#             zfile.write_gen_zip(ids)
#         else:  # 7z пишет сперва файл и не по частям.
#             wr = CSVFileWriter()
#             wr.write_data(ids)
#             zfile.write_file_7z(wr.filepath)
# with open('log.txt', 'a', encoding='utf-8') as f:
#     print('Создан архив.', file=f)
