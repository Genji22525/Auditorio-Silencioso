# Banco PostgreSQL — Auditório Silencioso V2.1

## Banco oficial da V3

```text
Database: auditorio_silencioso_v3
Host: localhost
Port: 5432
```

O banco V3 é intencionalmente separado do banco utilizado nas versões anteriores. O objetivo é iniciar a persistência do V2.1 em uma base limpa e reproduzível, sem carregar tabelas ou estados históricos do projeto anterior.

## Schemas

```text
scenario
network
attack
execution
evaluation
```

### scenario
- `scenario.scenarios`

### network
- `network.segments`
- `network.hosts`
- `network.services`
- `network.vulnerabilities`
- `network.host_services`
- `network.host_vulnerabilities`

### attack
- `attack.attacks`
- `attack.attack_actions`

### execution
- `execution.executions`
- `execution.attempts`
- `execution.events`
- `execution.evidence`
- `execution.state_history`
- `execution.detections`
- `execution.responses`
- `execution.ground_truth`

### evaluation
- `evaluation.execution_metrics`

## Criação

Configure `.env` a partir de `.env.example` e confirme as credenciais do PostgreSQL. Em seguida:

```powershell
python scripts/setup_v3_database.py
```

O script:
1. conecta ao banco administrativo `postgres`;
2. cria `auditorio_silencioso_v3` se ele ainda não existir;
3. cria/verifica os cinco schemas;
4. cria/verifica as tabelas V2.1.

Ele não remove nem altera o banco anterior.

## Conexão no DBeaver

Criar uma nova conexão PostgreSQL com:

```text
Host: localhost
Port: 5432
Database: auditorio_silencioso_v3
User: postgres
Password: <a senha configurada no seu PostgreSQL>
```

Depois da criação, atualizar/reconectar a conexão para visualizar os cinco schemas.

## Primeiro teste persistido

Com o banco V3 criado:

```powershell
python scripts/first_execution.py
```

O script executa CTI e SBD com seed 1 e persiste os dados estruturais, operacionais e de avaliação.
