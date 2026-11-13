"""Client del laboratorio (Attività 3): 15 thread, richieste fisse e note, originali invariati.

Il thread i (1..15) invia {"primoNumero":10+i,"operazione":"+","secondoNumero":20}
e si aspetta 30+i: richieste tutte da 54 byte, risposte tutte da 2 byte.
Ogni thread apre la PROPRIA connessione TCP verso 127.0.0.1:22224.
"""
import json
import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 22224
NUM_WORKERS = 15
partenza = threading.Barrier(NUM_WORKERS)  # i 15 thread chiamano connect insieme
stampa = threading.Lock()


def richiesta(i):
    msg = {"primoNumero": 10 + i, "operazione": "+", "secondoNumero": 20}
    return json.dumps(msg, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def lavoratore(i):
    payload = richiesta(i)
    partenza.wait()
    inizio = time.perf_counter()  # appena prima di connect (≈ SYN)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(5)
        sock.connect((HOST, PORT))
        porta_locale = sock.getsockname()[1]
        sock.sendall(payload)
        risposta = sock.recv(1024)
    fine = time.perf_counter()  # subito dopo la chiusura (≈ FIN del client)
    with stampa:
        print(f"Thread-{i:02d} porta client {porta_locale} richiesta {payload.decode()} "
              f"({len(payload)} byte) risposta {risposta.decode()} ({len(risposta)} byte) "
              f"tempo {fine - inizio:.6f} s", flush=True)


if __name__ == "__main__":
    t0 = time.perf_counter()
    threads = [threading.Thread(target=lavoratore, args=(i,), name=f"Thread-{i:02d}")
               for i in range(1, NUM_WORKERS + 1)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"Tempo totale impiegato = {time.perf_counter() - t0:.6f} s")
