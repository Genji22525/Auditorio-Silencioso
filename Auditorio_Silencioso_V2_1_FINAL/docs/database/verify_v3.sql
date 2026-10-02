-- Execute this script in DBeaver while connected specifically to:
-- auditorio_silencioso_v3

SELECT current_database() AS database_name, current_user AS database_user;

SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema IN ('scenario','network','attack','execution','evaluation')
ORDER BY table_schema, table_name;

SELECT execution_id, engine, scenario_id, seed, detected, ttd, ttc
FROM execution.executions
ORDER BY execution_id;

SELECT 'executions' AS tabela, COUNT(*) AS registros FROM execution.executions
UNION ALL SELECT 'attempts', COUNT(*) FROM execution.attempts
UNION ALL SELECT 'events', COUNT(*) FROM execution.events
UNION ALL SELECT 'evidence', COUNT(*) FROM execution.evidence
UNION ALL SELECT 'detections', COUNT(*) FROM execution.detections
UNION ALL SELECT 'responses', COUNT(*) FROM execution.responses
UNION ALL SELECT 'state_history', COUNT(*) FROM execution.state_history
UNION ALL SELECT 'ground_truth', COUNT(*) FROM execution.ground_truth
UNION ALL SELECT 'execution_metrics', COUNT(*) FROM evaluation.execution_metrics;

SELECT execution_id, detection_rate, coverage, ttd, ttc,
       hosts_compromised, hosts_impacted, hosts_preserved,
       hosts_isolated, hosts_communication_interrupted,
       impact_before_detection, impact_before_containment
FROM evaluation.execution_metrics
ORDER BY execution_id;
