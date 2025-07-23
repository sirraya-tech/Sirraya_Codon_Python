from .open_camera import open_camera
from .open_browser import open_browser
from .search_product import search_product

intent_handlers = {
    "open_camera": open_camera,
    "open_browser": open_browser,
    "search_product": search_product,
    # Add other intents here
}
