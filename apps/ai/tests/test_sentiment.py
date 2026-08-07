


from django.test import SimpleTestCase

from apps.ai.sentiment import SentimentEngine


class SentimentEngineTests(SimpleTestCase):

    def setUp(self):
        self.engine = SentimentEngine()

    def test_positive_sentiment(self):
        result = self.engine.predict(
            "This product is excellent and amazing."
        )

        self.assertEqual(
            result["sentiment"],
            SentimentEngine.POSITIVE,
        )

    def test_negative_sentiment(self):
        result = self.engine.predict(
            "This product is terrible and broken."
        )

        self.assertEqual(
            result["sentiment"],
            SentimentEngine.NEGATIVE,
        )

    def test_neutral_sentiment(self):
        result = self.engine.predict(
            "The product is available."
        )

        self.assertEqual(
            result["sentiment"],
            SentimentEngine.NEUTRAL,
        )

    def test_positive_score(self):
        score = self.engine.sentiment_score(
            "excellent amazing"
        )

        self.assertGreater(score, 0)

    def test_negative_score(self):
        score = self.engine.sentiment_score(
            "terrible broken"
        )

        self.assertLess(score, 0)

    def test_neutral_score(self):
        score = self.engine.sentiment_score(
            "product laptop"
        )

        self.assertEqual(score, 0)

    def test_confidence_is_percentage(self):
        result = self.engine.predict(
            "excellent amazing perfect"
        )

        self.assertGreaterEqual(
            result["confidence"],
            0,
        )

        self.assertLessEqual(
            result["confidence"],
            100,
        )

    def test_batch_prediction(self):
        reviews = [
            "Excellent product.",
            "Terrible product.",
            "The product arrived.",
        ]

        results = self.engine.batch_predict(
            reviews
        )

        self.assertEqual(
            len(results),
            3,
        )

    def test_summary(self):
        reviews = [
            "Excellent product.",
            "Terrible product.",
            "The product arrived.",
        ]

        result = self.engine.summarize(
            reviews
        )

        self.assertEqual(
            result["total_reviews"],
            3,
        )

        self.assertIn(
            "positive",
            result,
        )

        self.assertIn(
            "negative",
            result,
        )

        self.assertIn(
            "neutral",
            result,
        )


