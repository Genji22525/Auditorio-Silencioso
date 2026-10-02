import json

from sqlalchemy import delete, text

from src.persistence.database import get_engine, get_session_factory
from src.persistence.schema import (
    Attack, AttackAction, Base, Attempt, Detection, Event, Evidence,
    Execution, ExecutionMetrics, GroundTruth, Host, HostService,
    HostVulnerability, ScenarioRecord, Segment, Service, StateHistory,
    Response, Vulnerability,
)

SCHEMAS = ("scenario", "network", "attack", "execution", "evaluation")


def ensure_schema():
    engine = get_engine()
    with engine.begin() as conn:
        for schema in SCHEMAS:
            conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
    Base.metadata.create_all(engine)


def _get_or_create(session, model, filters, values):
    obj = session.query(model).filter_by(**filters).one_or_none()
    if obj is None:
        obj = model(**values)
        session.add(obj)
        session.flush()
    return obj


def _remove_existing_execution(session, execution_id: str) -> None:
    # Allows the deterministic first-test script to be safely rerun with the same seed.
    session.execute(delete(ExecutionMetrics).where(ExecutionMetrics.execution_id == execution_id))
    session.execute(delete(GroundTruth).where(GroundTruth.execution_id == execution_id))
    session.execute(delete(Response).where(Response.execution_id == execution_id))
    session.execute(delete(Detection).where(Detection.execution_id == execution_id))
    session.execute(delete(StateHistory).where(StateHistory.execution_id == execution_id))
    session.execute(delete(Evidence).where(Evidence.execution_id == execution_id))
    session.execute(delete(Event).where(Event.execution_id == execution_id))
    session.execute(delete(Attempt).where(Attempt.execution_id == execution_id))
    session.execute(delete(Execution).where(Execution.execution_id == execution_id))


def persist_execution(inspection: dict, result, metrics: dict) -> None:
    ensure_schema()
    session = get_session_factory()()
    try:
        scenario = inspection["scenario"]
        scenario_id = scenario["scenario_id"]

        # Structural V2 data: scenario and network.
        _get_or_create(
            session, ScenarioRecord,
            {"scenario_id": scenario_id},
            {"scenario_id": scenario_id, "name": scenario["name"], "version": scenario["version"], "seed": scenario["seed"]},
        )

        for seg in scenario.get("segments", []):
            _get_or_create(
                session, Segment,
                {"scenario_id": scenario_id, "segment_id": seg["id"]},
                {"scenario_id": scenario_id, "segment_id": seg["id"], "name": seg["name"]},
            )

        for host in scenario.get("hosts", []):
            _get_or_create(
                session, Host,
                {"scenario_id": scenario_id, "hostname": host["hostname"]},
                {
                    "scenario_id": scenario_id,
                    "segment_id": host["segment"],
                    "hostname": host["hostname"],
                    "ip_address": host["ip"],
                    "host_type": host["type"],
                    "operating_system": host["os"],
                    "criticality": host["criticality"],
                    "patch_level": host.get("patch_level", "baseline"),
                },
            )

        service_ids = {}
        for service in scenario.get("services", []):
            obj = _get_or_create(
                session, Service,
                {"name": service["name"], "port": service["port"], "protocol": service["protocol"]},
                {
                    "name": service["name"], "port": service["port"], "protocol": service["protocol"],
                    "description": service.get("description", ""), "category": service.get("category"),
                },
            )
            service_ids[(service["name"], service["port"], service["protocol"])] = obj.id

        vulnerability_ids = {}
        for vuln in scenario.get("vulnerabilities", []):
            obj = _get_or_create(
                session, Vulnerability,
                {"cve": vuln["cve"]},
                {"cve": vuln["cve"], "name": vuln["name"]},
            )
            vulnerability_ids[vuln["cve"]] = obj.id

        # The baseline scenario does not currently carry host-service pairs explicitly;
        # attach every declared service only when a matching relation is supplied later.
        for item in scenario.get("host_services", []):
            key = (item["service"], item["port"], item["protocol"])
            service_id = service_ids.get(key)
            if service_id is not None:
                _get_or_create(
                    session, HostService,
                    {"scenario_id": scenario_id, "hostname": item["hostname"], "service_id": service_id},
                    {"scenario_id": scenario_id, "hostname": item["hostname"], "service_id": service_id},
                )

        for item in scenario.get("host_vulnerabilities", []):
            vuln_id = vulnerability_ids.get(item["cve"])
            if vuln_id is not None:
                _get_or_create(
                    session, HostVulnerability,
                    {"scenario_id": scenario_id, "hostname": item["hostname"], "vulnerability_id": vuln_id},
                    {"scenario_id": scenario_id, "hostname": item["hostname"], "vulnerability_id": vuln_id},
                )

        # Attack definition is structural and shared by the two engines.
        attack_id = f"ATK-{scenario_id}"
        _get_or_create(
            session, Attack,
            {"attack_id": attack_id},
            {"attack_id": attack_id, "name": "Simulated Ransomware Campaign", "version": "2.1"},
        )
        for action in inspection.get("attack", []):
            _get_or_create(
                session, AttackAction,
                {"attack_id": attack_id, "action_id": action["action_id"]},
                {"attack_id": attack_id, **{k: action[k] for k in (
                    "action_id", "event_type", "source_host", "target_host",
                    "success_probability", "duration_seconds", "produces_evidence"
                )}},
            )

        _remove_existing_execution(session, result.execution_id)

        session.add(Execution(
            execution_id=result.execution_id,
            engine=result.engine,
            scenario_id=result.scenario_id,
            seed=result.seed,
            detected=result.detected,
            detection_timestamp=result.detection_timestamp,
            relevant_event_timestamp=result.relevant_event_timestamp,
            containment_timestamp=result.containment_timestamp,
            ttd=result.ttd,
            ttc=result.ttc,
        ))
        # Make the execution row visible to PostgreSQL before dependent FK rows.
        session.flush()
        for item in inspection.get("attempts", []):
            session.add(Attempt(execution_id=result.execution_id, **{k: item[k] for k in (
                "action_id", "event_type", "timestamp", "source_host", "target_host", "success"
            )}))
        for event in inspection.get("events", []):
            session.add(Event(
                event_id=event.event_id, execution_id=result.execution_id,
                event_type=event.event_type, timestamp=event.timestamp,
                source_host=event.source_host, target_host=event.target_host,
                success=event.success, details=json.dumps(event.details, ensure_ascii=False),
            ))
        for ev in inspection.get("evidence", []):
            session.add(Evidence(
                evidence_id=ev.evidence_id, execution_id=result.execution_id,
                event_id=ev.event_id, timestamp=ev.timestamp, event_type=ev.event_type,
                source_host=ev.source_host, target_host=ev.target_host,
                attributes=json.dumps(ev.attributes, ensure_ascii=False),
            ))
        for snap in inspection.get("state_history", []):
            states = snap.get("states", {})
            connectivity = snap.get("connectivity", {})
            for host, state in states.items():
                security = state if state in {"healthy", "compromised", "impacted"} else "healthy"
                session.add(StateHistory(
                    execution_id=result.execution_id,
                    timestamp=snap["timestamp"],
                    host=host,
                    security_state=security,
                    connectivity_state=connectivity.get(host, "connected"),
                    transition=snap.get("transition"),
                    cause=snap.get("cause"),
                    snapshot=json.dumps({"security": states, "connectivity": connectivity}, ensure_ascii=False),
                ))
        for det in result.detections:
            session.add(Detection(
                execution_id=result.execution_id, engine=det["engine"], detected=True,
                event_id=det.get("event_id"), timestamp=det.get("timestamp"),
                reason=det.get("reason"), evidence_ids=json.dumps(det.get("evidence_ids", [])),
            ))
        for resp in result.responses:
            session.add(Response(execution_id=result.execution_id, **resp))
        for gt in result.ground_truth:
            session.add(GroundTruth(execution_id=result.execution_id, **gt))

        session.add(ExecutionMetrics(
            execution_id=result.execution_id,
            detection_rate=metrics.get("detection_rate", 0.0),
            coverage=metrics.get("coverage", 0.0),
            ttd=metrics.get("ttd"), ttc=metrics.get("ttc"),
            hosts_compromised=metrics.get("hosts_compromised", 0),
            hosts_impacted=metrics.get("hosts_impacted", 0),
            hosts_preserved=metrics.get("hosts_preserved", 0),
            hosts_isolated=metrics.get("hosts_isolated", 0),
            segments_isolated=metrics.get("segments_isolated", 0),
            hosts_communication_interrupted=metrics.get("hosts_communication_interrupted", 0),
            impact_before_detection=metrics.get("impact_before_detection",),
            impact_before_containment=metrics.get("impact_before_containment",),
            tp=metrics.get("tp"), fp=metrics.get("fp"), fn=metrics.get("fn"), tn=metrics.get("tn"),
        ))
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
