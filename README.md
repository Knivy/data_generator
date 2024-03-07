# data_generator
Дополнительное задание второго спринта курса Python разработчик буткемп.  
Создать приложение для генерации и упаковки данных в архив 

# Реализация 
## Генератор данных 
Генерирует данные минимум в 10 столбцах в произвольном или заданном диапазоне строк от 0,5 млн до 2 млн строк. Данные должны быть синтетическими и адекватными(Посмотри на Faker или mimesis) Данные упаковываются в 3 формата exсel или csv, txt 
## Упаковщик 
Создает архив из входящих данных в формат zip и 7z Данные могут вводится как напрямую с клавиатуры, загружаться из файла или генерироваться- выбор остается за пользователем Пользователь может задать предельный размер архива - в таком случае архив разбивается на части и сохраняется в единый архив архивированными частями Формат сохранения может задаваться пользователем 
## Обязательные требования 
Необходимо вести логи 
Приложение должно быть устойчиво к некорректному вводу данных пользоватлем 
Приложение должно быть расширяемым в части добавления нового функционала( новые форматы архивов, новые форматы входящих данных, новые методы ввода данных) 
Приложение должно использовать корректную кодировку 
Приложение должно быть выложено в гит, иметь хорошую документацию и понятный единый интерфейс 
Докстринги - обязательны 
Приложение должно соответвовать pep, ООП и УК РФ 
Дополнителльное требование - в случае с архивом данные не должны создавать файлы, а записываться непосредственно в архив

Faker сильно медленней, чем Mimesis
Для записи по частям надо BitesIO
gen_data > generate_line
interface
MaleFemaleGenerator > MaleFemaleFakerGenerator