import socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    print(f"Detected IP: {ip}")
    s.close()
except Exception as e:
    print(f"Error: {e}")
