from src.execution.runner import run_execution

def test_ttd_is_measured_from_first_successful_observable():
    cti, _, _ = run_execution("CTI", seed=1, sbd_rules=[], inspection=True)
    # The baseline CTI detection happens after the first successful observable.
    # The invariant is that TTD is not forced to 0 merely because detection and
    # the selected detection event share a timestamp.
    assert cti.ttd is not None
    assert cti.ttd > 0
