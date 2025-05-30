
import json
from sdk.codon_sdk import CodonSdk
import asyncio
from handlers.codon_handler import handle_codon

def get_user_secret(user_id):
    return {
        "owner123": "supersecretkey123",
        "owner456": "anothersecret456"
    }.get(user_id)

async def main():
    sdk = CodonSdk(get_user_secret)
    codon = sdk.parse_user_input("open camera", "owner123")
    print("Generated Codon:")
    print(json.dumps(codon, indent=2))

    await handle_codon(codon, get_user_secret)

if __name__ == "__main__":
    asyncio.run(main())
