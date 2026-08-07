



from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.ai.chatbot import ChatbotEngine, ChatResponse
from apps.ai.models import (
    AIChatMessage,
    AIChatSession,
)


User = get_user_model()


class ChatbotEngineTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="chatbot_user",
            email="chat@exam.com",
            password="testpass123",
        )

        self.engine = ChatbotEngine()

    def test_reply_creates_session(self):
        result = self.engine.reply(
            user=self.user,
            message="Hello",
        )

        self.assertIsInstance(
            result,
            ChatResponse,
        )

        self.assertTrue(
            AIChatSession.objects.filter(
                user=self.user
            ).exists()
        )

    def test_reply_saves_user_message(self):
        self.engine.reply(
            user=self.user,
            message="Show me laptops.",
        )

        self.assertTrue(
            AIChatMessage.objects.filter(
                session__user=self.user,
                role=AIChatMessage.USER,
                message="Show me laptops.",
            ).exists()
        )

    def test_reply_saves_assistant_message(self):
        self.engine.reply(
            user=self.user,
            message="Hello",
        )

        self.assertTrue(
            AIChatMessage.objects.filter(
                session__user=self.user,
                role=AIChatMessage.ASSISTANT,
            ).exists()
        )

    def test_reply_returns_message(self):
        result = self.engine.reply(
            user=self.user,
            message="Hello",
        )

        self.assertIsInstance(
            result.message,
            str,
        )

    def test_reply_with_existing_session(self):
        session = AIChatSession.objects.create(
            user=self.user,
            title="Existing Chat",
        )

        self.engine.reply(
            user=self.user,
            message="Continue conversation.",
            session=session,
        )

        self.assertEqual(
            AIChatSession.objects.filter(
                user=self.user
            ).count(),
            1,
        )

    def test_conversation_history(self):
        session = AIChatSession.objects.create(
            user=self.user,
            title="History Test",
        )

        AIChatMessage.objects.create(
            session=session,
            role=AIChatMessage.USER,
            message="Hello",
        )

        AIChatMessage.objects.create(
            session=session,
            role=AIChatMessage.ASSISTANT,
            message="Hi!",
        )

        history = self.engine._conversation_history(
            session
        )

        self.assertEqual(
            len(history),
            2,
        )

    def test_provider_is_called(self):
        provider = Mock()

        provider.generate.return_value = (
            "AI response"
        )

        engine = ChatbotEngine(
            provider=provider
        )

        result = engine.reply(
            user=self.user,
            message="Hello",
        )

        provider.generate.assert_called_once()

        self.assertEqual(
            result.message,
            "AI response",
        )

    def test_provider_failure_is_handled(self):
        provider = Mock()

        provider.generate.side_effect = Exception(
            "Provider unavailable"
        )

        engine = ChatbotEngine(
            provider=provider
        )

        result = engine.reply(
            user=self.user,
            message="Hello",
        )

        self.assertIsInstance(
            result.message,
            str,
        )


