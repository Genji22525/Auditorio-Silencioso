import random

from src.scenario.model import build_scenario
from src.attack.model import build_attack
from src.state.history import (
    initial_states,
    initial_connectivity,
    apply_event,
    apply_response,
    action_viable,
)
from src.ground_truth.tracker import build_ground_truth
from src.evidence.builder import build_evidence
from src.engines.cti.engine import CTIEngine
from src.engines.sbd.engine import SBDEngine
from src.response.policy import containment_allowed
from src.evaluation.metrics import calculate_execution_metrics
from src.common.models import ExecutionResult, Event


def run_execution(engine_name: str, seed: int, sbd_rules=None, inspection=False):
    execution_id = f"EXE-{engine_name}-{seed:06d}"

    # The scenario is a shared structural baseline.
    # The seed controls the stochastic behavior of this execution.
    scenario = build_scenario(seed)
    attack = build_attack()
    rng = random.Random(seed)

    security_states = initial_states(scenario.hosts)
    connectivity = initial_connectivity(scenario.hosts)

    cti = CTIEngine()
    sbd = SBDEngine(sbd_rules or [])
    engine = cti if engine_name == "CTI" else sbd

    attempts = []
    events = []
    evidence = []

    detections = []
    responses = []
    history = []
    state_history = []

    clock = 0.0
    detection = None
    containment_ts = None

    def record_snapshot(timestamp, transition=None, cause=None):
        state_history.append({
            "timestamp": timestamp,
            "states": dict(security_states),
            "connectivity": dict(connectivity),
            "transition": transition,
            "cause": cause,
        })

    record_snapshot(0.0, cause="initial_state")

    for action in attack:
        clock += action.duration_seconds

        viable = action_viable(action, connectivity)
        random_value = rng.random()
        success = viable and (random_value < action.success_probability)

        attempt = {
            "action_id": action.action_id,
            "event_type": action.event_type,
            "timestamp": clock,
            "source_host": action.source_host,
            "target_host": action.target_host,
            "success": success,
            "viable": viable,
        }

        attempts.append(attempt)

        if not success:
            record_snapshot(
                clock,
                cause="attempt_failed_or_not_viable",
            )
            continue

        event = Event(
            event_id=f"{execution_id}-EV{len(events) + 1:03d}",
            execution_id=execution_id,
            event_type=action.event_type,
            timestamp=clock,
            source_host=action.source_host,
            target_host=action.target_host,
            success=True,
            details={
                "action_id": action.action_id,
            },
        )

        events.append(event)

        apply_event(security_states, event)

        # Snapshot do estado produzido pelo evento,
        # antes de qualquer resposta defensiva.
        record_snapshot(
            clock,
            cause=f"event:{event.event_id}",
        )

        obs = build_evidence(
            execution_id,
            event,
            len(evidence) + 1,
        )
        evidence.append(obs)

        detection_candidate = (
            engine.inspect(obs, history)
            if engine_name == "CTI"
            else engine.inspect(obs)
        )

        history.append(obs)

        if detection is None and detection_candidate is not None:
            detection = detection_candidate

            detections.append({
                "engine": detection.engine,
                "event_id": detection.event_id,
                "timestamp": detection.timestamp,
                "reason": detection.reason,
                "evidence_ids": detection.evidence_ids,
            })

            if containment_allowed(engine_name):
                response = engine.response(
                    detection,
                    event.target_host,
                )

                containment_ts = response.timestamp

                responses.append({
                    "engine": response.engine,
                    "action": response.action,
                    "timestamp": response.timestamp,
                    "target_host": response.target_host,
                    "reason": response.reason,
                })

                apply_response(connectivity, response)

                record_snapshot(
                    response.timestamp,
                    transition=response.action,
                    cause="defensive_response",
                )

    # Ground Truth remains independent of detector decisions.
    # It is constructed from attempts, events and state history.
    state_at_attempt = []

    for attempt in attempts:
        prior = [
            snapshot
            for snapshot in state_history
            if snapshot["timestamp"] <= attempt["timestamp"]
        ]

        state_at_attempt.append(
            prior[-1]["states"]
            if prior
            else dict(security_states)
        )

    gt = build_ground_truth(
        attempts,
        events,
        state_at_attempt,
    )

    # TTD is measured from the first successful observable of the campaign
    # to the first detection, not from the detection event itself.
    relevant_event = events[0] if events else None

    hosts_compromised = {
        g.target_host
        for g in gt
        if (
            g.success
            and g.event_type in {"E01", "E02", "E03", "E04", "E05"}
        )
    }

    hosts_impacted = {
        g.target_host
        for g in gt
        if (
            g.success
            and g.event_type == "E05"
        )
    }

    hosts_preserved = (
        set(h["hostname"] for h in scenario.hosts)
        - hosts_compromised
        - hosts_impacted
    )

    hosts_isolated = {
        host
        for host, state in connectivity.items()
        if state == "host_isolated"
    }

    hosts_interrupted = {
        host
        for host, state in connectivity.items()
        if state == "communication_interrupted"
    }

    result = ExecutionResult(
        execution_id=execution_id,
        engine=engine_name,
        scenario_id=scenario.scenario_id,
        seed=seed,

        detected=detection is not None,

        detection_timestamp=(
            detection.timestamp
            if detection
            else None
        ),

        relevant_event_timestamp=(
            relevant_event.timestamp
            if relevant_event
            else None
        ),

        containment_timestamp=containment_ts,

        ttd=(
            detection.timestamp - relevant_event.timestamp
            if detection and relevant_event
            else None
        ),

        ttc=(
            containment_ts - detection.timestamp
            if containment_ts and detection
            else None
        ),

        hosts_affected=len(hosts_impacted),
        hosts_preserved=len(hosts_preserved),

        # Impacts strictly before detection. `<` (not `<=`) is used so that
        # an impact occurring at the exact same instant as the detection is
        # not counted as having happened "before" it. When there is no
        # detection, there is no detection instant to compare against, so
        # the value is None rather than 0 or a sum over all events.
        impact_before_detection=(
            sum(
                1
                for event in events
                if (
                    event.event_type == "E05"
                    and event.timestamp < detection.timestamp
                )
            )
            if detection
            else None
        ),

        # Impacts strictly before containment. When containment did not
        # occur (e.g. SBD detects but does not contain), "impact before
        # containment" is not a meaningful quantity, so the value is None
        # rather than 0 — this avoids conflating "no containment happened"
        # with "containment happened with zero prior impact".
        impact_before_containment=(
            sum(
                1
                for event in events
                if (
                    event.event_type == "E05"
                    and event.timestamp < containment_ts
                )
            )
            if containment_ts is not None
            else None
        ),

        events_total=len(events),
        evidence_total=len(evidence),

        detections=detections,
        responses=responses,
        ground_truth=[
            g.__dict__
            for g in gt
        ],
    )

    metrics = calculate_execution_metrics(
        gt,
        result,
        len(scenario.hosts),
        connectivity=connectivity,
    )

    if not inspection:
        return result, metrics

    inspection_data = {
        "scenario": scenario.__dict__,
        "attack": [
            action.__dict__
            for action in attack
        ],
        "attempts": attempts,
        "events": events,
        "evidence": evidence,
        "state_history": state_history,
        "ground_truth": gt,
        "detections": detections,
        "responses": responses,
        "metrics": metrics,
        "result": result,
    }

    return result, metrics, inspection_data