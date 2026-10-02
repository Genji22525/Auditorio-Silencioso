"""Finalize the CTI corpus from the preserved CIRCL/MISP raw manifest.

Selection is deliberately transparent: 2024-2026 is the candidate window;
R1 is operational ransomware intelligence, R2 contextual ransomware intelligence,
and R3 is excluded from the operational corpus.
"""
import csv, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/"data/raw/cti/misp_circl/manifest.json"
OUT=ROOT/"data/processed/cti"


def classify(info,tags):
    text=(info+" "+" ".join(tags)).lower()
    ransomware="ransomware" in text or "ransom" in text
    ttp=[t for t in tags if "mitre-attack-pattern" in t or "attack-pattern" in t]
    if not ransomware:
        return "R3","Fora do foco operacional de ransomware; não há evidência suficiente no manifest de relevância direta para a campanha simulada.",len(ttp)
    if "salesforce gainsight" in info.lower():
        return "R2","Contexto relevante de incidente/ransomware, mas foco principal em comprometimento de identidade/cloud e baixa certeza registrada; não é necessário ao núcleo operacional.",len(ttp)
    if "major payment disruption" in info.lower():
        return "R2","Incidente de ransomware contextual com baixa certeza registrada e sem TTPs estruturados no manifest processado.",len(ttp)
    if "datacarry" in info.lower():
        return "R2","Ransomware com TTPs estruturados, porém com certeza 50 no manifest; mantido como contexto e não como núcleo operacional.",len(ttp)
    return "R1","Ransomware diretamente relevante e operacionalmente estruturado, com TTPs/indicadores ou contexto técnico suficiente para alimentar o conhecimento prévio experimental.",len(ttp)


def main():
    data=json.loads(RAW.read_text(encoding="utf-8"))
    audit=[]; selected=[]
    for uid,event in data.items():
        date=event.get("date") or ""
        if date[:4] not in {"2024","2025","2026"}: continue
        info=event.get("info") or ""
        tags=[t.get("name","") for t in event.get("Tag",[])]
        cls,reason,ttp_count=classify(info,tags)
        row={"event_uuid":uid,"date":date,"info":info,"classification":cls,"ttp_tag_count":ttp_count,"tags":tags,"reason":reason,"source":"CIRCL OSINT / MISP"}
        audit.append(row)
        if cls=="R1": selected.append({**event,"event_uuid":uid,"source":"CIRCL OSINT / MISP","classification":"R1","selection_reason":reason})
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"cti_selection_audit.json").write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding="utf-8")
    with (OUT/"cti_selection_audit.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=["event_uuid","date","info","classification","ttp_tag_count","tags","reason","source"]); w.writeheader()
        for row in audit:
            row=dict(row); row["tags"]=" | ".join(row["tags"]); w.writerow(row)
    (OUT/"cti_operational_r1.json").write_text(json.dumps(selected,ensure_ascii=False,indent=2),encoding="utf-8")
    summary={"source":"CIRCL OSINT / MISP","temporal_scope":"2024-2026","manifest_records":len(data),"candidates_2024_2026":len(audit),"R1_operational":sum(r["classification"]=="R1" for r in audit),"R2_contextual":sum(r["classification"]=="R2" for r in audit),"R3_excluded":sum(r["classification"]=="R3" for r in audit),"R1_event_uuids":[r["event_uuid"] for r in selected],"note":"The classification is an explicit selection layer; no source IOC/TTP content was fabricated or enriched."}
    (OUT/"cti_selection_summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
