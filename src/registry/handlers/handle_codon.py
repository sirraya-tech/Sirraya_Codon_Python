from typing import Callable, Dict, Any
from utils.crypto_utils import verify_signature
from intents import intent_handlers  # Make sure to define intent handlers in this module

AUTHORIZED_USERS = ["owner123", "owner456"]

async def handle_codon(codon: Dict[str, Any], get_user_secret: Callable[[str], str]) -> None:
    """
    Handle a codon by verifying the signature, authorizing the user, and executing the intent handler.

    Args:
        codon (dict): The codon dictionary containing intent, payload, and meta.
        get_user_secret (callable): Function that returns a secret key for a given user ID.
    """
    intent = codon.get("intent")
    payload = codon.get("payload", {})
    meta = codon.get("meta", {})
    identity = meta.get("identity", {})

    user_id = identity.get("userId", "unknown")
    signature = identity.get("signature")

    secret = get_user_secret(user_id)
    if not secret:
        print(f"❌ No secret found for user {user_id}.")
        return

    is_valid = verify_signature(intent, payload, user_id, signature, secret)
    if not is_valid:
        print(f"🚫 Invalid signature for user {user_id}. Request rejected.")
        return

    if user_id not in AUTHORIZED_USERS:
        print(f"🚫 Unauthorized: User {user_id} is not allowed to execute this intent.")
        return

    handler = intent_handlers.get(intent)
    if handler:
        print(f"✅ Executing intent handler for: {intent}")
        await handler(payload)
    else:
        print(f"❓ Unknown or unsupported intent: {intent}")
        print(f"Available intents: {list(intent_handlers.keys())}")
