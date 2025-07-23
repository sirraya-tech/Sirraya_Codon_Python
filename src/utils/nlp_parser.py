import webbrowser
import urllib.parse
import spacy
from handlers.intents.open_browser import open_browser

nlp = spacy.load("en_core_web_sm")

# -------- Intent Handlers --------


async def search_product(payload):
    product = payload.get("product", "amsaa")
    platform = payload.get("platform", "amazon")
    
    query = urllib.parse.quote_plus(product)

    search_urls = {
        "amazon": f"https://www.amazon.in/s?k={query}",
        "flipkart": f"https://www.flipkart.com/search?q={query}",
        "google": f"https://www.google.com/search?q={query}"
    }

    url = search_urls.get(platform.lower(), search_urls["google"])
    print(f"🔎 Searching for '{product}' on {platform.capitalize()}...")
    webbrowser.open(url)

# -------- Intent Dispatcher --------
INTENT_HANDLERS = {
    "open_browser": open_browser,
    "search_product": search_product,
}

async def handle_intent(intent_name, payload):
    handler = INTENT_HANDLERS.get(intent_name)
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

# -------- Entry Point Example --------
async def run_command_from_text(text):
    parsed = parse_command(text)
    await handle_intent(parsed["intent"], parsed["payload"])

# Example usage
# await run_command_from_text("search for Amsaa saffron on Amazon")
# await run_command_from_text("open https://amsaa.in")
