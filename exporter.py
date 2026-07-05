class Exporter:

    def export_txt(self, result, filename="result.txt"):

        if result is None:
            return False

        with open(filename, "w") as file:

            file.write("=" * 50 + "\n")
            file.write("PATTERN ANALYZER PRO\n")
            file.write("VERSION 1.0 STABLE\n")
            file.write("=" * 50 + "\n\n")

            file.write(f"Top Pair     : {result['pair']}\n")
            file.write(f"Score        : {result['score']}\n")
            file.write(f"Trend        : {result['trend']}\n")
            file.write(f"Confidence   : {result['confidence']}\n")
            file.write(f"Level        : {result['level']}\n")

            if "decision" in result:
                file.write(f"AI Decision  : {result['decision']}\n")

            if "risk" in result:
                file.write(f"Risk         : {result['risk']}\n")

            if "stability" in result:
                file.write(f"Stability    : {result['stability']}%\n")

            if "mirror" in result and result["mirror"]:

                file.write(
                    f"Mirror Pair  : {result['mirror']['pair']}\n"
                )

                file.write(
                    f"Mirror Hit   : {result['mirror']['repeat']}\n"
                )

            file.write("\n")

            file.write("Reason\n")
            file.write("-" * 50 + "\n")

            for reason in result["reason"]:
                file.write(f"- {reason}\n")

            file.write("\n")
            file.write("=" * 50 + "\n")

        return True