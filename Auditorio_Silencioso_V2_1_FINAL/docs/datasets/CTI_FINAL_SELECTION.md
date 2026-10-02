# Seleção final do dataset CTI

## Fonte

Fonte primária: **CIRCL OSINT / MISP**. O RAW original permanece em `data/raw/cti/misp_circl/manifest.json`.

## Janela temporal

Foram considerados eventos datados de **2024, 2025 e 2026**, produzindo 366 candidatos a partir do manifest de 1.680 eventos.

## Critérios

- **R1 — operacional:** ransomware diretamente relevante e com conteúdo técnico estruturado suficiente para compor o conhecimento prévio experimental, especialmente TTPs/indicadores/contexto técnico.
- **R2 — contextual:** relacionado a ransomware e potencialmente útil para contexto, mas sem necessidade de entrar no núcleo operacional da comparação.
- **R3 — excluído:** fora do foco operacional ou insuficiente para o objetivo experimental.

## Resultado

| Classe | Quantidade | Uso |
|---|---:|---|
| R1 | 6 | conhecimento operacional CTI |
| R2 | 3 | contexto/documentação |
| R3 | 357 | excluído do conhecimento operacional |
| Total | 366 | candidatos 2024–2026 |

### R1

1. Backmydata Ransomware IOCs — 2024-02-19
2. #StopRansomware: Akira Ransomware — 2024-04-19
3. CISA AA24-131A: Black Basta — 2024-05-10
4. CISA AA24-242A: RansomHub — 2024-08-30
5. Inside the Dragon: DragonForce Ransomware Group — 2024-10-01
6. AA25-071A: Medusa Ransomware — 2025-03-03

### R2

- Ransomware Strikes Indian Banking Infrastructure / RansomEXX — 2024-08-21
- Salesforce Gainsight Security Advisory — 2025-11-26
- Datacarry Ransomware — 2026-02-18

A auditoria completa, incluindo os 357 registros R3 e os motivos de exclusão, está em `cti_selection_audit.csv`.

## Limitação importante

O manifest disponível contém metadados, tags e referências contextuais; ele não é um dump completo de atributos IOC. Portanto, o motor CTI não deve ser descrito como se estivesse fazendo matching de IP/domínio/hash diretamente. O corpus R1 é usado como **conhecimento prévio contextual/TTP**, e a detecção é feita pela correlação temporal de evidências observadas segundo a taxonomia comportamental do simulador.
