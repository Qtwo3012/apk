from collections import Counter


class Analyzer:

    def __init__(self, dataset):
        self.dataset = dataset

    # ==========================================
    # Frequency Engine
    # ==========================================

    def frequency(self, digit):

        hasil = Counter()

        for angka in self.dataset:
            hasil[angka[-digit:]] += 1

        return hasil

    def frequency_4d(self):
        return self.frequency(4)

    def frequency_3d(self):
        return self.frequency(3)

    def frequency_2d(self):
        return self.frequency(2)

    # ==========================================
    # Digit Engine
    # ==========================================

    def digit_frequency(self):

        hasil = Counter()

        for angka in self.dataset:

            for digit in angka:
                hasil[digit] += 1

        return hasil

    def hot_digit(self, limit=3):

        return sorted(
            self.digit_frequency().items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]

    def cold_digit(self, limit=3):

        return sorted(
            self.digit_frequency().items(),
            key=lambda x: x[1]
        )[:limit]

    # ==========================================
    # Pair Engine
    # ==========================================

    def pair_frequency(self):

        hasil = Counter()

        for angka in self.dataset:

            for i in range(len(angka) - 1):

                pair = angka[i:i + 2]

                hasil[pair] += 1

        return hasil

    def hot_pair(self, limit=5):

        return sorted(
            self.pair_frequency().items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]

    def cold_pair(self, limit=5):

        return sorted(
            self.pair_frequency().items(),
            key=lambda x: x[1]
        )[:limit]

    # ==========================================
    # History Engine
    # ==========================================

    def history_pair(self, pair):

        hasil = []

        for index, angka in enumerate(self.dataset, start=1):

            if pair in angka:
                hasil.append(index)

        return hasil

    # ==========================================
    # Gap Engine
    # ==========================================

    def gap_pair(self, pair):

        history = self.history_pair(pair)

        if len(history) < 2:
            return []

        gap = []

        for i in range(1, len(history)):
            gap.append(history[i] - history[i - 1])

        return gap

    # ==========================================
    # Repeat Engine
    # ==========================================

    def repeat_pair(self, pair):

        return len(self.history_pair(pair))

    # ==========================================
    # Mirror Engine
    # ==========================================

    def mirror_pair(self, pair):

        return pair[::-1]
            # ==========================================
    # Cycle Engine
    # ==========================================

    def cycle_pair(self, pair):

        gap = self.gap_pair(pair)

        if not gap:
            return None

        return max(set(gap), key=gap.count)

    # ==========================================
    # Trend Engine
    # ==========================================

    def trend_pair(self, pair):

        total = self.repeat_pair(pair)

        if total >= 3:
            return "HOT"

        elif total == 2:
            return "WARM"

        return "COLD"

    # ==========================================
    # Summary
    # ==========================================

    def summary(self):

        freq2d = self.frequency_2d()

        hot = self.hot_pair(1)
        cold = self.cold_pair(1)

        return {

            "total_data": len(self.dataset),

            "unique_4d": len(self.frequency_4d()),

            "unique_3d": len(self.frequency_3d()),

            "unique_2d": len(freq2d),

            "most_pair": hot[0] if hot else None,

            "least_pair": cold[0] if cold else None

        }

    # ==========================================
    # Statistics
    # ==========================================

    def statistics(self):

        return {

            "total_data": len(self.dataset),

            "frequency_2d": len(self.frequency_2d()),

            "pair_total": len(self.pair_frequency()),

            "hot_digit": self.hot_digit(),

            "cold_digit": self.cold_digit(),

            "hot_pair": self.hot_pair(),

            "cold_pair": self.cold_pair()

        }