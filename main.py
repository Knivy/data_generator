from parts import MaleFemaleGenerator

if __name__ == '__main__':
    fk = MaleFemaleGenerator()
    for line in fk.generate(10):
        print(line)
