


"""
Chatbot engine.

Responsibilities:
- Build prompts
- Manage conversation sessions
- Load conversation history
- Generate AI responses
- Save chat messages
- Measure performance
"""

from dataclasses import dataclass
from typing import Optional

from .models import AIChatSession, AIChatMessage
from .prompts import PromptLibrary
from .utils import (
    estimate_tokens,
    start_timer,
    calculate_execution_time,
)


@dataclass
class ChatResponse:
    """
    Standard response returned by the chatbot.
    """

    message: str
    tokens_used: int
    response_time: float


class ChatbotEngine:
    """
    AI Chatbot Engine.

    This class is provider-agnostic, meaning it can work with
    OpenAI, Gemini, Anthropic, local LLMs, or any future provider.
    """

    def __init__(self, provider=None):
        self.provider = provider

    def reply(self, user, message: str, session: Optional[AIChatSession] = None) -> ChatResponse:
        """
        Generate an AI response.
        """

        timer = start_timer()

        session = self._get_or_create_session(
            user=user,
            session=session,
        )

        history = self._conversation_history(session)

        prompt = self._build_prompt(
            history=history,
            message=message,
        )

        response = self._generate_response(prompt)

        self._save_messages(
            session=session,
            user_message=message,
            assistant_message=response,
        )

        elapsed = calculate_execution_time(timer)

        return ChatResponse(
            message=response,
            tokens_used=estimate_tokens(prompt),
            response_time=elapsed,
        )

    def _get_or_create_session(
        self,
        user,
        session: Optional[AIChatSession] = None,
    ) -> AIChatSession:
        """
        Return an existing chat session or create a new one.
        """

        if session is not None:
            return session

        return AIChatSession.objects.create(
            user=user,
            title="New Conversation",
        )

    def _conversation_history(
        self,
        session: AIChatSession,
        limit: int = 20,
    ):
        """
        Load recent conversation history.
        """

        return list(
            session.messages.order_by("-created_at")[:limit]
        )

    def _build_prompt(
        self,
        history,
        message: str,
    ) -> str:
        """
        Build the complete prompt sent to the AI model.
        """

        conversation = []

        for chat in reversed(history):
            conversation.append(
                f"{chat.role.capitalize()}: {chat.message}"
            )

        conversation_text = "\n".join(conversation)

        prompt = (
            f"{PromptLibrary.SYSTEM_PROMPT}\n\n"
            f"{conversation_text}\n\n"
            f"User: {message}\n"
            f"Assistant:"
        )

        return prompt

    def _generate_response(self, prompt: str) -> str:
        """
        Generate an AI response.

        
        (OpenAI, Gemini, etc.) is connected.
        """

        if self.provider is None:
            return (
                "The AI assistant is currently  "
                "unavailable because Gemini is not configured."
            )

        try:
            return self.provider.generate(
                prompt=prompt,
                system_instruction=(
                   PromptLibrary.SYSTEM_PROMPT
                ),
            )

        except Exception:
            return (
                "Sorry, I'm temporarily unavailable. "
                "Please try again later."
            )

    def _save_messages(
        self,
        session: AIChatSession,
        user_message: str,
        assistant_message: str,
    ) -> None:
        """
        Save both the user's message and the AI response.
        """

        AIChatMessage.objects.create(
            session=session,
            role=AIChatMessage.USER,
            message=user_message,
            tokens_used=estimate_tokens(user_message),
        )

        AIChatMessage.objects.create(
            session=session,
            role=AIChatMessage.ASSISTANT,
            message=assistant_message,
            tokens_used=estimate_tokens(assistant_message),
        )

        session.last_activity = AIChatMessage.objects.latest("created_at").created_at
        session.save(update_fields=["last_activity"])


