# Laboratorio socket TCP/UDP con Wireshark

Percorso in tre tappe sugli script Python della calcolatrice: si parte dai thread, si confrontano UDP e TCP, si osserva un server TCP multithread. Tutte le catture si fanno sull'interfaccia di loopback (Windows: **Adapter for loopback traffic capture / Npcap Loopback**; Linux: `lo`).

```
ripasso_thread.py        ripasso sui thread
a2/udp/  calc-server.py  calc-client.py   calcolatrice UDP (v1), porta 5005
a2/tcp/  calc-server.py  calc-client.py   calcolatrice TCP (v2), porta 65432
a3/      calc-server.py  calc-client.py   calcolatrice TCP multithread (v4), porta 22224
```

Requisiti: Python 3 (nessuna libreria esterna) e Wireshark con Npcap. Su Windows, se `python` non funziona, usare `py -3`.

## 1) Ripasso: comprensione del codice sui thread

```
python ripasso_thread.py
```

Leggere il codice e l'output delle quattro parti:

1. **Sequenziale:** tre attese da 1 s una dopo l'altra, circa 3 s in tutto.
2. **Thread:** le stesse attese con `threading.Thread(target=..., args=(...))`, `start()` e `join()`, circa 1 s in tutto.
3. **Un calcolo per thread:** come i client dell'attività 3, ogni thread ha i suoi dati e salva il risultato.
4. **Dati condivisi:** più thread modificano lo stesso contatore, protetto da un `Lock`.

Prima di proseguire bisogna saper spiegare cosa fanno `start()` e `join()` e perché l'ordine delle stampe può cambiare.

## 2) Attività 2: UDP (v1) contro TCP (v2)

Il client invia una sola richiesta, sempre uguale: `{"primoNumero":7,"operazione":"*","secondoNumero":6}`. La richiesta è di 52 byte e la risposta `42` è di 2 byte.

1. Avviare la cattura in Wireshark.
2. **UDP:** nella cartella `a2/udp`, terminale A `python calc-server.py`, terminale B `python calc-client.py`.
3. **UDP con server spento:** fermare il server (Ctrl+C) e rilanciare il client. Osservare cosa arriva al client (ICMP, timeout o errore).
4. **TCP:** nella cartella `a2/tcp`, terminale A `python calc-server.py`, terminale B `python calc-client.py`.
5. **TCP con server spento:** fermare il server e rilanciare il client. Osservare il RST.
6. Fermare e salvare la cattura.

Cosa confrontare: la presenza o l'assenza dell'handshake e della chiusura, il numero di pacchetti per lo stesso scambio di dati, la lunghezza del payload (UDP Length e TCP Len) e cosa succede quando il server non c'è.

## 3) Attività 3: server TCP multithread (v4)

Il client avvia **15 thread** che si connettono insieme. Il thread i invia `{"primoNumero":10+i,"operazione":"+","secondoNumero":20}` e riceve `30+i`: ogni richiesta è di 54 byte e ogni risposta di 2 byte.

1. Nella cartella `a3`, terminale A `python calc-server.py` (lasciarlo acceso).
2. Avviare la cattura, poi nel terminale B eseguire **una sola volta** `python calc-client.py`.
3. Attendere il tempo totale stampato dal client, fermare e salvare la cattura. Infine Ctrl+C nel terminale A.

Cosa osservare: quante connessioni (`tcp.stream`) ci sono, le porte del client e del server, chi chiude per primo e l'ordine con cui i thread vengono serviti (in Statistiche → Conversazioni e nel Flow Graph).

`calc-server.py` usa `listen(32)` al posto del `listen(5)` originale. Con una coda da 5 e 15 connessioni contemporanee alcuni SYN vengono scartati e ritrasmessi, e i risultati cambiano da una prova all'altra.

## Filtri utili (schemi generali)

| Scopo | Schema del filtro |
|---|---|
| Un protocollo | `udp`, `tcp`, `icmp` |
| Una porta, in entrambe le direzioni | `udp.port == P`, `tcp.port == P` |
| Solo verso il server, o solo dal server | `tcp.dstport == P`, `tcp.srcport == P` |
| Un indirizzo | `ip.addr == X`, `ip.src == X`, `ip.dst == X` |
| Escludere qualcosa | `!(filtro)`, ad esempio `!(ip.addr == X)`: **non** `ip.addr != X` |
| Tutte le condizioni insieme (AND) | `filtro1 && filtro2` |
| Almeno una condizione (OR) | `filtro1 \|\| filtro2` |
| Una singola connessione TCP | `tcp.stream == N` |
| Solo i pacchetti con dati | `tcp.len > 0`, `udp.length > 8` |
| Contenuto del payload | `frame contains "testo"` |
| Apertura della connessione | `tcp.flags.syn == 1` (solo SYN iniziali: `&& tcp.flags.ack == 0`) |
| Chiusura e reset | `tcp.flags.fin == 1`, `tcp.flags.reset == 1` |
| Porta UDP chiusa | `icmp.type == 3` |
| Problemi TCP | `tcp.analysis.retransmission`, `tcp.analysis.flags` |

Esempio combinato: `tcp.port == P && tcp.flags.syn == 1 && tcp.flags.ack == 0` mostra solo le richieste di apertura verso il server sulla porta P.

Strumenti: **Statistiche → Conversazioni** (una riga per connessione), **Statistiche → Flow Graph**, **Segui → Flusso TCP/UDP**.
