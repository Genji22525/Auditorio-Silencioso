# Migrations — Auditório Silencioso V2.1

A V2.1 utiliza um banco PostgreSQL separado e limpo: `auditorio_silencioso_v3`.

A estrutura inicial completa é criada por `001_initial_v2`/`src.persistence.repository.ensure_schema()` e compreende os schemas:

- `scenario`
- `network`
- `attack`
- `execution`
- `evaluation`

Para a instalação prática, o caminho recomendado é:

```powershell
python scripts/setup_v3_database.py
```

O script cria o banco (caso necessário) e então cria os schemas/tabelas. O banco anterior não é alterado.
