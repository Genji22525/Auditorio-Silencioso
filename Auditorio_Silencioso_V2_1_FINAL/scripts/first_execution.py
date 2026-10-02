"""Run the seed-1 technical validation against CTI and SBD and persist it."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.execution.runner import run_execution
from src.persistence.repository import persist_execution


def main():
    rules_path = ROOT / "data/processed/sbd/selected_rules.json"
    rules = json.loads(rules_path.read_text(encoding="utf-8")) if rules_path.exists() else []
    for engine in ("CTI", "SBD"):
        result, metrics, inspection = run_execution(engine, seed=1, sbd_rules=rules, inspection=True)
        persist_execution(inspection, result, metrics)
        print(f"{engine}: {result.execution_id} detected={result.detected} ttd={result.ttd} ttc={result.ttc}")
    print("Validação técnica seed=1 persistida no PostgreSQL V3.")


if __name__ == "__main__":
    main()
