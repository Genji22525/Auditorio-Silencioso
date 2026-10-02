"""Preflight checks before the definitive experiment."""
import json, sys
from pathlib import Path
from sqlalchemy import text
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.common.config import settings
from src.persistence.database import get_engine

def main():
    cti=ROOT/"data/processed/cti/cti_operational_r1.json"
    sbd=ROOT/"data/processed/sbd/selected_rules.json"
    if not cti.exists(): raise RuntimeError("CTI operacional ausente. Rode scripts/finalize_cti.py")
    if not sbd.exists(): raise RuntimeError("SBD selecionado ausente.")
    cti_n=len(json.loads(cti.read_text(encoding="utf-8"))); sbd_n=len(json.loads(sbd.read_text(encoding="utf-8")))
    if cti_n != 6: raise RuntimeError(f"CTI R1 esperado=6; encontrado={cti_n}")
    if sbd_n != 1191: raise RuntimeError(f"SBD esperado=1191; encontrado={sbd_n}")
    with get_engine().connect() as conn:
        db=conn.execute(text("SELECT current_database()" )).scalar()
        if db != "auditorio_silencioso_v3": raise RuntimeError(f"Banco incorreto: {db}. Esperado auditorio_silencioso_v3")
        schemas=conn.execute(text("SELECT schema_name FROM information_schema.schemata WHERE schema_name IN ('scenario','network','attack','execution','evaluation') ORDER BY schema_name")).scalars().all()
    if len(schemas)!=5: raise RuntimeError(f"Schemas V2.1 incompletos: {schemas}")
    print(f"OK database={db}")
    print(f"OK CTI_R1={cti_n}")
    print(f"OK SBD_rules={sbd_n}")
    print(f"OK schemas={schemas}")

if __name__=="__main__": main()
