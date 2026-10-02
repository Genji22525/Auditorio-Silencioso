# Auditoria da versão definitiva

## Código

- Compilação Python: aprovada.
- Testes automatizados: 7 aprovados.
- Determinismo por seed: testado.
- IDs de evidência: testados.
- Independência de execução entre CTI/SBD: testada.
- Semântica TTD: testada.
- Dataset CTI R1: testado com 6 registros.
- Pareamento por seed: testado.

## Dados

- CTI RAW: 1.680 eventos.
- Candidatos 2024–2026: 366.
- CTI R1: 6.
- CTI R2: 3.
- CTI R3: 357.
- SBD final: 1.191 regras selecionadas.

## Banco

O código definitivo aponta por padrão para `auditorio_silencioso_v3`. O script `preflight.py` impede a execução definitiva caso outro banco seja conectado. A conexão PostgreSQL real depende do serviço local do usuário e deve ser validada executando o preflight no Windows antes da bateria final.

## Experimento

- Seed 1: validação técnica.
- Seeds 2–31: amostra definitiva.
- 30 pares CTI/SBD.
- 60 execuções positivas.
- Ground Truth independente.
- TP/FP/FN/TN não calculados sem população negativa.

## Referência metodológica

O artigo de Alkhalaf et al. (2025), PROID, foi incorporado como referência metodológica para Ground Truth, ambiente simulado, baseline reproduzível e avaliação de métodos sobre uma mesma realidade observada. O artigo não é tratado como equivalente ao Auditório Silencioso.
