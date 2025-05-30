from utils.crypto_utils import verify_signature
from handlers.intents import intent_handlers

AUTHORIZED_USERS = ["owner123", "owner456"]  # your authorized user list

async def handle_codon(codon, get_user_secret):
    intent = codon.get("intent")
    payload = codon.get("payload", {})
    meta = codon.get("meta", {})
    identity = meta.get("identity", {})
    user_id = identity.get("userId", "unknown")
    signature = identity.get("signature")

    secret = get_user_secret(user_id)
    if not secret:
        print(f"❌ No secret found for user {user_id}. Aborting execution.")
        return

    is_valid = verify_signature(intent, payload, user_id, signature, secret)
    if not is_valid:
        print(f"🚫 Invalid signature for user {user_id}. Request rejected.")
        return

    if user_id not in AUTHORIZED_USERS:
        print(f"🚫 Unauthorized user: {user_id} cannot execute {intent}.")
        return

    handler = intent_handlers.get(intent)
    if handler:
        print(f"✅ Executing handler for intent: {intent}")
        await handler(payload)
    else:
        print(f"❓ Unknown intent: {intent}. Available intents: {list(intent_handlers.keys())}")
