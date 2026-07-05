class Validator:

    def validate(self, dataset):

        if len(dataset) == 0:
            raise ValueError("Dataset kosong!")

        for angka in dataset:

            if len(angka) != 4:
                raise ValueError(f"Data tidak valid: {angka}")

            if not angka.isdigit():
                raise ValueError(f"Harus berupa angka: {angka}")

        return True