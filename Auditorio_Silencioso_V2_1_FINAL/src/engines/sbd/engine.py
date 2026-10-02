from src.common.models import Detection, Evidence, ResponseAction

class SBDEngine:
    name = "SBD"

    def __init__(self, rules):
        self.rules = rules

    def inspect(self, evidence: Evidence) -> Detection | None:
        # Faithful abstraction: selected rule mappings determine whether
        # a fixed signature can match the observable event representation.
        matches = [
            r for r in self.rules
            if str(r.get("final_event")) == evidence.event_type
        ]
        if not matches:
            return None
        # The event-to-rule representation is intentionally explicit in this V2
        # baseline; no CTI knowledge or Ground Truth is consulted.
        return Detection(
            self.name, True, evidence.event_id, evidence.timestamp,
            f"fixed signature match ({len(matches)} selected rules mapped to {evidence.event_type})",
            [evidence.evidence_id]
        )

    def response(self, detection: Detection, host: str) -> ResponseAction:
        return ResponseAction(self.name, "alert", detection.timestamp, host,
                              "selected signature semantics: alert")
