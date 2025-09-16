"""Convert Task.time to DateTime safely

Revision ID: 85dd82f881bc
Revises: dbc1f8ba6c50
Create Date: 2025-09-15 15:00:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '85dd82f881bc'
down_revision = 'dbc1f8ba6c50'
branch_labels = None
depends_on = None


def upgrade():
    """Convert Task.time from TIME to DateTime using fixed date"""
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.alter_column(
            'time',
            existing_type=postgresql.TIME(),
            type_=sa.DateTime(),
            existing_nullable=True,
            postgresql_using="('2000-01-01 ' || time)::timestamp"
        )


def downgrade():
    """Revert Task.time from DateTime back to TIME"""
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.alter_column(
            'time',
            existing_type=sa.DateTime(),
            type_=postgresql.TIME(),
            existing_nullable=True,
            postgresql_using="time(time)"
        )
