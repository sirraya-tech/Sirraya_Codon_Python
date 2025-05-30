import re
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")  # Make sure to install it: python -m spacy download en_core_web_sm

def parse_nlp_to_codon_input(text: str, user_id: str, sdk):
    """
    Parses user text input using NLP and infers intent and payload for codon creation.

    Args:
        text (str): User's natural language input.
        user_id (str): Identifier of the user.
        sdk (CodonSdk): Instance of Codon SDK with create_codon method.

    Returns:
        dict: Parsed codon object from the SDK.
    """
    intent = None
    payload = {}

    doc = nlp(text.lower())

    # --- Intent: open_browser ---
    if "open browser" in text or "browse" in text:
        intent = "open_browser"
        url_regex = r"(?:https?:\/\/)?(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})(?:\/[^\s]*)?"
        matches = re.findall(url_regex, text)

        if matches:
            payload["url"] = [f"https://{match}" if not match.startswith("http") else match for match in matches]
        else:
            payload["url"] = ["https://default.example.com"]

    # --- Intent: open_terminal ---
    elif "open terminal" in text or "run command" in text:
        intent = "open_terminal"
        command_match = re.search(r"run command (.+)", text, re.IGNORECASE)

        if command_match:
            payload["command"] = [command_match.group(1)]
        else:
            payload["command"] = ["echo Hello, World!"]

    # Extend here with more NLP-based intent recognition...

    if not intent:
        raise ValueError("❌ Could not determine intent from input.")

    return sdk.create_codon(intent, payload, {}, user_id)
