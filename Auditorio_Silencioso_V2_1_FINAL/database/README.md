# PostgreSQL V3 — Auditório Silencioso V2.1

O banco oficial da V2.1 é `auditorio_silencioso_v3`.

A criação automatizada é feita por:

```powershell
python scripts/setup_v3_database.py
```

Após a criação, o DBeaver deve usar uma nova conexão apontando para `auditorio_silencioso_v3`. O banco anterior permanece separado e não é modificado.
