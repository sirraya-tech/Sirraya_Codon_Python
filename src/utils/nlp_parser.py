import spacy

nlp = spacy.load("en_core_web_sm")

# Simple hardcoded mapping — later you can train or use intent classification
def parse_command(text):
    doc = nlp(text.lower())

    # Example: Open browser if the verb is "open" and there's a website
    if "open" in [token.lemma_ for token in doc]:
        for token in doc:
            if token.like_url or token.text.endswith(".com"):
                url = token.text if token.text.startswith("http") else f"https://{token.text}"
                return {
                    "intent": "open_browser",
                    "payload": {"url": url}
                }

        # Default if no URL is found but user says "open something"
        return {
            "intent": "open_browser",
            "payload": {"url": "https://google.com"}  # fallback
        }

    return {
        "intent": "unknown",
        "payload": {}
    }
