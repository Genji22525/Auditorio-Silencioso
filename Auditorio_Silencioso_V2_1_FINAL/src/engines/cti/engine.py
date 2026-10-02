from __future__ import annotations

import json
from pathlib import Path

from src.common.models import Detection, Evidence, ResponseAction


# Explicit experimental taxonomy: the CTI corpus contains ATT&CK/TTP descriptions,
# while the simulator exposes five observable behavioral event classes. This mapping
# is a model boundary, not an enrichment of the source feed.
TTP_EVENT_MAP = {
    "E01": {"T1190", "T1133", "T1078", "T1566", "T1021.001"},
    "E02": {"T1059.001", "T1543.003", "T1547.001", "T1562.001"},
    "E03": {"T1016", "T1082", "T1018", "T1057", "T1083", "T1482", "T1069.001", "T1069.002"},
    "E04": {"T1021.001", "T1078", "T1219", "T1090", "T1537"},
    "E05": {"T1486", "T1490"},
}


class CTIEngine:
    name = "CTI"

    def __init__(self, knowledge_path: Path | None = None):
        if knowledge_path is None:
            knowledge_path = Path(__file__).resolve().parents[3] / "data/processed/cti/cti_operational_r1.json"
        self.knowledge_path = knowledge_path
        self.records = self._load_records(knowledge_path)
        self.knowledge = self._build_knowledge(self.records)

    @staticmethod
    def _load_records(path: Path) -> list[dict]:
        if not path.exists():
            raise FileNotFoundError(f"Dataset CTI operacional não encontrado: {path}")
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list) or not data:
            raise ValueError("Dataset CTI operacional vazio ou inválido.")
        return data

    @staticmethod
    def _build_knowledge(records: list[dict]) -> dict[str, dict]:
        tags = [tag for record in records for tag in record.get("Tag", [])]
        tag_text = " | ".join(t.get("name", "") if isinstance(t, dict) else str(t) for t in tags)
        supported = {}
        for event_type, techniques in TTP_EVENT_MAP.items():
            matched = [t for t in techniques if t in tag_text]
            supported[event_type] = {"relevance": len(matched) / max(len(techniques), 1), "matched_ttp": matched}
        # Ensure ransomware impact knowledge is represented when the selected corpus
        # explicitly contains T1486/T1490 or ransomware records.
        return supported

    def inspect(self, evidence: Evidence, observed_history: list[Evidence]) -> Detection | None:
        # Only previously observed evidence is considered. Ground Truth and future
        # events are never consulted.
        prior_relevant = [
            item for item in observed_history
            if item.event_type in self.knowledge and self.knowledge[item.event_type]["relevance"] > 0
        ]
        current = self.knowledge.get(evidence.event_type, {})
        if not current or current.get("relevance", 0) <= 0:
            return None

        if evidence.event_type == "E04" and len(prior_relevant) >= 2:
            return Detection(
                self.name, True, evidence.event_id, evidence.timestamp,
                f"CTI correlation: prior evidence + temporal relationship; R1 corpus support={current['relevance']:.2f}",
                [evidence.evidence_id],
            )
        if evidence.event_type == "E05" and prior_relevant:
            return Detection(
                self.name, True, evidence.event_id, evidence.timestamp,
                f"CTI correlation: impact evidence + prior observations; R1 corpus support={current['relevance']:.2f}",
                [evidence.evidence_id],
            )
        return None

    def response(self, detection: Detection, host: str) -> ResponseAction:
        return ResponseAction(
            self.name, "host_isolate", detection.timestamp + 4, host,
            "predefined experimental CTI containment policy",
        )
