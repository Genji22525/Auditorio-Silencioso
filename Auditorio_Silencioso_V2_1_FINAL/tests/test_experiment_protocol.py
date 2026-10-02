import json
from pathlib import Path
from src.execution.runner import run_execution


def test_paired_seed_keeps_attack_rng_independent_of_engine_order():
    rules=json.loads((Path(__file__).resolve().parents[1]/"data/processed/sbd/selected_rules.json").read_text(encoding="utf-8"))
    cti,_,ci=run_execution("CTI",seed=23,sbd_rules=rules,inspection=True)
    sbd,_,si=run_execution("SBD",seed=23,sbd_rules=rules,inspection=True)
    assert [a["timestamp"] for a in ci["attempts"]]==[a["timestamp"] for a in si["attempts"]]
    assert [a["action_id"] for a in ci["attempts"]]==[a["action_id"] for a in si["attempts"]]
    assert [a["success"] for a in ci["attempts"]][:4]==[a["success"] for a in si["attempts"]][:4]
    assert cti.execution_id!=sbd.execution_id
