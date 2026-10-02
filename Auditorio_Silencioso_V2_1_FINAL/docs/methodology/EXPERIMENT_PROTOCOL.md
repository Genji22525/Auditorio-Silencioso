# Protocolo experimental definitivo

## Pergunta

A Cyber Threat Intelligence consegue detectar e conter campanhas de ransomware simuladas de forma mais eficaz do que o Signature-Based Detection, sob as condições definidas pelo laboratório?

## Unidade experimental

Uma execução é uma campanha simulada em um cenário estrutural fixo. A seed determina a sequência estocástica do ataque. CTI e SBD recebem a mesma seed, mas mantêm estado operacional independente.

## Amostra

- Seed 1: validação técnica, excluída da amostra.
- Seeds 2–31: 30 pares.
- 30 execuções CTI + 30 execuções SBD = 60 execuções positivas.

## Controles

- mesmo cenário;
- mesma estratégia de ataque;
- mesma seed dentro de cada par;
- Ground Truth independente dos motores;
- CTI sem acesso a eventos futuros;
- SBD sem acesso ao conhecimento CTI;
- nenhuma execução de ransomware real.

## Efeito da resposta

A resposta defensiva pode modificar conectividade e tornar ações posteriores inviáveis. Isso é parte da dinâmica experimental. O ataque não consulta o motor defensivo para escolher ações; ele apenas encontra o estado operacional resultante quando uma tentativa é avaliada.

## Métricas

- taxa de detecção;
- TTD;
- TTC;
- cobertura da campanha = hosts que atingiram comprometimento / total de hosts;
- hosts comprometidos;
- hosts impactados;
- hosts preservados;
- hosts isolados;
- impacto antes da detecção;
- impacto antes da contenção.

TTD = instante da primeira detecção − instante do primeiro evento observável bem-sucedido.

TTC = instante da contenção − instante da detecção.

## Confusão estatística

TP/FP/FN/TN permanecem não definidos nesta bateria, pois a amostra final é composta somente por execuções positivas. Uma população benigna independente seria necessária para avaliar falsos positivos e verdadeiros negativos.

## Interpretação

A análise é descritiva e pareada. Não existe score agregado, ranking ou vencedor pré-definido. As conclusões devem permanecer limitadas ao modelo, cenário, corpus e políticas de resposta implementados.
