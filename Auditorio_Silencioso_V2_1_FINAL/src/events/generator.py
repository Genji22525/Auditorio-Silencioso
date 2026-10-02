import random
from src.common.models import AttackAction, Event

def execute_actions(actions: list[AttackAction], rng: random.Random, execution_id: str):
    clock = 0.0
    events = []
    attempts = []
    for action in actions:
        clock += action.duration_seconds
        success = rng.random() < action.success_probability
        attempts.append({
            "action_id": action.action_id,
            "event_type": action.event_type,
            "timestamp": clock,
            "source_host": action.source_host,
            "target_host": action.target_host,
            "success": success,
        })
        if success:
            events.append(Event(
                event_id=f"{execution_id}-EV{len(events)+1:03d}",
                execution_id=execution_id,
                event_type=action.event_type,
                timestamp=clock,
                source_host=action.source_host,
                target_host=action.target_host,
                success=True,
                details={"action_id": action.action_id},
            ))
    return attempts, events
