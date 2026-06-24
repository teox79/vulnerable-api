# vulnerable-api (demo shop API)

⚠️ **Progetto deliberatamente vulnerabile.** Serve SOLO come fixture per testare
il processo di analisi/lifecycle/dedup di ORBIT. Non eseguire in produzione né
esporre in rete: contiene vulnerabilità intenzionali e nessun segreto reale.

## Cos'è
Piccola API Flask di un negozio: lookup utenti e ordini, login, download report,
diagnostica di rete, restore di sessione. SQLite come storage.

```
app/
  __init__.py     # create_app, registra i blueprint
  db.py           # data-access condiviso (run_query su stringa SQL)
  users.py        # endpoint utenti
  orders.py       # endpoint ordini
  auth.py         # login + hashing password
  files.py        # download report
  exec.py         # diagnostica (ping)
  deserialize.py  # restore sessione
main.py           # entry point
schema.sql        # schema + seed demo
```

## Avvio
```bash
pip install -r requirements.txt
sqlite3 shop.db < schema.sql
python main.py   # http://localhost:8000
```

## Trust boundary
Tutti gli endpoint accettano input non autenticato dall'esterno (query string,
body JSON, path) che fluisce verso DB, filesystem, shell e deserializzazione.

## Answer key — vulnerabilità piantate
Elenco atteso dei finding (usalo per verificare scanner + lifecycle):

| # | File | Tipo | CWE | OWASP |
|---|------|------|-----|-------|
| 1 | app/users.py | SQL injection (`name`, f-string) | CWE-89 | A03 |
| 2 | app/users.py | SQL injection (`user_id`, concatenazione) | CWE-89 | A03 |
| 3 | app/orders.py | SQL injection (`customer`, f-string) | CWE-89 | A03 |
| 4 | app/auth.py | Credenziali hardcoded (signing secret + API key) | CWE-798 | A07 |
| 5 | app/auth.py | Hashing password debole (MD5) | CWE-327 | A02 |
| 6 | app/files.py | Path traversal (`path`) | CWE-22 | A01 |
| 7 | app/exec.py | Command injection (`host` in os.popen) | CWE-78 | A03 |
| 8 | app/deserialize.py | Deserializzazione insicura (pickle.loads) | CWE-502 | A08 |

### Caso DEDUP cross-file
I finding **1/2/3** condividono la stessa root cause: uso non parametrizzato di
`db.run_query` (helper condiviso). Sono su file diversi → l'intra-run dedup
dovrebbe **consolidarli** (una sola remediation: parametrizzare `run_query`).
Servono a verificare il dedup cross-file e poi il matching cross-run.

### Suggerimenti per testare il lifecycle
- **Fix → retest**: parametrizza una delle query e ri-scansiona → il finding
  relativo dovrebbe passare a `pending_retest`/`fixed`.
- **Regressione**: reintroduci la vuln dopo il fix → dovrebbe tornare `regressed`.
