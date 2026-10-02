from src.execution.runner import run_execution

def test_engine_runs_are_independent():
    cti, _ = run_execution("CTI", 11, [])
    sbd, _ = run_execution("SBD", 11, [])
    assert cti.execution_id != sbd.execution_id
    assert cti.engine == "CTI"
    assert sbd.engine == "SBD"
