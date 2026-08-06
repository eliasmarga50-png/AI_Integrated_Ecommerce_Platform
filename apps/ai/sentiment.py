



"""
Sentiment analysis engine.

Responsible for understanding customer opinions from
reviews, comments, and feedback.
"""

from .utils import (
    confidence_percentage,
    normalize_text,
)


class SentimentEngine:
    """
    AI Sentiment Engine.
    """

    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

    POSITIVE_WORDS = {
        "excellent",
        "great",
        "good",
        "love",
        "perfect",
        "awesome",
        "amazing",
        "fast",
        "recommended",
        "quality",
    }

    NEGATIVE_WORDS = {
        "bad",
        "poor",
        "terrible",
        "slow",
        "broken",
        "refund",
        "damage",
        "worst",
        "late",
        "disappointed",
    }

    def predict(self, text):
        """
        Analyze sentiment.

        Returns:

        {
            "sentiment": "...",
            "confidence": ...,
            "score": ...
        }
        """

        text = normalize_text(text)

        score = self.sentiment_score(text)

        sentiment = self.classify(score)

        confidence = self.calculate_confidence(score)

        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "score": score,
        }

    # --------------------------------------------------
    # Sentiment Score
    # --------------------------------------------------

    def sentiment_score(self, text):
        """
        Compute a simple sentiment score.

        Positive word = +1

        Negative word = -1
        """

        score = 0

        for word in text.split():

            if word in self.POSITIVE_WORDS:
                score += 1

            elif word in self.NEGATIVE_WORDS:
                score -= 1

        return score

    # --------------------------------------------------
    # Classification
    # --------------------------------------------------

    def classify(self, score):
        """
        Convert score into sentiment.
        """

        if score > 0:
            return self.POSITIVE

        if score < 0:
            return self.NEGATIVE

        return self.NEUTRAL

    # --------------------------------------------------
    # Confidence
    # --------------------------------------------------

    def calculate_confidence(self, score):
        """
        Estimate confidence.

        Higher absolute scores imply
        stronger confidence.
        """

        confidence = min(abs(score) / 5, 1.0)

        return confidence_percentage(confidence)

    # --------------------------------------------------
    # Batch Prediction
    # --------------------------------------------------

    def batch_predict(self, reviews):
        """
        Analyze multiple reviews.
        """

        return [
            self.predict(review)
            for review in reviews
        ]

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summarize(self, reviews):
        """
        Generate sentiment statistics.
        """

        results = self.batch_predict(reviews)

        positive = sum(
            r["sentiment"] == self.POSITIVE
            for r in results
        )

        negative = sum(
            r["sentiment"] == self.NEGATIVE
            for r in results
        )

        neutral = sum(
            r["sentiment"] == self.NEUTRAL
            for r in results
        )

        return {
            "total_reviews": len(results),
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
        }


