"""Add time column to Task

Revision ID: 1f784b19ef86
Revises: 2ab9130f0223
Create Date: 2025-09-14 10:04:15.511896
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '1f784b19ef86'
down_revision = '2ab9130f0223'
branch_labels = None
depends_on = None

def upgrade():
    """Add 'time' column as TIME type for Task."""
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', sa.Time(), nullable=True))
        batch_op.create_index(batch_op.f('ix_task_due_date'), ['due_date'], unique=False)
        batch_op.create_index(batch_op.f('ix_task_time'), ['time'], unique=False)
        batch_op.create_index(batch_op.f('ix_task_user_id'), ['user_id'], unique=False)

def downgrade():
    """Remove 'time' column safely."""
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_task_user_id'))
        batch_op.drop_index(batch_op.f('ix_task_time'))
        batch_op.drop_index(batch_op.f('ix_task_due_date'))
        batch_op.drop_column('time')
