# Referência metodológica — PROID

**Referência:** ALKHALAF, Abdulaziz Abdullah; ALRUWAILI, Fahad F.; EL-LATIF, Ahmed A. Abd; AL-NAJDAWI, Nijad. *Proactive identification of cybersecurity compromises via the PROID compromise assessment framework*. Scientific Reports, v. 15, art. 39102, 2025. DOI: 10.1038/s41598-025-24936-2.

Fonte oficial: https://www.nature.com/articles/s41598-025-24936-2

## O que foi estudado

O artigo apresenta o PROID, um framework de Compromise Assessment que integra Threat Intelligence e Threat Hunting e combina quatro formas de análise: assinatura, hunting sem assinatura, reconhecimento automatizado de padrões e análise humana. A validação ocorre em um ambiente empresarial simulado, com 31 técnicas MITRE ATT&CK distribuídas por dez táticas. Os autores descrevem que os ataques foram implementados primeiro para estabelecer Ground Truth em uma linha de base fixa e reproduzível; depois, os métodos foram avaliados usando o mesmo conjunto de hipóteses e telemetria.

## O que é aproveitado pelo Auditório Silencioso

A principal contribuição metodológica para este projeto é a preocupação explícita com **Ground Truth independente, ambiente simulado controlado e linha de base reproduzível**. Isso sustenta a decisão de registrar o Ground Truth separadamente dos motores e de executar CTI e SBD sobre a mesma realização estocástica de cada seed.

Outra aproximação é a separação entre preparação/escopo, execução e análise dos resultados. No Auditório Silencioso, isso aparece como dados RAW/processados, configuração experimental, execução, Ground Truth, persistência e avaliação.

## O que não deve ser confundido

O PROID não é um modelo CTI-versus-SBD e não é um estudo específico de ransomware. Ele combina múltiplos métodos de detecção em um framework de Compromise Assessment. Portanto, o artigo é uma **referência metodológica**, não uma validação externa da hipótese do Auditório Silencioso.

O resultado do artigo também não deve ser transferido para o nosso experimento como se fosse uma conclusão sobre CTI ou SBD.
