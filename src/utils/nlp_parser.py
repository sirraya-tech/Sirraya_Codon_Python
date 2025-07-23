import spacy
from handlers.intents import intent_handlers  # ✅ dynamically loaded handlers

nlp = spacy.load("en_core_web_sm")

# -------- Intent Dispatcher --------
async def handle_intent(intent_name, payload):
    handler = intent_handlers.get(intent_name)
    if handler:
        await handler(payload)
    else:
        print(f"❌ No handler for intent: {intent_name}")

# -------- Intent Parser --------
def parse_command(text):
    doc = nlp(text.lower())

    # Match: open browser to some URL
    if "open" in [token.lemma_ for token in doc]:
        for token in doc:
            if token.like_url or token.text.endswith(".com"):
                url = token.text if token.text.startswith("http") else f"https://{token.text}"
                return {
                    "intent": "open_browser",
                    "payload": {"url": url}
                }

        return {
            "intent": "open_browser",
            "payload": {"url": "https://google.com"}
        }

    # Match: search for a product
    if "search" in [token.lemma_ for token in doc] or "find" in [token.lemma_ for token in doc]:
        product = ""
        platform = "google"

        for ent in doc.ents:
            if ent.label_ in ("PRODUCT", "ORG"):
                product = ent.text
        
        for token in doc:
            if token.text.lower() in ("amazon", "flipkart"):
                platform = token.text.lower()

        return {
            "intent": "search_product",
            "payload": {
                "product": product if product else "amsaa",
                "platform": platform
            }
        }

    return {
        "intent": "unknown",
        "payload": {}
    }

# -------- Entry Point --------
async def run_command_from_text(text):
    parsed = parse_command(text)
    await handle_intent(parsed["intent"], parsed["payload"])

# Test example (uncomment in async context)
# await run_command_from_text("search for Amsaa saffron on Amazon")
# await run_command_from_text("open https://amsaa.in")
