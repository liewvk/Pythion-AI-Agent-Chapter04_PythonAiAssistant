# main.py

from ollama import ResponseError

from httpx import (
    ConnectError,
    TimeoutException
)

from conversation import Conversation

from ollama_service import OllamaService

from settings import (
    ASSISTANT_MODES,
    MODEL_NAME,
    OLLAMA_HOST,
    SESSION_FILE
)


def show_help():
    """Display available commands."""

    print("\nCommands:")

    print("  /help                 Show commands")
    print("  /mode general         General assistant")
    print("  /mode tutor           Python tutor")
    print("  /mode writer          Business draft assistant")
    print("  /history              View conversation")
    print("  /clear                Clear current conversation")
    print("  /save                 Save current session")
    print("  /load                 Load last saved session")
    print("  /status               Check Ollama and model")
    print("  /exit                 Close program")


def show_history(session):
    """Display previous conversation messages."""

    if not session.history:
        print("No conversation history.")
        return

    for item in session.history:

        print(
            f"\n{item['role'].title()}: "
            f"{item['content']}"
        )


def check_status(service, session):
    """Check Ollama and display application status."""

    models = service.get_installed_models()

    print(
        f"Ollama server: {OLLAMA_HOST} (reachable)"
    )

    print(f"Selected model: {MODEL_NAME}")

    if MODEL_NAME in models:

        print("Model status: installed")

    else:

        print(
            "Model status: NOT FOUND — run ollama pull",
            MODEL_NAME
        )

    print(f"Assistant mode: {session.mode}")

    print(
        f"Stored messages: {len(session.history)}"
    )


def handle_command(line, session, service):
    """Process a command. Return True to exit."""

    parts = line.lower().split()

    command = parts[0]

    if command == "/help":

        show_help()

    elif command == "/history":

        show_history(session)

    elif command == "/clear":

        session.clear()

        print(
            "Current conversation cleared. "
            "Saved file unchanged."
        )

    elif command == "/save":

        path = session.save()

        print("Session saved to:", path)

    elif command == "/load":

        if session.history:

            choice = input(
                "Replace current conversation? (yes/no): "
            ).strip().lower()

            if choice != "yes":

                print("Load canceled.")
                return False

        path = session.load()

        print(f"Session loaded from: {path}")

        print("Restored mode:", session.mode)

    elif command == "/mode":

        if (
            len(parts) != 2
            or parts[1] not in ASSISTANT_MODES
        ):

            print(
                "Use /mode general, "
                "/mode tutor, or /mode writer."
            )

            return False

        new_mode = parts[1]

        if new_mode == session.mode:

            print(
                "Already in",
                new_mode,
                "mode."
            )

            return False

        if session.history:

            choice = input(
                "Mode change clears history. "
                "Continue? (yes/no): "
            ).strip().lower()

            if choice != "yes":

                print("Mode unchanged.")
                return False

        session.change_mode(new_mode)

        print(
            "Assistant mode:",
            session.mode
        )

    elif command == "/status":

        check_status(service, session)

    elif command == "/exit":

        return True

    else:

        print(
            "Unknown command. Type /help."
        )

    return False


def main():

    session = Conversation()

    service = OllamaService()

    print("============================================")
    print("       PYTHON AI ASSISTANT WITH OLLAMA")
    print("       Visual Studio 2026")
    print("============================================")

    print("Model:", MODEL_NAME)
    print("Mode:", session.mode)

    print("Type /help to see commands.")

    while True:

        try:

            line = input("\nYou: ").strip()

        except (EOFError, KeyboardInterrupt):

            print("\nGoodbye!")
            break

        if not line:
            continue

        # Commands begin with a forward slash.
        if line.startswith("/"):

            try:

                if handle_command(
                    line,
                    session,
                    service
                ):

                    print("Goodbye!")
                    break

            except FileNotFoundError:

                print(
                    "No saved session found. "
                    "Use /save first."
                )

            except (OSError, ValueError) as exc:

                print(
                    "Session error:",
                    exc
                )

            except (ConnectError, TimeoutException):

                print(
                    "Cannot reach Ollama. "
                    "Start it and try /status again."
                )

            except ResponseError as exc:

                print(
                    "Ollama error:",
                    exc
                )

            continue

        # Process an ordinary AI question.
        try:

            print("Generating response...")

            answer = service.ask(
                ASSISTANT_MODES[session.mode],
                session.messages(),
                line
            )

            print(
                "\nAssistant:",
                answer
            )

            # Store the successful exchange.
            session.record(
                line,
                answer
            )

        except ResponseError as exc:

            print(
                "Ollama error:",
                exc
            )

            print(
                "Verify the selected model "
                "with 'ollama list'."
            )

        except ConnectError:

            print(
                "Cannot reach Ollama at",
                OLLAMA_HOST
            )

            print(
                "Launch Ollama or use "
                "'ollama serve' if needed."
            )

        except TimeoutException:

            print(
                "The local model request timed out."
            )

        except ValueError as exc:

            print(
                "Response error:",
                exc
            )


if __name__ == "__main__":
    main()# main.py

from ollama import ResponseError

from httpx import (
    ConnectError,
    TimeoutException
)

from conversation import Conversation

from ollama_service import OllamaService

from settings import (
    ASSISTANT_MODES,
    MODEL_NAME,
    OLLAMA_HOST,
    SESSION_FILE
)


def show_help():
    """Display available commands."""

    print("\nCommands:")

    print("  /help                 Show commands")
    print("  /mode general         General assistant")
    print("  /mode tutor           Python tutor")
    print("  /mode writer          Business draft assistant")
    print("  /history              View conversation")
    print("  /clear                Clear current conversation")
    print("  /save                 Save current session")
    print("  /load                 Load last saved session")
    print("  /status               Check Ollama and model")
    print("  /exit                 Close program")


def show_history(session):
    """Display previous conversation messages."""

    if not session.history:
        print("No conversation history.")
        return

    for item in session.history:

        print(
            f"\n{item['role'].title()}: "
            f"{item['content']}"
        )


def check_status(service, session):
    """Check Ollama and display application status."""

    models = service.get_installed_models()

    print(
        f"Ollama server: {OLLAMA_HOST} (reachable)"
    )

    print(f"Selected model: {MODEL_NAME}")

    if MODEL_NAME in models:

        print("Model status: installed")

    else:

        print(
            "Model status: NOT FOUND — run ollama pull",
            MODEL_NAME
        )

    print(f"Assistant mode: {session.mode}")

    print(
        f"Stored messages: {len(session.history)}"
    )


def handle_command(line, session, service):
    """Process a command. Return True to exit."""

    parts = line.lower().split()

    command = parts[0]

    if command == "/help":

        show_help()

    elif command == "/history":

        show_history(session)

    elif command == "/clear":

        session.clear()

        print(
            "Current conversation cleared. "
            "Saved file unchanged."
        )

    elif command == "/save":

        path = session.save()

        print("Session saved to:", path)

    elif command == "/load":

        if session.history:

            choice = input(
                "Replace current conversation? (yes/no): "
            ).strip().lower()

            if choice != "yes":

                print("Load canceled.")
                return False

        path = session.load()

        print(f"Session loaded from: {path}")

        print("Restored mode:", session.mode)

    elif command == "/mode":

        if (
            len(parts) != 2
            or parts[1] not in ASSISTANT_MODES
        ):

            print(
                "Use /mode general, "
                "/mode tutor, or /mode writer."
            )

            return False

        new_mode = parts[1]

        if new_mode == session.mode:

            print(
                "Already in",
                new_mode,
                "mode."
            )

            return False

        if session.history:

            choice = input(
                "Mode change clears history. "
                "Continue? (yes/no): "
            ).strip().lower()

            if choice != "yes":

                print("Mode unchanged.")
                return False

        session.change_mode(new_mode)

        print(
            "Assistant mode:",
            session.mode
        )

    elif command == "/status":

        check_status(service, session)

    elif command == "/exit":

        return True

    else:

        print(
            "Unknown command. Type /help."
        )

    return False


def main():

    session = Conversation()

    service = OllamaService()

    print("============================================")
    print("       PYTHON AI ASSISTANT WITH OLLAMA")
    print("       Visual Studio 2026")
    print("============================================")

    print("Model:", MODEL_NAME)
    print("Mode:", session.mode)

    print("Type /help to see commands.")

    while True:

        try:

            line = input("\nYou: ").strip()

        except (EOFError, KeyboardInterrupt):

            print("\nGoodbye!")
            break

        if not line:
            continue

        # Commands begin with a forward slash.
        if line.startswith("/"):

            try:

                if handle_command(
                    line,
                    session,
                    service
                ):

                    print("Goodbye!")
                    break

            except FileNotFoundError:

                print(
                    "No saved session found. "
                    "Use /save first."
                )

            except (OSError, ValueError) as exc:

                print(
                    "Session error:",
                    exc
                )

            except (ConnectError, TimeoutException):

                print(
                    "Cannot reach Ollama. "
                    "Start it and try /status again."
                )

            except ResponseError as exc:

                print(
                    "Ollama error:",
                    exc
                )

            continue

        # Process an ordinary AI question.
        try:

            print("Generating response...")

            answer = service.ask(
                ASSISTANT_MODES[session.mode],
                session.messages(),
                line
            )

            print(
                "\nAssistant:",
                answer
            )

            # Store the successful exchange.
            session.record(
                line,
                answer
            )

        except ResponseError as exc:

            print(
                "Ollama error:",
                exc
            )

            print(
                "Verify the selected model "
                "with 'ollama list'."
            )

        except ConnectError:

            print(
                "Cannot reach Ollama at",
                OLLAMA_HOST
            )

            print(
                "Launch Ollama or use "
                "'ollama serve' if needed."
            )

        except TimeoutException:

            print(
                "The local model request timed out."
            )

        except ValueError as exc:

            print(
                "Response error:",
                exc
            )


if __name__ == "__main__":
    main()
