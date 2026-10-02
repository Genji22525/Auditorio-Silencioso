import json
from pathlib import Path


def test_final_cti_dataset_is_closed_and_r1_only():
    root=Path(__file__).resolve().parents[1]
    data=json.loads((root/"data/processed/cti/cti_operational_r1.json").read_text(encoding="utf-8"))
    assert len(data)==6
    assert all(item.get("classification")=="R1" for item in data)
    assert all(item.get("source")=="CIRCL OSINT / MISP" for item in data)
