"""Verify the V3 PostgreSQL database and report persisted execution counts."""
import sys
from pathlib import Path

from sqlalchemy import text

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.persistence.database import get_engine


TABLES = [
    ("scenario", "scenarios"),
    ("network", "segments"),
    ("network", "hosts"),
    ("network", "services"),
    ("network", "vulnerabilities"),
    ("attack", "attacks"),
    ("attack", "attack_actions"),
    ("execution", "executions"),
    ("execution", "attempts"),
    ("execution", "events"),
    ("execution", "evidence"),
    ("execution", "detections"),
    ("execution", "responses"),
    ("execution", "state_history"),
    ("execution", "ground_truth"),
    ("evaluation", "execution_metrics"),
]


def main():
    engine = get_engine()
    with engine.connect() as conn:
        print(f"database={conn.execute(text('SELECT current_database()')).scalar()}")
        print("\nTabelas:")
        for schema, table in TABLES:
            count = conn.execute(text(f'SELECT COUNT(*) FROM "{schema}"."{table}"')).scalar()
            print(f"  {schema}.{table}: {count}")

        print("\nExecuções:")
        rows = conn.execute(text('''
            SELECT execution_id, engine, scenario_id, seed, detected, ttd, ttc
            FROM "execution"."executions"
            ORDER BY execution_id
        '''))
        for row in rows:
            print("  ", dict(row._mapping))

        print("\nMétricas:")
        rows = conn.execute(text('''
            SELECT execution_id, detection_rate, coverage, ttd, ttc,
                   hosts_compromised, hosts_impacted, hosts_preserved,
                   hosts_isolated, hosts_communication_interrupted
            FROM "evaluation"."execution_metrics"
            ORDER BY execution_id
        '''))
        for row in rows:
            print("  ", dict(row._mapping))


if __name__ == "__main__":
    main()
