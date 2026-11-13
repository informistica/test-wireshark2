"""
RIPASSO: i thread in Python (preparazione all'attività 3, calcolatrice v4)

Un THREAD è un "flusso di esecuzione" dentro lo stesso programma.
Con più thread il programma può portare avanti più compiti "insieme":
mentre un thread aspetta (rete, disco, sleep), un altro lavora.

Eseguire con:  python ripasso_thread.py
"""

import threading
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
    t = threading.Thread(target=servi_cliente, args=(i,))
    t.start()                          # il thread parte SUBITO, il for continua
    lista_thread.append(t)

for t in lista_thread:
    t.join()                           # aspetto che ogni thread abbia finito
print(f"  Tempo totale: {time.time() - inizio:.1f} s\n")   # circa 1 s
# Nota: l'ordine dei messaggi "inizio/fine" può cambiare a ogni esecuzione.


# ---------------------------------------------------------------------------
# PARTE 3 - Ogni thread fa un calcolo diverso (come i 15 client della v4)
# ---------------------------------------------------------------------------
risultati = {}                         # dizionario condiviso tra i thread

def calcola(id_thread, a, b):
    time.sleep(0.5)                    # simula il viaggio in rete
    risultati[id_thread] = a + b
    print(f"  thread {id_thread}: {a} + {b} = {a + b}")

print("PARTE 3 - 5 thread, ognuno con la sua operazione")
lista_thread = [threading.Thread(target=calcola, args=(i, 10 + i, 20))
                for i in range(1, 6)]
for t in lista_thread:
    t.start()
for t in lista_thread:
    t.join()
print(f"  Risultati raccolti: {dict(sorted(risultati.items()))}\n")


# ---------------------------------------------------------------------------
# PARTE 4 - Dati condivisi: serve un Lock
# ---------------------------------------------------------------------------
# Se più thread modificano la stessa variabile, le modifiche si possono
# "sovrapporre". Il Lock garantisce che una sola modifica alla volta avvenga.
contatore = 0
lucchetto = threading.Lock()

def incrementa(volte):
    global contatore
    for _ in range(volte):
        with lucchetto:                # entra uno alla volta
            contatore += 1

print("PARTE 4 - 4 thread incrementano lo stesso contatore")
lista_thread = [threading.Thread(target=incrementa, args=(100_000,)) for _ in range(4)]
for t in lista_thread:
    t.start()
for t in lista_thread:
    t.join()
print(f"  Contatore finale: {contatore} (atteso 400000)\n")


# ---------------------------------------------------------------------------
# COLLEGAMENTO CON IL LABORATORIO
# ---------------------------------------------------------------------------
# - client v4: crea 15 thread; ognuno apre il SUO socket TCP, invia la sua
#   richiesta JSON e aspetta la risposta  -> in Wireshark vedrai 15 tcp.stream.
# - server v4: per ogni connessione accettata (accept) avvia un thread che
#   serve quel client, così il server non resta bloccato su un solo cliente.
# Domanda da porsi prima della cattura: se i 15 thread partono insieme,
# in che ordine arriveranno le connessioni al server?
