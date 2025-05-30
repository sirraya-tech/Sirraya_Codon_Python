import json

def parse_codon_text(codon_text: str) -> dict:
    """
    Parses a codon text string into its structured components: telomere, intent, payload, and meta.

    Args:
        codon_text (str): The codon string separated by '::'.

    Returns:
        dict: Parsed codon with keys 'telomere', 'intent', 'payload', and 'meta'.

    Raises:
        ValueError: If format is invalid or JSON parsing fails.
    """
    parts = [part.strip() for part in codon_text.split("::")]
    
    if len(parts) != 4:
        raise ValueError("❌ Invalid codon format. Expected 4 parts separated by '::'.")

    telomere, intent, payload_raw, meta_raw = parts

    try:
        payload = json.loads(payload_raw)
        meta = json.loads(meta_raw)
    except json.JSONDecodeError as e:
        raise ValueError("❌ Failed to parse payload or meta as JSON.") from e

    return {
        "telomere": telomere,
        "intent": intent,
        "payload": payload,
        "meta": meta
    }
