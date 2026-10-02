"""Analyze the definitive paired experiment without producing an artificial score."""
import csv, json, statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
IN=ROOT/"results/experiment/executions.csv"
OUT=ROOT/"results/experiment/analysis.json"

def vals(rows,k): return [float(r[k]) for r in rows if r.get(k) not in (None,"","nan")]

def main():
    rows=list(csv.DictReader(IN.open(encoding="utf-8")))
    if len(rows)!=60: raise RuntimeError(f"Esperadas 60 execuções; encontradas {len(rows)}")
    by={e:[r for r in rows if r["engine"]==e] for e in ("CTI","SBD")}
    summary={}
    for e,rs in by.items():
        summary[e]={"n":len(rs)}
        for k in ("detection_rate","coverage","ttd","ttc","hosts_compromised","hosts_impacted","hosts_preserved","hosts_isolated","impact_before_detection","impact_before_containment"):
            v=vals(rs,k); summary[e][k]={"mean":statistics.mean(v) if v else None,"median":statistics.median(v) if v else None,"stdev":statistics.stdev(v) if len(v)>1 else None,"n":len(v)}
    paired=[]
    for seed in range(2,32):
        c=next(r for r in by["CTI"] if int(r["seed"])==seed); s=next(r for r in by["SBD"] if int(r["seed"])==seed)
        paired.append({"seed":seed,"ttd_difference_cti_minus_sbd":float(c["ttd"])-float(s["ttd"]),"hosts_impacted_difference_cti_minus_sbd":int(c["hosts_impacted"])-int(s["hosts_impacted"]),"hosts_compromised_difference_cti_minus_sbd":int(c["hosts_compromised"])-int(s["hosts_compromised"])})
    out={"experiment":{"seeds":[2,31],"paired_executions":30,"total_executions":60},"summary":summary,"paired_differences":paired,"interpretation_note":"Diferenças são descritivas e não constituem ranking ou score agregado."}
    OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Análise salva em {OUT}")

if __name__=="__main__": main()
