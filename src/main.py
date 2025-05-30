
import json
from sdk.codon_sdk import CodonSdk


def get_user_secret(user_id):
    # Mock secret store
    secrets = {
        "owner123": "supersecretkey123",
        "owner456": "anothersecret456"
    }
    return secrets.get(user_id)

def main():
    sdk = CodonSdk(get_user_secret)
    codon = sdk.parse_user_input("open camera", "owner123")
    print("Generated Codon:")
    print(json.dumps(codon, indent=2))

if __name__ == "__main__":
    main()
