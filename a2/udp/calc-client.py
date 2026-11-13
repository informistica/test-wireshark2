"""Client del laboratorio: una sola richiesta fissa, originali invariati."""
import json
import socket

HOST = "127.0.0.1"
REQUEST = {"primoNumero": 7, "operazione": "*", "secondoNumero": 6}
PAYLOAD = json.dumps(REQUEST, separators=(",", ":"), ensure_ascii=True).encode("ascii")

PORT = 5005
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.settimeout(3)
    print("Richiesta:", PAYLOAD.decode(), "byte:", len(PAYLOAD))
    sock.sendto(PAYLOAD, (HOST, PORT))
    try:
        data, peer = sock.recvfrom(1024)
        print("Risposta:", data.decode(), "byte:", len(data))
    except socket.timeout:
        print("Timeout: nessuna risposta UDP entro 3 secondi. Controllare anche ICMP nella cattura.")
    except ConnectionResetError:
        print("Errore ICMP notificato dal sistema (possibile su Windows): nessuna risposta applicativa UDP.")
