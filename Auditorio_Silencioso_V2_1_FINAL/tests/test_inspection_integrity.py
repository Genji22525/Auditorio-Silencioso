from src.execution.runner import run_execution


def test_inspection_evidence_matches_events():
    result, metrics, inspection = run_execution("CTI", 1, [], inspection=True)
    assert result.execution_id == "EXE-CTI-000001"
    assert len(inspection["evidence"]) == len(inspection["events"])
    assert [e.event_id for e in inspection["evidence"]] == [e.event_id for e in inspection["events"]]
    ids = [e.evidence_id for e in inspection["evidence"]]
    assert len(ids) == len(set(ids))
    assert ids == [f"{result.execution_id}-OBS{i:03d}" for i in range(1, len(ids) + 1)]
    assert metrics["hosts_compromised"] >= metrics["hosts_impacted"]
