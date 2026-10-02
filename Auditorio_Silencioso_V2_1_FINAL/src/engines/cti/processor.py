from pathlib import Path
import json

def process_manifest(raw_path: Path, output_path: Path):
    data = json.loads(raw_path.read_text(encoding="utf-8"))
    records = []
    for event_uuid, event in data.items():
        records.append({
            "event_uuid": event_uuid,
            "date": event.get("date"),
            "info": event.get("info"),
            "analysis": event.get("analysis"),
            "threat_level_id": event.get("threat_level_id"),
            "tags": [t.get("name") for t in event.get("Tag", [])],
            "source": "CIRCL OSINT / MISP",
        })
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return records
