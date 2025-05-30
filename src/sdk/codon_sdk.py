import json
from typing import Callable, Dict, Any

from utils.crypto_utils import generate_telomere_with_user, verify_signature
from core.codon_parser import parse_codon_text
from registry.intent_registry import get_intent_data
from context.context_detector import detect_context


class CodonSdk:
    """
    CodonSdk is responsible for securely encoding and decoding user commands ("codons")
    with identity and context-awareness.
    """

    def __init__(self, get_user_secret: Callable[[str], str]):
        """
        :param get_user_secret: A function that returns a secret key for a given user ID.
        """
        self.get_user_secret = get_user_secret

    def parse_user_input(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """
        Parses raw user input and generates a codon.
        
        :param user_input: The natural language or structured command from the user.
        :param user_id: Unique identifier for the user.
        :return: Parsed codon dictionary.
        """
        intent_data = get_intent_data(user_input)
        intent = intent_data["intent"]
        payload = intent_data.get("payload", {})
        meta = intent_data.get("meta", {})

        return self.create_codon(intent, payload, meta, user_id)

    def create_codon(
        self,
        intent: str,
        payload: Dict[str, Any] = {},
        meta: Dict[str, Any] = {},
        user_id: str = "anonymous"
    ) -> Dict[str, Any]:
        """
        Generates a codon text securely using a telomere and parses it.
        
        :param intent: The user's intended action.
        :param payload: Optional parameters/data for the intent.
        :param meta: Additional metadata.
        :param user_id: User identifier (default is anonymous).
        :return: Parsed codon object.
        :raises Exception: If signature verification fails.
        """
        secret = self.get_user_secret(user_id)
        telomere = generate_telomere_with_user(intent, payload, user_id, secret)
        signature = telomere

        print(f"🔐 Generated telomere for user {user_id}: {telomere}")

        is_verified = verify_signature(intent, payload, user_id, signature, secret)
        if not is_verified:
            raise Exception("❌ Unauthorized: Signature mismatch")

        context = detect_context()

        full_meta = {
            "class": "DeviceCodon",
            "expires_in": 30,
            **meta,
            "identity": {
                "userId": user_id,
                "signature": signature
            },
            "context": context
        }

        codon_text = f"{telomere}::{intent}::{json.dumps(payload)}::{json.dumps(full_meta)}"
        return self.parse_codon(codon_text)

    def parse_codon(self, codon_text: str) -> Dict[str, Any]:
        """
        Parses a raw codon text string into its structured codon object.
        
        :param codon_text: The serialized codon string.
        :return: Parsed codon dictionary.
        """
        return parse_codon_text(codon_text)
