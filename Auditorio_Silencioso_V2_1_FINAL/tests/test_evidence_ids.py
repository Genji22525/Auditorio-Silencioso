from src.common.models import Event
from src.evidence.builder import build_evidence


def test_evidence_ids_are_unique_and_sequential():
    events = [
        Event("EXE-CTI-000001-EV001", "EXE-CTI-000001", "E01", 8.0, "WS-001", "SRV-001", True),
        Event("EXE-CTI-000001-EV002", "EXE-CTI-000001", "E02", 14.0, "WS-001", "SRV-001", True),
        Event("EXE-CTI-000001-EV003", "EXE-CTI-000001", "E03", 19.0, "WS-001", "SRV-001", True),
    ]
    evidence = [build_evidence("EXE-CTI-000001", event, i) for i, event in enumerate(events, 1)]
    assert [item.evidence_id for item in evidence] == [
        "EXE-CTI-000001-OBS001",
        "EXE-CTI-000001-OBS002",
        "EXE-CTI-000001-OBS003",
    ]
    assert len({item.evidence_id for item in evidence}) == len(evidence)
