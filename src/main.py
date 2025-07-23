import asyncio
import json
from sdk.codon_sdk import CodonSdk
from handlers.codon_handler import handle_codon
from utils.nlp_parser import parse_command

def get_user_secret(user_id):
    return {
        "owner123": "supersecretkey123",
    }.get(user_id)

async def main():
    sdk = CodonSdk(get_user_secret)

    command = input("Type your command: ").strip()

    codon_data = parse_command(command)

    if codon_data["intent"] == "unknown":
        print("Sorry, I didn't understand that.")
        return

    codon = sdk.create_codon(
        intent=codon_data["intent"],
        payload=codon_data["payload"],
        meta={},
        user_id="owner123"
    )

    print("\nGenerated Codon:")
    print(json.dumps(codon, indent=2))

    await handle_codon(codon, get_user_secret)

if __name__ == "__main__":
    asyncio.run(main())
