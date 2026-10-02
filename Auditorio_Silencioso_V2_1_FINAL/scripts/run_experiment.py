import csv
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.execution.runner import run_execution
from src.persistence.repository import persist_execution

START_SEED = 2
END_SEED = 31
ENGINES = ("CTI", "SBD")
RULES_PATH = ROOT / "data/processed/sbd/selected_rules.json"
CTI_PATH = ROOT / "data/processed/cti/cti_operational_r1.json"
OUT_DIR = ROOT / "results/experiment"
CSV_PATH = OUT_DIR / "executions.csv"
SUMMARY_PATH = OUT_DIR / "summary.json"
CONFIG_PATH = OUT_DIR / "experiment_config.json"


def main():
    if not CTI_PATH.exists():
        raise FileNotFoundError(f"CTI operacional ausente: {CTI_PATH}. Execute scripts/finalize_cti.py.")
    if not RULES_PATH.exists():
        raise FileNotFoundError(f"Regras SBD ausentes: {RULES_PATH}. Execute scripts/process_datasets.py ou restaure o dataset validado.")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rules = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    cti_records = json.loads(CTI_PATH.read_text(encoding="utf-8"))
    if not cti_records:
        raise RuntimeError("Dataset CTI operacional vazio.")
    if len(rules) == 0:
        raise RuntimeError("Dataset SBD vazio.")
    rows = []
    for seed in range(START_SEED, END_SEED + 1):
        for engine in ENGINES:
            result, metrics, inspection = run_execution(engine, seed=seed, sbd_rules=rules, inspection=True)
            persist_execution(inspection, result, metrics)
            rows.append({
                "execution_id": result.execution_id,
                "engine": engine,
                "scenario_id": result.scenario_id,
                "seed": seed,
                "detected": int(result.detected),
                "detection_rate": metrics["detection_rate"],
                "coverage": metrics["coverage"],
                "ttd": metrics["ttd"],
                "ttc": metrics["ttc"],
                "hosts_compromised": metrics["hosts_compromised"],
                "hosts_impacted": metrics["hosts_impacted"],
                "hosts_preserved": metrics["hosts_preserved"],
                "hosts_isolated": metrics["hosts_isolated"],
                "segments_isolated": metrics["segments_isolated"],
                "hosts_communication_interrupted": metrics["hosts_communication_interrupted"],
                "impact_before_detection": metrics["impact_before_detection"],
                "impact_before_containment": metrics["impact_before_containment"],
            })
            print(f"{engine}: seed={seed} detected={result.detected} ttd={result.ttd} ttc={result.ttc} comp={metrics['hosts_compromised']} impact={metrics['hosts_impacted']} isolated={metrics['hosts_isolated']}")

    if len(rows) != (END_SEED - START_SEED + 1) * len(ENGINES):
        raise RuntimeError("Número inesperado de execuções.")
    fields = list(rows[0].keys())
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader(); writer.writerows(rows)
    summary = {"seeds": [START_SEED, END_SEED], "executions": len(rows), "engines": {}}
    for engine in ENGINES:
        subset = [r for r in rows if r["engine"] == engine]
        summary["engines"][engine] = {"executions": len(subset)}
        for key in ("detection_rate", "coverage", "ttd", "ttc", "hosts_compromised", "hosts_impacted", "hosts_preserved", "hosts_isolated", "impact_before_detection", "impact_before_containment"):
            vals = [r[key] for r in subset if r[key] is not None]
            summary["engines"][engine][key] = {"mean": statistics.mean(vals) if vals else None, "median": statistics.median(vals) if vals else None, "stdev": statistics.stdev(vals) if len(vals) >= 2 else None, "n": len(vals)}
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    CONFIG_PATH.write_text(json.dumps({"scenario_id":"SCN-000001","scenario_version":"2.1","seed_range":[START_SEED,END_SEED],"engines":list(ENGINES),"total_executions":len(rows),"cti_dataset":"data/processed/cti/cti_operational_r1.json","sbd_dataset":"data/processed/sbd/selected_rules.json","ground_truth":"independent per execution","negative_population":False}, indent=2), encoding="utf-8")
    print(f"Experimento concluído: {len(rows)} execuções")
    print(f"CSV: {CSV_PATH}")
    print(f"Resumo: {SUMMARY_PATH}")

if __name__ == "__main__": main()
