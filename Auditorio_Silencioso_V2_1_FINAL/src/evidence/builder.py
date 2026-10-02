from src.common.models import Evidence


def build_evidence(execution_id, event, index):
    return Evidence(
        evidence_id=f"{execution_id}-OBS{index:03d}",
        execution_id=execution_id,
        event_id=event.event_id,
        timestamp=event.timestamp,
        event_type=event.event_type,
        source_host=event.source_host,
        target_host=event.target_host,
        attributes={
            "observable_event_type": event.event_type,
            "source_host": event.source_host,
            "target_host": event.target_host,
        },
    )
