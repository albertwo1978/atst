"""add additional task order fields

Revision ID: 875e4b8a05fc
Revises: f36f130622b9
Create Date: 2018-08-21 15:52:46.636928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '875e4b8a05fc'
down_revision = 'f36f130622b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task_order', sa.Column('clin_0001', sa.Integer(), nullable=True))
    op.add_column('task_order', sa.Column('clin_0003', sa.Integer(), nullable=True))
    op.add_column('task_order', sa.Column('clin_1001', sa.Integer(), nullable=True))
    op.add_column('task_order', sa.Column('clin_1003', sa.Integer(), nullable=True))
    op.add_column('task_order', sa.Column('clin_2001', sa.Integer(), nullable=True))
    op.add_column('task_order', sa.Column('clin_2003', sa.Integer(), nullable=True))
    op.add_column('task_order', sa.Column('funding_type', sa.String(), nullable=True))
    op.add_column('task_order', sa.Column('funding_type_other', sa.String(), nullable=True))
    op.add_column('task_order', sa.Column('source', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task_order', 'source')
    op.drop_column('task_order', 'funding_type_other')
    op.drop_column('task_order', 'funding_type')
    op.drop_column('task_order', 'clin_2003')
    op.drop_column('task_order', 'clin_2001')
    op.drop_column('task_order', 'clin_1003')
    op.drop_column('task_order', 'clin_1001')
    op.drop_column('task_order', 'clin_0003')
    op.drop_column('task_order', 'clin_0001')
    # ### end Alembic commands ###
