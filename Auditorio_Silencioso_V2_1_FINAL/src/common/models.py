from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

@dataclass
class Scenario:
    scenario_id: str
    name: str
    version: str
    seed: int
    segments: list[dict[str, Any]]
    hosts: list[dict[str, Any]]
    services: list[dict[str, Any]]
    vulnerabilities: list[dict[str, Any]]

@dataclass
class AttackAction:
    action_id: str
    event_type: str
    source_host: str
    target_host: str
    success_probability: float
    duration_seconds: int
    produces_evidence: bool = True

@dataclass
class Event:
    event_id: str
    execution_id: str
    event_type: str
    timestamp: float
    source_host: str
    target_host: str
    success: bool
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class GroundTruthRecord:
    timestamp: float
    action_id: str
    success: bool
    source_host: str
    target_host: str
    event_type: str | None
    host_state_after: str

@dataclass
class Evidence:
    evidence_id: str
    execution_id: str
    event_id: str
    timestamp: float
    event_type: str
    source_host: str
    target_host: str
    attributes: dict[str, Any] = field(default_factory=dict)

@dataclass
class Detection:
    engine: str
    detected: bool
    event_id: str | None
    timestamp: float | None
    reason: str | None
    evidence_ids: list[str] = field(default_factory=list)

@dataclass
class ResponseAction:
    engine: str
    action: str
    timestamp: float
    target_host: str | None
    reason: str

@dataclass
class ExecutionResult:
    execution_id: str
    engine: str
    scenario_id: str
    seed: int
    detected: bool
    detection_timestamp: float | None
    relevant_event_timestamp: float | None
    containment_timestamp: float | None
    ttd: float | None
    ttc: float | None
    hosts_affected: int
    hosts_preserved: int
    impact_before_detection: int
    impact_before_containment: int
    events_total: int
    evidence_total: int
    detections: list[dict[str, Any]]
    responses: list[dict[str, Any]]
    ground_truth: list[dict[str, Any]]
