from src.common.models import Scenario


def build_scenario(seed: int) -> Scenario:
    # Corporate-like deterministic baseline.
    # The scenario is structural and shared across experimental executions.
    # The execution seed is kept as an argument for API compatibility, but
    # experimental variability is generated in the execution layer.

    return Scenario(
        scenario_id="SCN-000001",
        name="Corporate Baseline",
        version="2.1",
        seed=1,

        segments=[
            {"id": "SEG-USER", "name": "User Network"},
            {"id": "SEG-SRV", "name": "Server Network"},
            {"id": "SEG-ADMIN", "name": "Administration"},
        ],

        hosts=[
            {
                "hostname": "WS-001",
                "ip": "10.10.10.10",
                "segment": "SEG-USER",
                "type": "workstation",
                "os": "Windows",
                "criticality": "medium",
            },
            {
                "hostname": "WS-002",
                "ip": "10.10.10.11",
                "segment": "SEG-USER",
                "type": "workstation",
                "os": "Windows",
                "criticality": "medium",
            },
            {
                "hostname": "SRV-001",
                "ip": "10.10.20.10",
                "segment": "SEG-SRV",
                "type": "server",
                "os": "Windows Server",
                "criticality": "high",
            },
            {
                "hostname": "SRV-002",
                "ip": "10.10.20.11",
                "segment": "SEG-SRV",
                "type": "server",
                "os": "Linux",
                "criticality": "high",
            },
            {
                "hostname": "ADM-001",
                "ip": "10.10.30.10",
                "segment": "SEG-ADMIN",
                "type": "admin",
                "os": "Windows",
                "criticality": "critical",
            },
        ],

        services=[
            {
                "name": "SMB",
                "port": 445,
                "protocol": "tcp",
            },
            {
                "name": "RDP",
                "port": 3389,
                "protocol": "tcp",
            },
            {
                "name": "DNS",
                "port": 53,
                "protocol": "udp",
            },
        ],

        vulnerabilities=[
            {
                "cve": "CVE-2021-44228",
                "name": "Example vulnerability",
                "host": "SRV-001",
            },
            {
                "cve": "CVE-2019-0708",
                "name": "Example remote service weakness",
                "host": "WS-002",
            },
        ],
    )