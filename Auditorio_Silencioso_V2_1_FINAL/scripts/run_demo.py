from src.execution.runner import run_execution
from src.engines.sbd.processor import process_selected_rules
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
rules_path = ROOT / "data/processed/sbd/selected_rules.json"
rules = json.loads(rules_path.read_text(encoding="utf-8")) if rules_path.exists() else []

for engine in ("CTI", "SBD"):
    result, metrics = run_execution(engine, seed=1, sbd_rules=rules)
    print("\n" + "="*60)
    print(engine, result.execution_id)
    print("Ground Truth:")
    for item in result.ground_truth:
        print(item)
    print("Métricas:", metrics)
