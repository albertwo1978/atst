"""remove revisions body column

Revision ID: 090e1bd0d7ce
Revises: a903ebe91ad5
Create Date: 2018-08-31 12:08:52.376027

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import postgresql

from atst.models.request import Request
from atst.utils import deep_merge
from atst.domain.requests import create_revision_from_request_body
from atst.domain.task_orders import TaskOrders


# revision identifiers, used by Alembic.
revision = '090e1bd0d7ce'
down_revision = 'a903ebe91ad5'
branch_labels = None
depends_on = None


def delete_two_deep(body, key1, key2):
    result = body.get(key1, {}).get(key2)
    if result:
        del(body[key1][key2])

    return body


TASK_ORDER_DATA = TaskOrders.TASK_ORDER_DATA + ["task_order_id", "csrf_token"]

def create_revision(body):
    financials = body.get("financial_verification")
    if financials:
        for column in TASK_ORDER_DATA:
            if column in financials:
                del(financials[column])

    return create_revision_from_request_body(body)


def massaged_revision(body):
    try:
        return create_revision(body)
    except ValueError:
        # some of the data on staging has out-of-range dates like "02/29/2019";
        # we don't know how to coerce them to valid dates, so we remove those
        # fields.
        body = delete_two_deep(body, "details_of_use", "start_date")
        body = delete_two_deep(body, "information_about_you", "date_latest_training")

        return create_revision(body)

from uuid import UUID

def upgrade():
    Session = sessionmaker(bind=op.get_bind())
    session = Session()
    for request in session.query(Request).all():
        (body,) = session.execute("SELECT body from requests WHERE id='{}'".format(request.id)).fetchone()

        revision = massaged_revision(body)
        request.revisions.append(revision)

        session.add(revision)
        session.add(request)

    session.commit()

    op.drop_column('requests', 'body')


def downgrade():
    op.add_column('requests', sa.Column('body', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True))
