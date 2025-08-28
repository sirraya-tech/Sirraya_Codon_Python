import asyncio
import json
import socket
import threading
import webbrowser

# ---------------------------
# Codon SDK mock (replace with your real sdk.codon_sdk)
# ---------------------------
class Codon:
    def __init__(self, intent, payload, user_id):
        self.intent = intent
        self.payload = payload
        self.user_id = user_id

class CodonSdk:
    def __init__(self, get_user_secret):
        self.get_user_secret = get_user_secret

    def create_codon(self, intent, payload, meta, user_id):
        return Codon(intent, payload, user_id)

# ---------------------------
# Helpers
# ---------------------------
def get_user_secret(user_id):
    return {
        "owner123": "supersecretkey123",
    }.get(user_id)

def parse_command(command: str):
    command = command.lower().strip()
    if "open browser" in command:
        return {"intent": "open_browser", "payload": {}}
    return {"intent": "unknown", "payload": {}}

async def handle_codon(codon, get_user_secret):
    if codon.intent == "open_browser":
        webbrowser.open("http://www.google.com")  # will open browser locally
        return {"status": "success", "message": "Browser opened"}
    return {"status": "error", "message": "Unknown intent"}

# ---------------------------
# Core Logic
# ---------------------------
async def process_codon_command(command, user_id="owner123"):
    sdk = CodonSdk(get_user_secret)
    codon_data = parse_command(command)

    if codon_data["intent"] == "unknown":
        return {"status": "error", "message": "Unknown command"}

    codon = sdk.create_codon(
        intent=codon_data["intent"],
        payload=codon_data["payload"],
        meta={},
        user_id=user_id
    )

    # Execute locally
    result = await handle_codon(codon, get_user_secret)
    return {"status": "success", "codon": codon.__dict__, "result": result}

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"[SERVER] Listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"[SERVER] Connected by {addr}")
                data = conn.recv(1024)
                if not data:
                    continue
                try:
                    request = json.loads(data.decode())
                    command = request.get("command")
                    user_id = request.get("user_id", "owner123")

                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    response = loop.run_until_complete(
                        process_codon_command(command, user_id)
                    )
                    loop.close()

                    conn.sendall(json.dumps(response).encode())
                except Exception as e:
                    conn.sendall(json.dumps({
                        "status": "error",
                        "message": str(e)
                    }).encode())

def send_command(command, peer_ip, peer_port=65432, user_id="owner123"):
    request = {
        "command": command,
        "user_id": user_id
    }
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((peer_ip, peer_port))
        s.sendall(json.dumps(request).encode())
        response = s.recv(1024).decode()
        return json.loads(response)

# ---------------------------
# Main entry
# ---------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="P2P Codon Peer")
    parser.add_argument("--mode", choices=["server", "client"], required=True,
                        help="Run as server (receiver) or client (sender)")
    parser.add_argument("--host", default="0.0.0.0", help="Host/IP to bind (server) or connect (client)")
    parser.add_argument("--port", type=int, default=65432, help="Port number")
    args = parser.parse_args()

    if args.mode == "server":
        # Run server forever
        start_server(args.host, args.port)

    elif args.mode == "client":
        # Interactive client
        while True:
            cmd = input("Enter command (or 'exit' to quit): ").strip()
            if cmd.lower() == "exit":
                break
            response = send_command(cmd, args.host, args.port)
            print("Response:", response)
