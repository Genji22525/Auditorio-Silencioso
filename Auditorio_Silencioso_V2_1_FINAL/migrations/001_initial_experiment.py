"""Initial complete database for Auditório Silencioso V2.1 on the clean V3 PostgreSQL database.

Creates the clean V2.1 schemas: scenario, network, attack, execution and evaluation.
No objects from the previous project database are required.
"""
from alembic import op

revision = "001_initial_v3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    from src.persistence.repository import ensure_schema
    ensure_schema()


def downgrade():
    op.execute("DROP SCHEMA IF EXISTS evaluation CASCADE")
    op.execute("DROP SCHEMA IF EXISTS execution CASCADE")
    op.execute("DROP SCHEMA IF EXISTS attack CASCADE")
    op.execute("DROP SCHEMA IF EXISTS network CASCADE")
    op.execute("DROP SCHEMA IF EXISTS scenario CASCADE")
