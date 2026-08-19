



import json

from django.conf import settings


class GeminiProvider:
    """
    Google Gemini provider using the official
    Google GenAI Python SDK.
    """

    def __init__(self, api_key=None):
        from google import genai
        from google.genai import types

        self.types = types

        self.api_key = (
            api_key
            or getattr(
                settings,
                "GEMINI_API_KEY",
                "",
            )
            or getattr(
                settings,
                "GOOGLE_API_KEY",
                "",
            )
        ).strip()

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=self.api_key
        )

        self.model = getattr(
            settings,
            "GEMINI_MODEL",
            "gemini-2.5-flash-lite",
        )

    @classmethod
    def from_settings(cls):
        key = (
            getattr(
                settings,
                "GEMINI_API_KEY",
                "",
            )
            or getattr(
                settings,
                "GOOGLE_API_KEY",
                "",
            )
        ).strip()

        if not key:
            return None

        return cls(key)

    def generate(
        self,
        prompt,
        system_instruction=None,
        temperature=0.4,
        max_output_tokens=512,
    ):
        config = self.types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )

        response = (
            self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )
        )

        text = (
            response.text or ""
        ).strip()

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text

    def generate_json(
        self,
        prompt,
        system_instruction=None,
        max_output_tokens=512,
    ):
        config = self.types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            temperature=0.2,
            max_output_tokens=max_output_tokens,
        )

        response = (
            self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )
        )

        text = (
            response.text or ""
        ).strip()

        if not text:
            raise RuntimeError(
                "Gemini returned empty JSON."
            )

        return json.loads(text)


