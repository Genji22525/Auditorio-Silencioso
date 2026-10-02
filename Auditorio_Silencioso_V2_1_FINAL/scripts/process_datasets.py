from pathlib import Path
from src.engines.cti.processor import process_manifest
from src.engines.sbd.processor import process_selected_rules

ROOT = Path(__file__).resolve().parents[1]

cti_candidates = ROOT / "data/raw/cti/misp_circl/manifest.json"
if cti_candidates.exists():
    records = process_manifest(
        cti_candidates,
        ROOT / "data/processed/cti/misp_circl_manifest_processed.json"
    )
    print(f"CTI processado: {len(records)} eventos do manifest.")

sbd_csv = ROOT / "data/raw/sbd/snort3/sbd_rule_dataset_final.csv"
if sbd_csv.exists():
    df = process_selected_rules(
        sbd_csv,
        ROOT / "data/processed/sbd/selected_rules.json"
    )
    print(f"SBD processado: {len(df)} regras selecionadas.")
