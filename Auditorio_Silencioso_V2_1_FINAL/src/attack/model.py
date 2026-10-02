from src.common.models import AttackAction

def build_attack() -> list[AttackAction]:
    # Strategy only: actions/attempts. It does not query or adapt to engines.
    return [
        AttackAction("A01", "E01", "WS-001", "SRV-001", 0.90, 8),
        AttackAction("A02", "E02", "WS-001", "SRV-001", 0.85, 6),
        AttackAction("A03", "E03", "WS-001", "SRV-001", 0.80, 5),
        AttackAction("A04", "E04", "SRV-001", "WS-002", 0.70, 9),
        AttackAction("A05", "E04", "SRV-001", "SRV-002", 0.55, 9),
        AttackAction("A06", "E05", "SRV-001", "SRV-001", 0.65, 10),
        AttackAction("A07", "E04", "SRV-001", "ADM-001", 0.40, 9),
        AttackAction("A08", "E05", "ADM-001", "ADM-001", 0.45, 10),
    ]
