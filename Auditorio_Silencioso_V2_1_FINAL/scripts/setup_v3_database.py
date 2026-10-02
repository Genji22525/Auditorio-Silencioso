"""Create the clean PostgreSQL V3 database used by Auditório Silencioso V2.1."""
import os
import sys
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.common.config import settings
from src.persistence.repository import ensure_schema


def main():
    target_url = make_url(settings.database_url)
    database_name = target_url.database
    if not database_name:
        raise RuntimeError("DATABASE_URL precisa informar o nome do banco.")

    admin_url = make_url(os.getenv(
        "ADMIN_DATABASE_URL",
        target_url.set(database="postgres").render_as_string(hide_password=False),
    ))

    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT", pool_pre_ping=True)
    with admin_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": database_name},
        ).scalar()
        if not exists:
            safe_name = database_name.replace('"', '""')
            conn.exec_driver_sql(f'CREATE DATABASE "{safe_name}"')
            print(f"Banco criado: {database_name}")
        else:
            print(f"Banco já existe: {database_name}")
    admin_engine.dispose()

    ensure_schema()
    print("Schemas e tabelas V2.1 criados/verificados com sucesso.")
    print(f"DATABASE_URL: {settings.database_url}")
    print("Schemas: scenario, network, attack, execution, evaluation")


if __name__ == "__main__":
    main()
