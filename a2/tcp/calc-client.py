"""Client del laboratorio: una sola richiesta fissa, originali invariati."""
import json
import socket

HOST = "127.0.0.1"
REQUEST = {"primoNumero": 7, "operazione": "*", "secondoNumero": 6}
PAYLOAD = json.dumps(REQUEST, separators=(",", ":"), ensure_ascii=True).encode("ascii")

PORT = 65432
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(3)
        sock.connect((HOST, PORT))
        print("Richiesta:", PAYLOAD.decode(), "byte:", len(PAYLOAD))
        sock.sendall(PAYLOAD)
        parts = []
        while True:
            chunk = sock.recv(1024)
            if not chunk:
                break
            parts.append(chunk)
        data = b"".join(parts)
        print("Risposta:", data.decode(), "byte:", len(data))
except ConnectionRefusedError:
    print("Connessione rifiutata: osservare SYN e RST nella cattura.")
except socket.timeout:
    print("Timeout: verificare server, firewall e cattura.")
