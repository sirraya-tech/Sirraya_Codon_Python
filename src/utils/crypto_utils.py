import hmac
import hashlib
import json

def generate_telomere_with_user(intent: str, payload: dict, user_id: str, secret: str) -> str:
    """
    Generates a secure HMAC-based telomere (signature) for the given user, intent, and payload.
    
    Args:
        intent (str): The intent string.
        payload (dict): The payload object.
        user_id (str): The user identifier.
        secret (str): The secret key associated with the user.

    Returns:
        str: Hexadecimal HMAC-SHA256 digest (the telomere).
    """
    message = intent + json.dumps(payload, separators=(',', ':'), sort_keys=True) + user_id
    return hmac.new(secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()


def verify_signature(intent: str, payload: dict, user_id: str, signature: str, secret: str) -> bool:
    """
    Verifies the provided signature against the expected one.
    
    Args:
        intent (str): The intent string.
        payload (dict): The payload object.
        user_id (str): The user identifier.
        signature (str): The HMAC signature to verify.
        secret (str): The secret key associated with the user.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    expected_signature = generate_telomere_with_user(intent, payload, user_id, secret)
    return hmac.compare_digest(expected_signature, signature)
