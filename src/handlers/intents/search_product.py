import webbrowser
import urllib.parse

async def search_product(payload):
    product = payload.get("product", "saffron")
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