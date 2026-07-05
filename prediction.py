"""
=========================================
Pattern Analyzer Pro
Prediction Engine
Version : 4.0
Build   : Build16
=========================================
"""

class Prediction:

    def __init__(self, analyzer):

        self.analyzer = analyzer

    # =====================================
    # Candidate Engine
    # =====================================

    def candidate_digit(self, limit=3):

        hasil = self.analyzer.hot_digit(limit)

        return [digit for digit, _ in hasil]

    def candidate_pair(self, limit=10):

        return self.analyzer.hot_pair(limit)

    # =====================================
    # Utility Engine
    # =====================================

    def hot_digit(self):

        return self.candidate_digit()

    def hot_pair(self):

        return self.candidate_pair()

    def total_candidate(self):

        return len(self.candidate_pair())

    # =====================================
    # Score Engine
    # =====================================

    def score_pair(self, pair, frequency):

        score = 0

        # Frequency
        score += frequency * 10

        hot = self.candidate_digit()

        # Hot digit
        if pair[0] in hot:
            score += 20

        if pair[1] in hot:
            score += 20

        # Trend
        trend = self.analyzer.trend_pair(pair)

        if trend == "HOT":
            score += 30

        elif trend == "WARM":
            score += 15

        # Repeat
        repeat = self.analyzer.repeat_pair(pair)

        score += repeat * 2

        # Gap
        gap = self.analyzer.gap_pair(pair)

        if gap:

            rata = sum(gap) / len(gap)

            if rata <= 3:
                score += 10

            elif rata <= 6:
                score += 5

        # Cycle
        cycle = self.analyzer.cycle_pair(pair)

        if cycle is not None:
            score += 5

        return score
            # =====================================
    # Ranking Engine
    # =====================================

    def ranking(self):

        hasil = []

        for pair, frequency in self.candidate_pair():

            score = self.score_pair(pair, frequency)

            hasil.append({

                "pair": pair,
                "frequency": frequency,
                "trend": self.analyzer.trend_pair(pair),
                "repeat": self.analyzer.repeat_pair(pair),
                "gap": self.analyzer.gap_pair(pair),
                "cycle": self.analyzer.cycle_pair(pair),
                "score": score

            })

        hasil.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return hasil

    # =====================================
    # Probability Engine
    # =====================================

    def probability(self, score):

        ranking = self.ranking()

        if not ranking:
            return 0

        highest = ranking[0]["score"]

        if highest <= 0:
            return 0

        persen = (score / highest) * 100

        if persen > 99:
            persen = 99

        return round(persen, 2)

    # =====================================
    # Confidence Engine
    # =====================================

    def confidence_score(self):

        ranking = self.ranking()

        if not ranking:
            return 0

        probability = self.probability(
            ranking[0]["score"]
        )

        if probability >= 95:
            return 95

        elif probability >= 90:
            return 90

        elif probability >= 80:
            return 85

        elif probability >= 70:
            return 80

        return 70

    def confidence_level(self):

        confidence = self.confidence_score()

        if confidence >= 95:
            return "VERY HIGH"

        elif confidence >= 90:
            return "HIGH"

        elif confidence >= 80:
            return "MEDIUM"

        return "LOW"
            # =====================================
    # Recommendation Engine
    # =====================================

    def recommendation(self):

        ranking = self.ranking()

        if not ranking:
            return None

        terbaik = ranking[0]

        probability = self.probability(
            terbaik["score"]
        )

        if probability >= 95:
            decision = "PLAY"

        elif probability >= 90:
            decision = "WATCHLIST"

        elif probability >= 80:
            decision = "MONITOR"

        else:
            decision = "SKIP"

        return {

            "pair": terbaik["pair"],
            "score": terbaik["score"],
            "probability": probability,
            "confidence": self.confidence_score(),
            "level": self.confidence_level(),
            "decision": decision

        }

    # =====================================
    # Prediction Engine
    # =====================================

    def prediction_2d(self, limit=5):

        return [
            item["pair"]
            for item in self.ranking()[:limit]
        ]

    def prediction_3d(self, limit=5):

        hasil = []

        hot = self.candidate_digit()

        if len(hot) < 3:
            return hasil

        for pair in self.prediction_2d(limit):

            hasil.append(pair + hot[0])
            hasil.append(pair + hot[1])
            hasil.append(pair + hot[2])

        return hasil

    def prediction_4d(self, limit=5):

        hasil = []

        hot = self.candidate_digit()

        if len(hot) < 2:
            return hasil

        for angka in self.prediction_3d(limit):

            hasil.append(angka + hot[0])
            hasil.append(angka + hot[1])

        return hasil

    # =====================================
    # BBFS Engine
    # =====================================

    def bbfs(self):

        hasil = []

        for digit, _ in self.analyzer.hot_digit(6):

            hasil.append(digit)

        return hasil
        
            # =====================================
    # Top Prediction
    # =====================================

    def top_prediction(self, limit=5):

        hasil = []

        for i, item in enumerate(self.ranking()[:limit], start=1):

            hasil.append({

                "rank": i,
                "pair": item["pair"],
                "score": item["score"],
                "trend": item["trend"]

            })

        return hasil
        
            # =====================================
    # Mirror Engine
    # =====================================

    def mirror_support(self):

        ranking = self.ranking()

        if not ranking:
            return None

        pair = ranking[0]["pair"]

        if not hasattr(self.analyzer, "mirror_pair"):
            return None

        mirror = self.analyzer.mirror_pair(pair)

        return {
            "pair": mirror,
            "repeat": self.analyzer.repeat_pair(mirror)
        }

    # =====================================
    # AI Summary
    # =====================================

    def ai_summary(self):

        rekom = self.recommendation()

        mirror = self.mirror_support()

        return {

            "decision": rekom["decision"] if rekom else "-",

            "risk": "LOW" if self.confidence_score() >= 90
                    else "MEDIUM" if self.confidence_score() >= 80
                    else "HIGH",

            "stability": self.confidence_score(),

            "mirror": mirror

        }

    # =====================================
    # Best Prediction
    # =====================================

    def best_prediction(self):

        ranking = self.ranking()

        if not ranking:
            return None

        terbaik = ranking[0]

        return {

            "pair": terbaik["pair"],
            "score": terbaik["score"],
            "probability": self.probability(
                terbaik["score"]
            ),
            "trend": terbaik["trend"],
            "confidence": self.confidence_score(),
            "level": self.confidence_level(),
            "reason": self.reason()

        }

        # =====================================
    # Reason Engine
    # =====================================

    def reason(self):

        ranking = self.ranking()

        if not ranking:
            return []

        terbaik = ranking[0]

        alasan = []

        if terbaik["frequency"] >= 2:
            alasan.append("High Frequency")

        if terbaik["trend"] == "HOT":
            alasan.append("Hot Trend")

        if terbaik["repeat"] >= 2:
            alasan.append("Repeat Pattern")

        if terbaik["cycle"] is not None:
            alasan.append("Cycle Detected")

        if self.mirror_support():
            alasan.append("Mirror Supported")

        alasan.append("Hot Digit")

        return alasan

    # ==========================================
    # Compatibility Engine
    # ==========================================

    def decision(self):

        ai = self.ai_summary()
        return ai["decision"]

    def risk(self):

        ai = self.ai_summary()
        return ai["risk"]

    def stability(self):

        ai = self.ai_summary()
        return ai["stability"]