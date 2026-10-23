# conversation.py

import json

from settings import (
    ASSISTANT_MODES,
    MAX_EXCHANGES,
    SESSION_FILE
)


class Conversation:

    def __init__(self):

        self.mode = "general"

        self.history = []

    def messages(self):
        """Return a copy of the conversation messages."""

        return [
            item.copy()
            for item in self.history
        ]

    def record(self, question, answer):
        """Save a successful question-and-answer exchange."""

        if not question.strip() or not answer.strip():
            raise ValueError(
                "Question and answer must not be empty."
            )

        self.history.extend([
            {
                "role": "user",
                "content": question
            },
            {
                "role": "assistant",
                "content": answer
            }
        ])

        # Keep only the most recent exchanges.
        self.history = self.history[
            -2 * MAX_EXCHANGES:
        ]

    def clear(self):
        """Clear the current conversation."""

        self.history.clear()

    def change_mode(self, mode):
        """Change assistant mode and clear old context."""

        if mode not in ASSISTANT_MODES:
            raise ValueError(
                "Unknown assistant mode."
            )

        self.mode = mode

        self.clear()

    def save(self):
        """Save the conversation to a JSON file."""

        SESSION_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        data = {
            "version": 1,
            "mode": self.mode,
            "history": self.history
        }

        temporary = SESSION_FILE.with_suffix(".tmp")

        temporary.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        temporary.replace(SESSION_FILE)

        return SESSION_FILE

    def load(self):
        """Load and validate a saved conversation."""

        if SESSION_FILE.stat().st_size > 1_000_000:
            raise ValueError(
                "The session file is too large."
            )

        data = json.loads(
            SESSION_FILE.read_text(
                encoding="utf-8"
            )
        )

        if (
            not isinstance(data, dict)
            or data.get("version") != 1
        ):
            raise ValueError(
                "Unsupported session file format."
            )

        mode = data.get("mode")
        history = data.get("history")

        if (
            mode not in ASSISTANT_MODES
            or not isinstance(history, list)
        ):
            raise ValueError(
                "Invalid session data."
            )

        if len(history) % 2 != 0:
            raise ValueError(
                "Conversation must contain complete exchanges."
            )

        clean = []

        for index, item in enumerate(history):

            expected_role = (
                "user"
                if index % 2 == 0
                else "assistant"
            )

            if (
                not isinstance(item, dict)
                or item.get("role") != expected_role
                or not isinstance(item.get("content"), str)
                or not item["content"].strip()
            ):
                raise ValueError(
                    "Invalid conversation message."
                )

            clean.append({
                "role": expected_role,
                "content": item["content"]
            })

        self.mode = mode

        self.history = clean[
            -2 * MAX_EXCHANGES:
        ]

        return SESSION_FILE
