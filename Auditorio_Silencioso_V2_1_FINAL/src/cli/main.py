import json
from pathlib import Path
import pandas as pd
from src.execution.runner import run_execution
from src.evaluation.comparison import aggregate
from src.metrics.plots import generate_comparison_plots

ROOT = Path(__file__).resolve().parents[2]

def load_sbd_rules():
    path = ROOT / "data/processed/sbd/selected_rules.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    print("=" * 48)
    print("       AUDITÓRIO SILENCIOSO V2.1")
    print("=" * 48)
    print("Motor que atuará primeiro:")
    print("[1] CTI")
    print("[2] SBD")
    first = input("Escolha: ").strip()
    first_engine = "CTI" if first != "2" else "SBD"

    try:
        n = int(input("Quantidade de execuções: ").strip())
        if n < 1:
            raise ValueError
    except ValueError:
        print("Quantidade inválida.")
        return

    confirm = input("Iniciar? [S/N] ").strip().upper()
    if confirm != "S":
        print("Execução cancelada.")
        return

    second_engine = "SBD" if first_engine == "CTI" else "CTI"
    rules = load_sbd_rules()
    rows = []

    for i in range(1, n + 1):
        # Same initial experimental seed per paired execution; execution state
        # is isolated. Engine order affects only operational order.
        seed = i
        for engine in (first_engine, second_engine):
            result, metrics = run_execution(engine, seed, rules)
            row = {"execution_id": result.execution_id, "engine": engine, "seed": seed, **metrics}
            rows.append(row)
            out = ROOT / "results/runs" / f"{result.execution_id}.json"
            out.write_text(json.dumps({
                "result": result.__dict__,
                "metrics": metrics,
            }, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[OK] {result.execution_id} | detectou={result.detected} | TTD={result.ttd}")

    df = pd.DataFrame(rows)
    df.to_csv(ROOT / "results/metrics/executions.csv", index=False)
    summary = aggregate(rows)
    (ROOT / "results/metrics/summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    generate_comparison_plots(summary, ROOT / "results/plots")

    print("\nResumo:")
    print(pd.DataFrame(summary).T.to_string())
    print("\nResultados: results/runs/")
    print("Métricas:   results/metrics/")
    print("Gráficos:   results/plots/")

if __name__ == "__main__":
    main()
