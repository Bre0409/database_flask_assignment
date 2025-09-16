"""Replace day with due_date in Task

Revision ID: 2ab9130f0223
Revises: 982b58d47463
Create Date: 2025-09-07 22:31:57.821107
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '2ab9130f0223'
down_revision = '982b58d47463'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('due_date', sa.Date(), nullable=False))
        batch_op.drop_column('day')

def downgrade():
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('day', sa.VARCHAR(length=50), nullable=False))
        batch_op.drop_column('due_date')
