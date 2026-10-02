from src.execution.runner import run_execution

def test_same_seed_same_result():
    a, ma = run_execution("CTI", 7, [])
    b, mb = run_execution("CTI", 7, [])
    assert a.ground_truth == b.ground_truth
    assert ma == mb
