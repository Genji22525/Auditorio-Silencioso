def calculate_execution_metrics(gt, result, total_hosts, connectivity=None):
    successes = [g for g in gt if g.success]
    compromised = {g.target_host for g in successes if g.event_type in {"E01", "E02", "E03", "E04", "E05"}}
    impacted = {g.target_host for g in successes if g.event_type == "E05"}
    preserved = set()
    all_hosts = {g.target_host for g in gt} if gt else set()
    if connectivity is not None:
        all_hosts |= set(connectivity)
    preserved = all_hosts - compromised - impacted
    connectivity = connectivity or {}

    return {
        "detection_rate": 1.0 if result.detected else 0.0,
        "coverage": len(compromised) / total_hosts if total_hosts else 0.0,
        "ttd": result.ttd,
        "ttc": result.ttc,
        "hosts_compromised": len(compromised),
        "hosts_impacted": len(impacted),
        "hosts_preserved": len(preserved),
        "hosts_isolated": sum(v == "host_isolated" for v in connectivity.values()),
        "segments_isolated": 0,
        "hosts_communication_interrupted": sum(v == "communication_interrupted" for v in connectivity.values()),
        "impact_before_detection": result.impact_before_detection,
        "impact_before_containment": result.impact_before_containment,
        "tp": None, "fp": None, "fn": None, "tn": None,
    }
