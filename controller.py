from dataset import Dataset
from database import Database
from validator import Validator
from analyzer import Analyzer
from prediction import Prediction
from report import Report
from exporter import Exporter


class Controller:

    def __init__(self):

        self.db = Database()
        self.loader = Dataset()
        self.validator = Validator()
        self.report = Report()
        self.exporter = Exporter()

    # ==========================================
    # Import Dataset
    # ==========================================

    def import_txt(self):

        self.loader.load_txt("sample/history.txt")

        self.db.import_dataset(
            self.loader.get()
        )

        print("=" * 50)
        print("IMPORT DATASET")
        print("=" * 50)

        print("Import Success")
        print("Total Record :", self.db.total())

    # ==========================================
    # Show Database
    # ==========================================

    def show_database(self):

        print("=" * 50)
        print("DATABASE")
        print("=" * 50)

        data = self.db.get_all()

        if not data:
            print("Database kosong.")
            return

        for i, nomor in enumerate(data, start=1):
            print(f"{i}. {nomor}")

        print("-" * 50)
        print("Total :", len(data))
            # ==========================================
    # Analyze
    # ==========================================

    def analyze(self):

        print("=" * 50)
        print("ANALYZE")
        print("=" * 50)

        data = self.db.get_all()

        if not data:
            print("Database kosong.")
            return

        analyzer = Analyzer(data)
        prediction = Prediction(analyzer)

        hasil = prediction.best_prediction()

        if hasil is None:
            print("Belum ada rekomendasi.")
            return

        print("Top Pair    :", hasil["pair"])
        print("Score       :", hasil["score"])
        print("Trend       :", hasil["trend"])
        print("Confidence  :", hasil["confidence"])
        print("Level       :", hasil["level"])

        print()
        print("AI Decision :", prediction.decision())
        print("Risk        :", prediction.risk())
        print(f"Stability   : {prediction.stability()}%")

        mirror = prediction.mirror_support()

        if mirror:
            print("Mirror Pair :", mirror["pair"])
            print("Mirror Hit  :", mirror["repeat"])

        print()
        print("Top Prediction")

        for item in prediction.top_prediction(5):
            print(
                f'{item["rank"]}. '
                f'{item["pair"]} '
                f'({item["score"]})'
            )

        print()
        print("Prediction 3D")

        for item in prediction.prediction_3d(3):
            print(item)

        print()
        print("Prediction 4D")

        for item in prediction.prediction_4d(2):
            print(item)

        print()
        print("BBFS")
        print(" ".join(prediction.bbfs()))

        print()
        print("Hot Digit")

        for digit, freq in analyzer.hot_digit():
            print(f"{digit} ({freq})")

        print()
        print("Cold Digit")

        for digit, freq in analyzer.cold_digit():
            print(f"{digit} ({freq})")

        print()
        print("Reason :")

        for item in hasil["reason"]:
            print("-", item)

        print()
        print("=" * 50)
        print("AI SUMMARY")
        print("=" * 50)

        ai = prediction.ai_summary()

        print("Decision  :", ai["decision"])
        print("Risk      :", ai["risk"])
        print(f"Stability : {ai['stability']}%")

        if ai["mirror"]:
            print("Mirror    :", ai["mirror"]["pair"])
            print("Hit       :", ai["mirror"]["repeat"])

        print("=" * 50)
            # ==========================================
    # Export
    # ==========================================

    def export(self):

        print("=" * 50)
        print("EXPORT REPORT")
        print("=" * 50)

        data = self.db.get_all()

        if not data:
            print("Database kosong.")
            return

        analyzer = Analyzer(data)
        prediction = Prediction(analyzer)

        hasil = prediction.best_prediction()

        if hasil is None:
            print("Belum ada data.")
            return

        hasil["decision"] = prediction.decision()
        hasil["risk"] = prediction.risk()
        hasil["stability"] = prediction.stability()
        hasil["mirror"] = prediction.mirror_support()

        sukses = self.exporter.export_txt(hasil)

        if sukses:
            print("Export Success")
            print("File : result.txt")
        else:
            print("Export Failed")