import os
import importlib

package_name = __name__  # This will be 'intent' if your folder is named 'intent'

intent_handlers = {}

# Dynamically load all .py files except __init__.py
for filename in os.listdir(os.path.dirname(__file__)):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]  # e.g., "open_browser"

        try:
            # Import the module dynamically
            module = importlib.import_module(f"{package_name}.{module_name}")

            # Assume the function name is the same as the file name
            handler_func = getattr(module, module_name)

            # Register in the handlers dictionary
            intent_handlers[module_name] = handler_func

        except (ImportError, AttributeError) as e:
            print(f"⚠️ Could not load '{module_name}' handler: {e}")
