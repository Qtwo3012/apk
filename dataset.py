class Dataset:

    def __init__(self):
        self.data = []

    def load(self, dataset):
        self.data = dataset

    def load_txt(self, filename):
        self.data = []

        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                angka = line.strip()

                if angka:
                    self.data.append(angka)

    def get(self):
        return self.data

    def total(self):
        return len(self.data)

    def clear(self):
        self.data = []