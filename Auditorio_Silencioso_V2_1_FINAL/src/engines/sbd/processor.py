from pathlib import Path
import pandas as pd
import json

def process_selected_rules(raw_csv: Path, output_json: Path):
    df = pd.read_csv(raw_csv)
    cols = ["sid", "rev", "action", "protocol", "src", "src_port",
            "direction", "dst", "dst_port", "msg", "classtype",
            "service", "metadata", "event_candidates", "body",
            "final_event", "final_reason"]
    selected = df[cols].copy()
    selected.to_json(output_json, orient="records", force_ascii=False, indent=2)
    return selected
