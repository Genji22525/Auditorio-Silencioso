# Auditório Silencioso — V2.1 (versão experimental definitiva)

Laboratório controlado e reproduzível para comparar **Cyber Threat Intelligence (CTI)** e **Signature-Based Detection (SBD)** diante de uma campanha simulada de ransomware. Nenhum ransomware real é executado.

## Banco oficial

A versão definitiva continua compatível com o PostgreSQL V3 já utilizado no projeto:

```text
Database: auditorio_silencioso_v3
Host: localhost
Port: 5432
```

O `.env` define `DATABASE_URL`; não é necessário alterar o código para conectar ao V3.

## Preparação

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/setup_v3_database.py
```

Se o banco V3 já existe e contém os schemas V2.1, o setup apenas verifica/cria o que faltar. Ele não apaga as execuções existentes.

## Fechamento dos dados

### CTI

```powershell
python scripts/finalize_cti.py
```

O script preserva o RAW, considera candidatos de 2024–2026 e gera:

- `data/processed/cti/cti_selection_audit.csv` — auditoria dos 366 candidatos;
- `data/processed/cti/cti_selection_audit.json`;
- `data/processed/cti/cti_operational_r1.json` — corpus operacional final;
- `data/processed/cti/cti_selection_summary.json`.

A seleção final é R1=6, R2=3 e R3=357. R2 é contextual e não entra no conhecimento operacional; R3 é excluído.

### SBD

O dataset final validado é `data/processed/sbd/selected_rules.json`, derivado das Snort 3 Community Rules. A seleção não é enriquecida com CTI.

## Validação técnica

```powershell
python scripts/first_execution.py
python scripts/verify_v3_database.py
```

A seed 1 é somente validação técnica e não entra na amostra final.

## Experimento definitivo

```powershell
python scripts/run_experiment.py
python scripts/analyze_experiment.py
```

O protocolo definitivo é:

- seeds 2–31;
- 30 execuções CTI;
- 30 execuções SBD;
- 60 execuções positivas;
- 30 pares CTI/SBD com a mesma seed;
- Ground Truth independente;
- resultados persistidos no PostgreSQL V3;
- CSV e JSON em `results/experiment/`.

TP/FP/FN/TN permanecem nulos porque esta versão não declara uma população negativa. Não se deve inferir taxa de falso positivo a partir da bateria positiva.

## Artigo de referência metodológica

O projeto utiliza como referência metodológica complementar: Alkhalaf, Alruwaili, El-Latif e Al-Najdawi (2025), *Proactive identification of cybersecurity compromises via the PROID compromise assessment framework*, Scientific Reports, 15, 39102, DOI 10.1038/s41598-025-24936-2.

A relação é metodológica: o artigo estabelece Ground Truth em ambiente simulado, usa uma linha de base reproduzível e compara métodos analíticos sobre a mesma realidade observada. O Auditório Silencioso não reproduz o PROID: seu objeto é especificamente comparar CTI e SBD em uma campanha simulada de ransomware.

Veja `docs/methodology/ARTICLE_REFERENCE_PROID.md`.

## Estrutura de resultados

`results/experiment/executions.csv` contém uma linha por execução.
`results/experiment/summary.json` contém agregações por motor.
`results/experiment/analysis.json` contém diferenças pareadas descritivas.

## Regra científica

Os resultados devem ser interpretados como evidência do comportamento **deste modelo experimental**, e não como afirmação universal sobre CTI ou SBD em ambientes reais. Não há score agregado nem vencedor pré-definido.
