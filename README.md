# Auditório Silencioso

### Uso de Cyber Threat Intelligence para prevenção proativa de campanhas de Ransomware

O **Auditório Silencioso** é um ambiente experimental desenvolvido como parte de um Trabalho de Conclusão de Curso em Ciência da Computação para investigar o uso de **Cyber Threat Intelligence (CTI)** na prevenção proativa de campanhas de ransomware, em comparação com mecanismos de **Signature-Based Detection (SBD)**.

O projeto foi desenvolvido como um laboratório controlado, determinístico e reproduzível. Não são executadas amostras reais de ransomware. Os comportamentos associados a uma campanha são simulados em um ambiente controlado, permitindo registrar, reproduzir e analisar os eventos produzidos durante cada execução.

---

## Objetivo

O projeto busca investigar a seguinte questão:

> **A Cyber Threat Intelligence consegue detectar e conter campanhas de ransomware de forma mais eficaz do que o Signature-Based Detection?**

A comparação é realizada entre dois mecanismos experimentais:

- **CTI — Cyber Threat Intelligence:** utiliza conhecimento prévio sobre ameaças, técnicas e contexto de campanhas de ransomware para interpretar evidências observadas durante a execução.
- **SBD — Signature-Based Detection:** utiliza regras previamente definidas para reconhecer padrões e características conhecidas associados aos eventos observados.

O objetivo não é comparar produtos comerciais específicos, mas analisar experimentalmente os dois mecanismos dentro de um ambiente controlado.

---

## Metodologia

O ambiente experimental utiliza um cenário corporativo simulado, composto por segmentos de rede, hosts, serviços e vulnerabilidades.

Uma campanha de ransomware simulada é executada por meio de uma sequência fixa de ações, permitindo que diferentes mecanismos de defesa sejam submetidos às mesmas condições experimentais.

A arquitetura separa:

```text
Cenário
   ↓
Ataque
   ↓
Execução
   ↓
Eventos e Evidências
   ↓
┌───────────────┬───────────────┐
│      CTI      │      SBD      │
└───────────────┴───────────────┘
           ↓
       Detecção
           ↓
        Resposta
           ↓
     Estado da rede
           ↓
        Ground Truth
           ↓
         Métricas
