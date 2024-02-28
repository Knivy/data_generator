from parts import InputDataSource, GeneratorDataSource, FileDataSource

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

    ids = FileDataSource()
    for line in ids.get_data():
        print(line)   
        