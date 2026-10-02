from src.common.models import GroundTruthRecord, Event

def build_ground_truth(attempts, events, state_snapshots):
    event_by_action = {e.details["action_id"]: e for e in events}
    records = []
    for idx, a in enumerate(attempts):
        e = event_by_action.get(a["action_id"])
        snapshot = state_snapshots[idx] if idx < len(state_snapshots) else {}
        records.append(GroundTruthRecord(
            timestamp=a["timestamp"],
            action_id=a["action_id"],
            success=a["success"],
            source_host=a["source_host"],
            target_host=a["target_host"],
            event_type=e.event_type if e else None,
            host_state_after=snapshot.get(a["target_host"], "unchanged"),
        ))
    return records
