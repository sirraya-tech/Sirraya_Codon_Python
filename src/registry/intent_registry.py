# Define a registry of intents with associated payloads and metadata
intent_registry = {
    "open camera": {
        "intent": "open_camera",
        "payload": {"flash": "on", "quality": "HD"},
        "meta": {"class": "DeviceCodon", "expires_in": 30},
    },
    "turn on flash": {
        "intent": "turn_on_flash",
        "payload": {"flash": "on"},
        "meta": {"class": "DeviceCodon", "expires_in": 30},
    },
    "play music": {
        "intent": "play_music",
        "payload": {"volume": 70},
        "meta": {"class": "DeviceCodon", "expires_in": 30},
    },
    # Add more intents as needed
}

def get_intent_data(user_input: str) -> dict:
    """
    Get intent, payload, and metadata based on user input.

    Args:
        user_input (str): User input string.

    Returns:
        dict: Matching intent data.

    Raises:
        ValueError: If input doesn't match any intent.
    """
    cleaned_input = user_input.lower().strip()
    intent_data = intent_registry.get(cleaned_input)

    if not intent_data:
        raise ValueError(f'❌ Intent not recognized for input: "{user_input}"')

    return intent_data
