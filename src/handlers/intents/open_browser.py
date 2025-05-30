import webbrowser

async def open_browser(payload):
    url = payload.get("url", "https://www.google.com")
    print(f"🌐 Opening browser with URL: {url}")
    webbrowser.open(url)
