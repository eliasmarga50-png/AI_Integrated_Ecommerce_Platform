



from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.ai.recommendation import RecommendationEngine


User = get_user_model()


class RecommendationEngineTests(TestCase):

    def setUp(self):
        self.engine = RecommendationEngine()

        self.user = User.objects.create_user(
            username="recommendation_user",
            email="rec@exam.com",
            password="testpass123",
        )

    def test_recommend_returns_list(self):
        results = self.engine.recommend(
            user=self.user,
        )

        self.assertIsInstance(
            results,
            list,
        )

    def test_recommend_without_user(self):
        results = self.engine.recommend()

        self.assertIsInstance(
            results,
            list,
        )

    def test_personalized_without_user(self):
        results = self.engine.personalized(
            None
        )

        self.assertEqual(
            results,
            [],
        )

    def test_recently_viewed_without_user(self):
        results = self.engine.recently_viewed(
            None
        )

        self.assertEqual(
            results,
            [],
        )

    def test_similar_products_returns_list(self):
        results = self.engine.similar_products(
            None,
        )

        self.assertIsInstance(
            results,
            list,
        )

    def test_popular_returns_list(self):
        results = self.engine.popular()

        self.assertIsInstance(
            results,
            list,
        )

    def test_trending_returns_list(self):
        results = self.engine.trending()

        self.assertIsInstance(
            results,
            list,
        )

    def test_new_arrivals_returns_list(self):
        results = self.engine.new_arrivals()

        self.assertIsInstance(
            results,
            list,
        )

    def test_rank_returns_list(self):
        products = []

        results = self.engine.rank(
            products
        )

        self.assertEqual(
            results,
            products,
        )
        


