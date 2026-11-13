# Japanese Tutor 0.1.1
# Start with: python .\japanese_tutur_win_0.1.1.py

# TODO: Add dictonary api to lookup_vocabulary
# TODO: Add interactive quiz with multiple choice questions and answers with a selection system so the user can select the answer and get feedback if it was correct or not
# TODO: Add an UI with interactive and playful frontend using liquid glass and apple type animations
# TODO: Port to Android using flet


from ollama import Client
# installs pykakasi 2.3.0 oder higher, to convert hiragana/katakana/kanji to romanji without user having to install it manually
try:
    import pykakasi
except ImportError:
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "pykakasi>=2.3.0"])
    import pykakasi
    print("pykakasi was installed successfully.")

# installs flet 0.10.0 or higher, to create a frontend for the tutor without user having to install it manually
try:
    import flet as ft
except ImportError:
    import subprocess
    import sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "flet>=0.10.0"])
    import flet as ft
    print("flet was installed successfully.")


# connect to the local Ollama server
client = Client(host="http://127.0.0.1:11434")



# TOOLS

# Simple tool to look up Japanese words in a local vocabulary (needs to be expanded with more words or connected to an external dictionary API)
def lookup_vocabulary(word: str) -> str:
    """Searches for a Japanese word in the local vocabulary and returns its meaning."""
    vocabulary = {
        "neko": "猫 (ねこ, neko) — Cat",
        "mizu": "水 (みず, mizu) — Water",
        "arigatou": "ありがとう (arigatou) — Thank you",
    }

    # Das Wort suchen; bei keinem Treffer eine Nachricht zurückgeben
    return vocabulary.get(word.strip().lower(), f"No entry for {word!r} found.")

# Simple tool to create quizzes
def create_quiz(topic: str, num_questions: int = 5) -> str:
    """Generates a quiz on a given topic with a specified number of questions."""
    # Call the quiz questions API (placeholder)
    return f"Quiz on {topic} with {num_questions} questions (placeholder)."

# tool to convert Japanese text to Romaji using pykakasi library
def convert_to_romanji(text: str) -> str:
    """Converts Japanese text (Hiragana, Katakana, Kanji) to Romaji using pykakasi."""
    kks = pykakasi.kakasi()
    result = kks.convert(text)
    return " ".join([item["hepburn"] for item in result])

# Tell the model about the available tools
tools = [lookup_vocabulary, create_quiz, convert_to_romanji]



# SETTINGS & CONFIG

# Allowed tools for the model to call
available_tools = {
    "lookup_vocabulary": lookup_vocabulary,
    "create_quiz": create_quiz,
    "convert_to_romanji": convert_to_romanji,
}

# System prompt to set the behavior of the model
messages = [
    {
        "role": "system",
        "content": (
            "You are an advanced Japanese tutor. Teach the user Japanese. "
            "The user can ask in any language. Answer in Markdown and add "
            "romaji after Japanese translations. Explain words and sentences "
            "in simple chunks and in the language the user asked in. "
            "Do not use emojis. Use lookup_vocabulary when the user asks "
            "about a word in the local vocabulary."
        ),
    }
]


# CHAT LOOP

# Unlimited chat loop to interact with the model
while True:
    user_message = input("You: ")

    # Quit the chat loop if the user types "exit" or "quit"
    if user_message.lower() in {"exit", "quit"}:
        break

    # Add the user's message to the chat history
    messages.append({"role": "user", "content": user_message})

    # Tool call loop to allow the model to call tools multiple times if needed
    for _ in range(5):
        # The model generates a response based on the chat history and available tools
        response = client.chat(
            model="gemma4:e4b",
            messages=messages,
            tools=tools,
        )

        # The model's response is added to the chat history
        messages.append(response.message)

        # Validating if the model requested any tool calls
        tool_calls = response.message.tool_calls or []
        if not tool_calls:
            # Save the model's answer and print it to the console
            answer = response.message.content or ""
            print("Tutor:", answer)
            break

        # Execute the tool calls requested by the model and return the results back to the model
        for call in tool_calls:
            tool_name = call.function.name
            function = available_tools.get(tool_name)

            # Execute the tool function with the provided arguments and get the result
            if function is None:
                result = f"Unknown Tool: {tool_name}"
            else:
                result = function(**call.function.arguments)

            # Give the result of the tool call back to the model by appending it to the chat history
            messages.append(
                {
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": str(result),
                }
            )
    else:
        # Preventthe model from calling tools indefinitely by limiting the number of tool calls to 5
        print("Tutor: Too many tool calls. Please ask a different question or rephrase your request.")
