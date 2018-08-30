"""add request revision

Revision ID: 04fe150da553
Revises: 2c2a2af465d3
Create Date: 2018-08-30 13:28:16.928946

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '04fe150da553'
down_revision = '2c2a2af465d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('request_revisions',
    sa.Column('time_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('time_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('request_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('am_poc', sa.Boolean(), nullable=True),
    sa.Column('dodid_poc', sa.String(), nullable=True),
    sa.Column('email_poc', sa.String(), nullable=True),
    sa.Column('fname_poc', sa.String(), nullable=True),
    sa.Column('lname_poc', sa.String(), nullable=True),
    sa.Column('jedi_usage', sa.String(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('cloud_native', sa.Boolean(), nullable=True),
    sa.Column('dollar_value', sa.Integer(), nullable=True),
    sa.Column('dod_component', sa.String(), nullable=True),
    sa.Column('data_transfers', sa.String(), nullable=True),
    sa.Column('expected_completion_date', sa.String(), nullable=True),
    sa.Column('jedi_migration', sa.Boolean(), nullable=True),
    sa.Column('num_software_systems', sa.Integer(), nullable=True),
    sa.Column('number_user_sessions', sa.Integer(), nullable=True),
    sa.Column('average_daily_traffic', sa.Integer(), nullable=True),
    sa.Column('engineering_assessment', sa.Boolean(), nullable=True),
    sa.Column('technical_support_team', sa.Boolean(), nullable=True),
    sa.Column('estimated_monthly_spend', sa.Integer(), nullable=True),
    sa.Column('average_daily_traffic_gb', sa.Integer(), nullable=True),
    sa.Column('rationalization_software_systems', sa.Boolean(), nullable=True),
    sa.Column('organization_providing_assistance', sa.String(), nullable=True),
    sa.Column('citizenship', sa.String(), nullable=True),
    sa.Column('designation', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('email_request', sa.String(), nullable=True),
    sa.Column('fname_request', sa.String(), nullable=True),
    sa.Column('lname_request', sa.String(), nullable=True),
    sa.Column('service_branch', sa.String(), nullable=True),
    sa.Column('date_latest_training', sa.Date(), nullable=True),
    sa.Column('pe_id', sa.String(), nullable=True),
    sa.Column('task_order_number', sa.String(), nullable=True),
    sa.Column('fname_co', sa.String(), nullable=True),
    sa.Column('lname_co', sa.String(), nullable=True),
    sa.Column('email_co', sa.String(), nullable=True),
    sa.Column('office_co', sa.String(), nullable=True),
    sa.Column('fname_cor', sa.String(), nullable=True),
    sa.Column('lname_cor', sa.String(), nullable=True),
    sa.Column('email_cor', sa.String(), nullable=True),
    sa.Column('office_cor', sa.String(), nullable=True),
    sa.Column('uii_ids', sa.String(), nullable=True),
    sa.Column('treasury_code', sa.String(), nullable=True),
    sa.Column('ba_code', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['request_id'], ['requests.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('request_revisions')
    # ### end Alembic commands ###
