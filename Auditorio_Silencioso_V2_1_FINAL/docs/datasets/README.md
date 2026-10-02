# Dados científicos

## CTI

Fonte: CIRCL OSINT / MISP.

- RAW: `data/raw/cti/misp_circl/manifest.json`
- Manifest original: 1.680 eventos
- Janela candidata: 2024–2026
- Candidatos: 366
- R1 operacional: 6
- R2 contextual: 3
- R3 excluído: 357
- Dataset operacional: `data/processed/cti/cti_operational_r1.json`
- Auditoria: `data/processed/cti/cti_selection_audit.csv`

A seleção não cria IOC, TTP ou evento que não esteja no material de origem. A taxonomia interna E01–E05 é uma camada explícita do simulador para transformar observáveis comportamentais em classes comparáveis.

## SBD

Fonte: Snort 3 Community Rules.

- RAW: `data/raw/sbd/snort3/`
- Dataset operacional congelado: `data/processed/sbd/selected_rules.json`
- Regras selecionadas: 1.191
- Duplicidades SID+REV: 0
- Seleção independente da CTI e dos resultados experimentais.

## Regra de proveniência

RAW é preservado. Processado é derivado do RAW. Nenhum resultado experimental pode ser usado para alterar retrospectivamente os datasets.
