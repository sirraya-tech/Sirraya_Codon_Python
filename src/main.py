import asyncio
import json
from sdk.codon_sdk import CodonSdk
from handlers.codon_handler import handle_codon

def get_user_secret(user_id):
    return {
        "owner123": "supersecretkey123",
    }.get(user_id)

async def main():
    sdk = CodonSdk(get_user_secret)
    
    # Create a codon for opening browser with URL payload
    codon = sdk.create_codon(
        intent="open_browser",
        payload={"url": "https://chat.openai.com"},
        meta={},
        user_id="owner123"
    )
    
    print("Generated Codon:")
    print(json.dumps(codon, indent=2))

    await handle_codon(codon, get_user_secret)

if __name__ == "__main__":
    asyncio.run(main())
