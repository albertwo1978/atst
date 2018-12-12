import pytest

from atst.domain.exceptions import NotFoundError
from atst.domain.task_orders import TaskOrders
from atst.eda_client import MockEDAClient

from tests.factories import LegacyTaskOrderFactory


def test_can_get_task_order():
    new_to = LegacyTaskOrderFactory.create(number="0101969F")
    to = TaskOrders.get(new_to.number)

    assert to.id == to.id


def test_nonexistent_task_order_raises_without_client():
    with pytest.raises(NotFoundError):
        TaskOrders.get("some fake number")


def test_nonexistent_task_order_raises_with_client(monkeypatch):
    monkeypatch.setattr(
        "atst.domain.task_orders.TaskOrders._client", lambda: MockEDAClient()
    )
    with pytest.raises(NotFoundError):
        TaskOrders.get("some other fake numer")
