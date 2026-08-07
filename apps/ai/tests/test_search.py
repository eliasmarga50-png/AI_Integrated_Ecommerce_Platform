


from django.test import SimpleTestCase

from apps.ai.search import SearchEngine


class SearchEngineTests(SimpleTestCase):

    def setUp(self):
        self.engine = SearchEngine()

    def test_search_returns_list(self):
        results = self.engine.search(
            "gaming laptop"
        )

        self.assertIsInstance(
            results,
            list,
        )

    def test_empty_search_returns_list(self):
        results = self.engine.search("")

        self.assertIsInstance(
            results,
            list,
        )

    def test_keyword_search_returns_list(self):
        results = self.engine.keyword_search(
            "laptop"
        )

        self.assertIsInstance(
            results,
            list,
        )

    def test_semantic_search_returns_list(self):
        results = self.engine.semantic_search(
            "gaming computer"
        )

        self.assertIsInstance(
            results,
            list,
        )

    def test_category_search_returns_list(self):
        results = self.engine.category_search(
            "electronics"
        )

        self.assertIsInstance(
            results,
            list,
        )

    def test_spell_correction_preserves_query(self):
        query = "gaming laptop"

        corrected = self.engine.correct_spelling(
            query
        )

        self.assertEqual(
            corrected,
            query,
        )

    def test_intent_detection(self):
        intent = self.engine.detect_intent(
            "gaming laptop"
        )

        self.assertEqual(
            intent,
            "product",
        )

    def test_result_limit(self):
        results = self.engine.search(
            "laptop",
            limit=5,
        )

        self.assertLessEqual(
            len(results),
            5,
        )


