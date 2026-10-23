# settings.py

from pathlib import Path
import os

# Ollama configuration
OLLAMA_HOST = "http://localhost:11434"

MODEL_NAME = "qwen3.5:9b"

TIMEOUT_SECONDS = 600

# Model generation settings
TEMPERATURE = 0.3

MAX_RESPONSE_TOKENS = 350

# Maximum number of complete conversation exchanges
MAX_EXCHANGES = 6

# Local folder used for saving sessions
DATA_FOLDER = (
    Path(os.environ.get("LOCALAPPDATA") or Path.home())
    / "PythonAIAgentsMadeEasy"
    / "Chapter04"
)

SESSION_FILE = DATA_FOLDER / "session.json"

# Assistant modes
ASSISTANT_MODES = {

    "general": (
        "You are a helpful AI assistant. "
        "Answer clearly and concisely. "
        "Admit uncertainty, and do not invent facts."
    ),

    "tutor": (
        "You are a patient Python tutor for beginners. "
        "Explain each concept in simple terms and "
        "include a short Python example when helpful."
    ),

    "writer": (
        "You help prepare professional email and "
        "report drafts. "
        "Do not invent names, dates, or commitments. "
        "Never claim that a message has been sent."
    )
}
