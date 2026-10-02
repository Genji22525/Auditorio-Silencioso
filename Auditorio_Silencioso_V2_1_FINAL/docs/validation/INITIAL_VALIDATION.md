# Validação inicial

A V2.1 funcional possui uma primeira validação automatizada de:
- determinismo com a mesma seed;
- isolamento entre execuções CTI/SBD;
- tentativa ≠ evento;
- Ground Truth produzido independentemente;
- métricas básicas reproduzíveis;
- geração de gráficos a partir dos resultados;
- preservação dos dados RAW;
- processamento reproduzível.

## Limitação metodológica registrada

A matriz completa TP/FP/FN/TN exige uma população de evidências negativas/benignas explicitamente definida. Esta versão não inventa essa população. A estrutura para os cálculos foi criada, mas a estimativa científica completa de falsos positivos será fechada quando o modelo de evidência negativa fizer parte da metodologia.
