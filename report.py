class Report:

    def show(self, result):

        print("=" * 50)
        print("PATTERN ANALYZER REPORT")
        print("=" * 50)

        if result is None:
            print("Tidak ada rekomendasi.")
            print("=" * 50)
            return

        print(f"Top Pair    : {result['pair']}")
        print(f"Score       : {result['score']}")
        print(f"Trend       : {result['trend']}")
        print(f"Confidence  : {result['confidence']}")

        print("\nReason :")

        for reason in result["reason"]:
            print(f"✔ {reason}")

        print("=" * 50)