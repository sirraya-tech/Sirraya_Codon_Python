# codon_p2p.py
import socket
import json
import sys
import webbrowser

HOST = ''          # For server: listen on all interfaces
PORT = 65432       # Fixed port

def run_server():
    """Receiver - runs on Machine B"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVER] Listening on port {PORT}...")

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
                    user_id = request.get("user_id")

                    print(f"[SERVER] Received command: {command} from {user_id}")

                    # Execute the command
                    if command == "open_browser":
                        webbrowser.open("https://www.google.com")
                        response = {"status": "success", "action": "browser opened"}
                    else:
                        response = {"status": "error", "message": "Unknown command"}

                except Exception as e:
                    response = {"status": "error", "message": str(e)}

                conn.sendall(json.dumps(response).encode())


def send_p2p_command(command, host, port=PORT):
    """Client - runs on Machine A"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        request = json.dumps({
            "command": command,
            "user_id": "owner123"
        })
        s.sendall(request.encode())
        data = s.recv(1024)
        return json.loads(data.decode())


def run_client(server_ip):
    """Interactive client shell"""
    while True:
        command = input("Enter command (or 'exit' to quit): ").strip()
        if command.lower() == "exit":
            break
        response = send_p2p_command(command, server_ip)
        print("Response:", response)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Server (Machine B): python codon_p2p.py server")
        print("  Client (Machine A): python codon_p2p.py client <server_ip>")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "server":
        run_server()
    elif mode == "client":
        if len(sys.argv) < 3:
            print("Please provide the server IP: python codon_p2p.py client <server_ip>")
            sys.exit(1)
        server_ip = sys.argv[2]
        run_client(server_ip)
    else:
        print("Unknown mode. Use 'server' or 'client'.")
