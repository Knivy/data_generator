from parts import InputDataSource, GeneratorDataSource, FileDataSource
from parts import CSVFileWriter, XlsxFileWriter

if __name__ == '__main__':
    # fk = MaleFemaleGenerator()
    # for line in fk.generate(10):
    #     print(line)

    # ids = InputDataSource()
    # for line in ids.get_data():
    #     print(line)

    # ids = GeneratorDataSource()
    # for line in ids.get_data():
    #     print(line)

    # ids = FileDataSource()
    # print(type(ids.get_data()))
    # for line in ids.get_data():
    #     print(line)

    ids = GeneratorDataSource().get_data()
    CSVFileWriter().write_data(ids)
