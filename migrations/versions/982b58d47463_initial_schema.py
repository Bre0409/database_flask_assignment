"""Initial schema

Revision ID: 982b58d47463
Revises: 
Create Date: 2025-09-02 16:30:10.746361
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '982b58d47463'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.Column('first_name', sa.String(length=150), nullable=False),
        sa.Column('password', sa.String(length=256), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_table(
        'event',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('text', sa.String(length=300), nullable=False),
        sa.Column('day', sa.String(length=50), nullable=False),
        sa.Column('completed', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('task')
    op.drop_table('event')
    op.drop_table('user')
