"""
RIPASSO: i thread in Python (preparazione all'attività 3, calcolatrice v4)

Un THREAD è un "flusso di esecuzione" dentro lo stesso programma.
Con più thread il programma può portare avanti più compiti "insieme":
mentre un thread aspetta (rete, disco, sleep), un altro lavora.

Eseguire con:  python ripasso_thread.py
"""

from threading import Thread, Lock
import time


# ---------------------------------------------------------------------------
# PARTE 1 - Senza thread: i compiti vengono eseguiti uno dopo l'altro
# ---------------------------------------------------------------------------
def servi_cliente(numero):
    """Simula un cliente che richiede 1 secondo di attesa (es. una risposta di rete)."""
    print(f"  cliente {numero}: inizio")
    time.sleep(1)                      # attesa: qui il programma "non fa niente"
    print(f"  cliente {numero}: fine")


print("PARTE 1 - Sequenziale (3 clienti uno alla volta)")
inizio = time.time()
for i in range(1, 4):
    servi_cliente(i)
print(f"  Tempo totale: {time.time() - inizio:.1f} s\n")   # circa 3 s


# ---------------------------------------------------------------------------
# PARTE 2 - Con i thread: i compiti procedono in parallelo
# ---------------------------------------------------------------------------
print("PARTE 2 - Con i thread (3 clienti insieme)")
inizio = time.time()
lista_thread = []
for i in range(1, 4):
    # target = funzione da eseguire, args = i suoi parametri (tupla!)
    t = Thread(target=servi_cliente, args=(i,))
    t.start()                          # il thread parte SUBITO, il for continua
    lista_thread.append(t)

for t in lista_thread:
    t.join()                           # aspetto che ogni thread abbia finito
print(f"  Tempo totale: {time.time() - inizio:.1f} s\n")   # circa 1 s
# Nota: l'ordine dei messaggi "inizio/fine" può cambiare a ogni esecuzione.

 