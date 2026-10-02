"""Generate descriptive plots from the definitive experiment summary."""
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.metrics.plots import generate_comparison_plots

def main():
    p=ROOT/"results/experiment/summary.json"
    if not p.exists(): raise FileNotFoundError("Rode primeiro scripts/run_experiment.py")
    data=json.loads(p.read_text(encoding="utf-8"))
    summary=data.get("engines",data)
    generate_comparison_plots(summary, ROOT/"results/experiment/plots")
    print("Gráficos gerados em results/experiment/plots/")
if __name__=="__main__": main()
