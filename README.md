# Python AI Assistant (Chapter 04)

This project is a simple local AI assistant built with Python and Ollama. It demonstrates how to create a command-line chatbot that can switch between different assistant personas, remember conversation history, and save/load sessions locally.

## Features

- Local model integration via Ollama
- Three assistant modes:
  - `general` for helpful everyday assistance
  - `tutor` for beginner-friendly Python guidance
  - `writer` for professional email and report drafting
- Conversation history support
- Save and restore previous chat sessions
- Status checks for the Ollama server and selected model

## Project Structure

- `main.py` — application entry point and command loop
- `conversation.py` — session and message management
- `ollama_service.py` — API calls to Ollama
- `settings.py` — model, prompt, and storage configuration
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.10+
- Ollama installed and running locally
- A compatible Ollama model pulled to your system

## Setup

1. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   . .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start Ollama:

   ```bash
   ollama serve
   ```

4. Pull the model used by the app:

   ```bash
   ollama pull qwen3.5:9b
   ```

## Run the Assistant

```bash
python main.py
```

## Available Commands

- `/help` — show available commands
- `/mode general` — switch to general assistant mode
- `/mode tutor` — switch to Python tutor mode
- `/mode writer` — switch to business writing mode
- `/history` — view conversation history
- `/clear` — clear the current conversation
- `/save` — save the current session
- `/load` — load the last saved session
- `/status` — check Ollama and model status
- `/exit` — close the app

## Notes

The project stores session data in a local folder under the user profile, typically:

- Windows: `%LOCALAPPDATA%\PythonAIAgentsMadeEasy\Chapter04\session.json`
- macOS/Linux: `~/PythonAIAgentsMadeEasy/Chapter04/session.json`

This example is part of a hands-on chapter focused on building a practical AI assistant with local LLM tooling.
