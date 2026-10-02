from sqlalchemy import Boolean, Float, ForeignKey, Integer, BigInteger, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


# -------------------- Scenario / Network --------------------
class ScenarioRecord(Base):
    __tablename__ = "scenarios"
    __table_args__ = (
        UniqueConstraint("name", "version", name="uq_scenario_name_version"),
        {"schema": "scenario"},
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    scenario_id: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    version: Mapped[str] = mapped_column(String(30), nullable=False)
    seed: Mapped[int] = mapped_column(Integer, nullable=False)


class Segment(Base):
    __tablename__ = "segments"
    __table_args__ = ({"schema": "network"},)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    scenario_id: Mapped[str] = mapped_column(ForeignKey("scenario.scenarios.scenario_id"), nullable=False, index=True)
    segment_id: Mapped[str] = mapped_column(String(80), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    __table_args__ = (
        UniqueConstraint("scenario_id", "segment_id", name="uq_segment_scenario_segment"),
        {"schema": "network"},
    )


class Host(Base):
    __tablename__ = "hosts"
    __table_args__ = (
        UniqueConstraint("scenario_id", "hostname", name="uq_host_scenario_hostname"),
        UniqueConstraint("scenario_id", "ip_address", name="uq_host_scenario_ip"),
        {"schema": "network"},
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    scenario_id: Mapped[str] = mapped_column(ForeignKey("scenario.scenarios.scenario_id"), nullable=False, index=True)
    segment_id: Mapped[str] = mapped_column(String(80), nullable=False)
    hostname: Mapped[str] = mapped_column(String(80), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)
    host_type: Mapped[str] = mapped_column(String(40), nullable=False)
    operating_system: Mapped[str] = mapped_column(String(100), nullable=False)
    criticality: Mapped[str] = mapped_column(String(30), nullable=False)
    patch_level: Mapped[str] = mapped_column(String(100), nullable=False, default="baseline")


class Service(Base):
    __tablename__ = "services"
    __table_args__ = (
        UniqueConstraint("name", "port", "protocol", name="uq_service_name_port_protocol"),
        {"schema": "network"},
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False)
    protocol: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    category: Mapped[str | None] = mapped_column(String(50))


class Vulnerability(Base):
    __tablename__ = "vulnerabilities"
    __table_args__ = (
        UniqueConstraint("cve", name="uq_vulnerability_cve"),
        {"schema": "network"},
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    cve: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)


class HostService(Base):
    __tablename__ = "host_services"
    __table_args__ = (
        UniqueConstraint("scenario_id", "hostname", "service_id", name="uq_host_service"),
        {"schema": "network"},
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    scenario_id: Mapped[str] = mapped_column(ForeignKey("scenario.scenarios.scenario_id"), nullable=False, index=True)
    hostname: Mapped[str] = mapped_column(String(80), nullable=False)
    service_id: Mapped[int] = mapped_column(ForeignKey("network.services.id"), nullable=False)


class HostVulnerability(Base):
    __tablename__ = "host_vulnerabilities"
    __table_args__ = (
        UniqueConstraint("scenario_id", "hostname", "vulnerability_id", name="uq_host_vulnerability"),
        {"schema": "network"},
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    scenario_id: Mapped[str] = mapped_column(ForeignKey("scenario.scenarios.scenario_id"), nullable=False, index=True)
    hostname: Mapped[str] = mapped_column(String(80), nullable=False)
    vulnerability_id: Mapped[int] = mapped_column(ForeignKey("network.vulnerabilities.id"), nullable=False)


# -------------------- Attack --------------------
class Attack(Base):
    __tablename__ = "attacks"
    __table_args__ = {"schema": "attack"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    attack_id: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    version: Mapped[str] = mapped_column(String(30), nullable=False)


class AttackAction(Base):
    __tablename__ = "attack_actions"
    __table_args__ = (
        UniqueConstraint("attack_id", "action_id", name="uq_attack_action"),
        {"schema": "attack"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    attack_id: Mapped[str] = mapped_column(ForeignKey("attack.attacks.attack_id"), nullable=False, index=True)
    action_id: Mapped[str] = mapped_column(String(40), nullable=False)
    event_type: Mapped[str] = mapped_column(String(10), nullable=False)
    source_host: Mapped[str] = mapped_column(String(80), nullable=False)
    target_host: Mapped[str] = mapped_column(String(80), nullable=False)
    success_probability: Mapped[float] = mapped_column(Float, nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    produces_evidence: Mapped[bool] = mapped_column(Boolean, nullable=False)


# -------------------- Execution --------------------
class Execution(Base):
    __tablename__ = "executions"
    __table_args__ = {"schema": "execution"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    execution_id: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    engine: Mapped[str] = mapped_column(String(10), nullable=False)
    scenario_id: Mapped[str] = mapped_column(ForeignKey("scenario.scenarios.scenario_id"), nullable=False, index=True)
    seed: Mapped[int] = mapped_column(Integer, nullable=False)
    detected: Mapped[bool] = mapped_column(Boolean, nullable=False)
    detection_timestamp: Mapped[float | None] = mapped_column(Float)
    relevant_event_timestamp: Mapped[float | None] = mapped_column(Float)
    containment_timestamp: Mapped[float | None] = mapped_column(Float)
    ttd: Mapped[float | None] = mapped_column(Float)
    ttc: Mapped[float | None] = mapped_column(Float)


class Attempt(Base):
    __tablename__ = "attempts"
    __table_args__ = {"schema": "execution"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    execution_id: Mapped[str] = mapped_column(ForeignKey("execution.executions.execution_id"), nullable=False, index=True)
    action_id: Mapped[str] = mapped_column(String(40), nullable=False)
    event_type: Mapped[str] = mapped_column(String(10), nullable=False)
    timestamp: Mapped[float] = mapped_column(Float, nullable=False)
    source_host: Mapped[str] = mapped_column(String(80), nullable=False)
    target_host: Mapped[str] = mapped_column(String(80), nullable=False)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)


class Event(Base):
    __tablename__ = "events"
    __table_args__ = {"schema": "execution"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    execution_id: Mapped[str] = mapped_column(ForeignKey("execution.executions.execution_id"), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(10), nullable=False)
    timestamp: Mapped[float] = mapped_column(Float, nullable=False)
    source_host: Mapped[str] = mapped_column(String(80), nullable=False)
    target_host: Mapped[str] = mapped_column(String(80), nullable=False)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)
    details: Mapped[str] = mapped_column(Text, nullable=False, default="{}")


class Evidence(Base):
    __tablename__ = "evidence"
    __table_args__ = {"schema": "execution"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    evidence_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    execution_id: Mapped[str] = mapped_column(ForeignKey("execution.executions.execution_id"), nullable=False, index=True)
    event_id: Mapped[str] = mapped_column(ForeignKey("execution.events.event_id"), nullable=False)
    timestamp: Mapped[float] = mapped_column(Float, nullable=False)
    event_type: Mapped[str] = mapped_column(String(10), nullable=False)
    source_host: Mapped[str] = mapped_column(String(80), nullable=False)
    target_host: Mapped[str] = mapped_column(String(80), nullable=False)
    attributes: Mapped[str] = mapped_column(Text, nullable=False, default="{}")


class StateHistory(Base):
    __tablename__ = "state_history"
    __table_args__ = {"schema": "execution"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    execution_id: Mapped[str] = mapped_column(ForeignKey("execution.executions.execution_id"), nullable=False, index=True)
    timestamp: Mapped[float] = mapped_column(Float, nullable=False)
    host: Mapped[str] = mapped_column(String(80), nullable=False)
    security_state: Mapped[str] = mapped_column(String(30), nullable=False)
    connectivity_state: Mapped[str] = mapped_column(String(40), nullable=False)
    transition: Mapped[str | None] = mapped_column(String(100))
    cause: Mapped[str | None] = mapped_column(String(100))
    snapshot: Mapped[str] = mapped_column(Text, nullable=False, default="{}")


class Detection(Base):
    __tablename__ = "detections"
    __table_args__ = {"schema": "execution"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    execution_id: Mapped[str] = mapped_column(ForeignKey("execution.executions.execution_id"), nullable=False, index=True)
    engine: Mapped[str] = mapped_column(String(10), nullable=False)
    detected: Mapped[bool] = mapped_column(Boolean, nullable=False)
    event_id: Mapped[str | None] = mapped_column(String(100))
    timestamp: Mapped[float | None] = mapped_column(Float)
    reason: Mapped[str | None] = mapped_column(Text)
    evidence_ids: Mapped[str] = mapped_column(Text, nullable=False, default="[]")


class Response(Base):
    __tablename__ = "responses"
    __table_args__ = {"schema": "execution"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    execution_id: Mapped[str] = mapped_column(ForeignKey("execution.executions.execution_id"), nullable=False, index=True)
    engine: Mapped[str] = mapped_column(String(10), nullable=False)
    action: Mapped[str] = mapped_column(String(80), nullable=False)
    timestamp: Mapped[float] = mapped_column(Float, nullable=False)
    target_host: Mapped[str | None] = mapped_column(String(80))
    reason: Mapped[str] = mapped_column(Text, nullable=False)


class GroundTruth(Base):
    __tablename__ = "ground_truth"
    __table_args__ = {"schema": "execution"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    execution_id: Mapped[str] = mapped_column(ForeignKey("execution.executions.execution_id"), nullable=False, index=True)
    timestamp: Mapped[float] = mapped_column(Float, nullable=False)
    action_id: Mapped[str] = mapped_column(String(40), nullable=False)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)
    source_host: Mapped[str] = mapped_column(String(80), nullable=False)
    target_host: Mapped[str] = mapped_column(String(80), nullable=False)
    event_type: Mapped[str | None] = mapped_column(String(10))
    host_state_after: Mapped[str] = mapped_column(String(30), nullable=False)


# -------------------- Evaluation --------------------
class ExecutionMetrics(Base):
    __tablename__ = "execution_metrics"
    __table_args__ = {"schema": "evaluation"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    execution_id: Mapped[str] = mapped_column(ForeignKey("execution.executions.execution_id"), unique=True, nullable=False)
    detection_rate: Mapped[float] = mapped_column(Float, nullable=False)
    coverage: Mapped[float] = mapped_column(Float, nullable=False)
    ttd: Mapped[float | None] = mapped_column(Float)
    ttc: Mapped[float | None] = mapped_column(Float)
    hosts_compromised: Mapped[int] = mapped_column(Integer, nullable=False)
    hosts_impacted: Mapped[int] = mapped_column(Integer, nullable=False)
    hosts_preserved: Mapped[int] = mapped_column(Integer, nullable=False)
    hosts_isolated: Mapped[int] = mapped_column(Integer, nullable=False)
    segments_isolated: Mapped[int] = mapped_column(Integer, nullable=False)
    hosts_communication_interrupted: Mapped[int] = mapped_column(Integer, nullable=False)
    impact_before_detection: Mapped[int | None] = mapped_column(Integer)
    impact_before_containment: Mapped[int | None] = mapped_column(Integer)
    tp: Mapped[int | None] = mapped_column(Integer)
    fp: Mapped[int | None] = mapped_column(Integer)
    fn: Mapped[int | None] = mapped_column(Integer)
    tn: Mapped[int | None] = mapped_column(Integer)
