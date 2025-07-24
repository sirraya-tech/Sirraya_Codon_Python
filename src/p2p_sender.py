# p2p_sender.py
import socket
import json

def send_p2p_command(command, host='localhost', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        request = json.dumps({
            "command": command,
            "user_id": "owner123"  # Can be parameterized
        })
        s.sendall(request.encode())
        data = s.recv(1024)
        return json.loads(data.decode())

if __name__ == "__main__":
    while True:
        command = input("Enter command (or 'exit' to quit): ").strip()
        if command.lower() == 'exit':
            break
        response = send_p2p_command(command)
        print("Response:", response)