# p2p_receiver.py
import asyncio
import json
import socket
from sdk.codon_sdk import CodonSdk
from handlers.codon_handler import handle_codon
from utils.nlp_parser import parse_command

def get_user_secret(user_id):
    return {
        "owner123": "supersecretkey123",
    }.get(user_id)

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
    
    await handle_codon(codon, get_user_secret)
    return {"status": "success", "codon": codon}

def start_p2p_server(host='localhost', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"P2P Server listening on {host}:{port}")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if not data:
                    continue
                
                try:
                    request = json.loads(data.decode())
                    command = request.get('command')
                    user_id = request.get('user_id', "owner123")
                    
                    # Run in event loop for async processing
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

if __name__ == "__main__":
    start_p2p_server()