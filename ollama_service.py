# ollama_service.py

from ollama import Client

from settings import (
    OLLAMA_HOST,
    MODEL_NAME,
    TIMEOUT_SECONDS,
    TEMPERATURE,
    MAX_RESPONSE_TOKENS
)


class OllamaService:

    def __init__(self):

        self.client = Client(
            host=OLLAMA_HOST,
            timeout=TIMEOUT_SECONDS
        )

    def get_installed_models(self):
        """Retrieve names of locally installed models."""

        response = self.client.list()

        return [
            item.model
            for item in response.models
        ]

    def ask(self, system_prompt, history, question):
        """Send a question and conversation to Qwen 3.5."""

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },

            *history,

            {
                "role": "user",
                "content": question
            }
        ]

        response = self.client.chat(
            model=MODEL_NAME,
            messages=messages,
            stream=False,
            think=False,
            options={
                "temperature": TEMPERATURE,
                "num_predict": MAX_RESPONSE_TOKENS
            }
        )

        answer = response.message.content or ""

        if not answer.strip():
            raise ValueError(
                "The model returned an empty answer."
            )

        return answer.strip()
