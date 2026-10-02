# 🎧 Auditório Silencioso

### Uso de Cyber Threat Intelligence para prevenção proativa de campanhas de Ransomware

**Autor:** Arthur Garcia Nonis
**Curso:** Ciência da Computação
**Tipo:** Trabalho de Conclusão de Curso

---

### 🏷️ Status e classificação

🧪 Projeto experimental
📚 Trabalho de Conclusão de Curso
🔬 Ambiente controlado
🛡️ Cyber Threat Intelligence
🚨 Ransomware
🔎 Signature-Based Detection
🐍 Python
🐘 PostgreSQL

---

## 📌 Sobre

O **Auditório Silencioso** é um projeto experimental desenvolvido no contexto de um Trabalho de Conclusão de Curso em **Ciência da Computação**, com foco na aplicação de **Cyber Threat Intelligence (CTI)** para prevenção proativa de campanhas de ransomware.

O projeto propõe um ambiente controlado e reproduzível para comparar dois mecanismos de detecção e resposta:

* 🧠 **Cyber Threat Intelligence (CTI)**
* 🔎 **Signature-Based Detection (SBD)**

A proposta não é comparar produtos comerciais específicos, mas estudar como diferentes abordagens de identificação e resposta podem se comportar diante de uma campanha de ransomware simulada.

> ⚠️ **Importante:** o projeto não executa ransomware real. Todos os comportamentos relacionados à campanha são simulados dentro de um ambiente experimental controlado.

---

## 📑 Sumário

* [1. Sobre o projeto](#1-sobre-o-projeto)
* [2. Objetivos](#2-objetivos)

  * [2.1. Objetivo geral](#21-objetivo-geral)
  * [2.2. Objetivos específicos](#22-objetivos-específicos)
* [3. Conceito experimental](#3-conceito-experimental)
* [4. Ambiente experimental](#4-ambiente-experimental)
* [5. Modelo do ataque](#5-modelo-do-ataque)
* [6. CTI — Cyber Threat Intelligence](#6-cti--cyber-threat-intelligence)
* [7. SBD — Signature-Based Detection](#7-sbd--signature-based-detection)
* [8. CTI × SBD](#8-cti--sbd)
* [9. Resposta e defesa](#9-resposta-e-defesa)
* [10. Ground Truth](#10-ground-truth)
* [11. Estado da infraestrutura](#11-estado-da-infraestrutura)
* [12. State History](#12-state-history)
* [13. Métricas](#13-métricas)
* [14. Defesa realizada com sucesso](#14-defesa-realizada-com-sucesso)
* [15. Experimento](#15-experimento)
* [16. Reprodutibilidade](#16-reprodutibilidade)
* [17. Banco de dados](#17-banco-de-dados)
* [18. Estrutura do banco](#18-estrutura-do-banco)
* [19. Estrutura do projeto](#19-estrutura-do-projeto)
* [20. Tecnologias](#20-tecnologias)
* [21. Fontes de dados](#21-fontes-de-dados)
* [22. Scripts principais](#22-scripts-principais)
* [23. Instalação](#23-instalação)
* [24. Configuração do banco](#24-configuração-do-banco)
* [25. Validação](#25-validação)
* [26. Resultados experimentais](#26-resultados-experimentais)
* [27. Análise dos resultados](#27-análise-dos-resultados)
* [28. Falsos positivos](#28-falsos-positivos)
* [29. Limitações](#29-limitações)
* [30. Decisões metodológicas](#30-decisões-metodológicas)
* [31. Protocolo experimental](#31-protocolo-experimental)
* [32. Auditoria](#32-auditoria)
* [33. Referência metodológica](#33-referência-metodológica)
* [34. Estado atual do projeto](#34-estado-atual-do-projeto)
* [35. Próximos passos](#35-próximos-passos)
* [36. Segurança](#36-segurança)
* [37. Finalidade](#37-finalidade)
* [38. Autor](#38-autor)
