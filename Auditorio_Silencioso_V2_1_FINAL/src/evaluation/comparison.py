def aggregate(rows):
    if not rows:
        return {}
    engines = sorted({r["engine"] for r in rows})
    out = {}
    for engine in engines:
        subset = [r for r in rows if r["engine"] == engine]
        def mean(key):
            vals = [r[key] for r in subset if r.get(key) is not None]
            return sum(vals) / len(vals) if vals else None
        out[engine] = {
            "executions": len(subset),
            "detection_rate": mean("detection_rate"),
            "coverage": mean("coverage"),
            "ttd": mean("ttd"),
            "ttc": mean("ttc"),
            "hosts_compromised": mean("hosts_compromised"),
            "hosts_impacted": mean("hosts_impacted"),
            "hosts_preserved": mean("hosts_preserved"),
            "hosts_isolated": mean("hosts_isolated"),
            "segments_isolated": mean("segments_isolated"),
            "hosts_communication_interrupted": mean("hosts_communication_interrupted"),
        }
    return out
