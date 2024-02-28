from parts import FakerGenerator

if __name__ == '__main__':
    fk = FakerGenerator()
    for line in fk.generate(10):
        print(line)
