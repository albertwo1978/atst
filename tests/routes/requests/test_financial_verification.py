import pytest
from unittest.mock import MagicMock
from flask import url_for
import datetime

from atst.eda_client import MockEDAClient
from atst.routes.requests.financial_verification import (
    GetFinancialVerificationForm,
    UpdateFinancialVerification,
    SaveFinancialVerificationDraft,
)

from tests.mocks import MOCK_VALID_PE_ID
from tests.factories import RequestFactory, UserFactory, LegacyTaskOrderFactory
from atst.forms.exceptions import FormValidationError
from atst.domain.requests.financial_verification import (
    PENumberValidator,
    TaskOrderNumberValidator,
)
from atst.models.request_status_event import RequestStatus
from atst.models.attachment import Attachment
from atst.domain.requests.query import RequestsQuery


@pytest.fixture
def fv_data():
    return {
        "request-pe_id": "123",
        "task_order-number": MockEDAClient.MOCK_CONTRACT_NUMBER,
        "request-fname_co": "Contracting",
        "request-lname_co": "Officer",
        "request-email_co": "jane@mail.mil",
        "request-office_co": "WHS",
        "request-fname_cor": "Officer",
        "request-lname_cor": "Representative",
        "request-email_cor": "jane@mail.mil",
        "request-office_cor": "WHS",
        "request-uii_ids": "1234",
        "request-treasury_code": "00123456",
        "request-ba_code": "02A",
    }


@pytest.fixture
def e_fv_data(pdf_upload):
    return {
        "task_order-funding_type": "RDTE",
        "task_order-funding_type_other": "other",
        "task_order-expiration_date": "1/1/{}".format(datetime.date.today().year + 1),
        "task_order-clin_0001": "50000",
        "task_order-clin_0003": "13000",
        "task_order-clin_1001": "30000",
        "task_order-clin_1003": "7000",
        "task_order-clin_2001": "30000",
        "task_order-clin_2003": "7000",
        "task_order-pdf": pdf_upload,
    }


MANUAL_TO_NUMBER = "DCA10096D0051"


TrueValidator = MagicMock()
TrueValidator.validate = MagicMock(return_value=True)

FalseValidator = MagicMock()
FalseValidator.validate = MagicMock(return_value=False)


def test_update_fv(fv_data):
    request = RequestFactory.create()
    user = UserFactory.create()
    data = {**fv_data, "pe_id": MOCK_VALID_PE_ID}

    updated_request = UpdateFinancialVerification(
        TrueValidator, TrueValidator, user, request, data, is_extended=False
    ).execute()

    assert updated_request.is_pending_ccpo_approval


def test_update_fv_re_enter_pe_number(fv_data):
    request = RequestFactory.create()
    user = UserFactory.create()
    data = {**fv_data, "pe_id": "0101228M"}
    update_fv = UpdateFinancialVerification(
        PENumberValidator(), TrueValidator, user, request, data, is_extended=False
    )

    with pytest.raises(FormValidationError):
        update_fv.execute()
    updated_request = update_fv.execute()

    assert updated_request.is_pending_ccpo_approval


def test_update_fv_invalid_task_order_number(fv_data):
    request = RequestFactory.create()
    user = UserFactory.create()
    data = {**fv_data, "task_order-number": MANUAL_TO_NUMBER}
    update_fv = UpdateFinancialVerification(
        TrueValidator,
        TaskOrderNumberValidator(),
        user,
        request,
        data,
        is_extended=False,
    )

    with pytest.raises(FormValidationError):
        update_fv.execute()


def test_draft_without_pe_id(fv_data):
    request = RequestFactory.create()
    user = UserFactory.create()
    data = {"request-uii_ids": "1234"}
    assert SaveFinancialVerificationDraft(
        PENumberValidator(),
        TaskOrderNumberValidator(),
        user,
        request,
        data,
        is_extended=False,
    ).execute()


def test_update_fv_extended(fv_data, e_fv_data):
    request = RequestFactory.create()
    user = UserFactory.create()
    data = {**fv_data, **e_fv_data}
    update_fv = UpdateFinancialVerification(
        TrueValidator, TaskOrderNumberValidator(), user, request, data, is_extended=True
    )

    assert update_fv.execute()


def test_update_fv_extended_does_not_validate_task_order(fv_data, e_fv_data):
    request = RequestFactory.create()
    user = UserFactory.create()
    data = {**fv_data, **e_fv_data, "task_order-number": "abc123"}
    update_fv = UpdateFinancialVerification(
        TrueValidator, TaskOrderNumberValidator(), user, request, data, is_extended=True
    )

    assert update_fv.execute()


def test_update_fv_missing_extended_data(fv_data):
    request = RequestFactory.create()
    user = UserFactory.create()
    update_fv = UpdateFinancialVerification(
        TrueValidator,
        TaskOrderNumberValidator(),
        user,
        request,
        fv_data,
        is_extended=True,
    )

    with pytest.raises(FormValidationError):
        update_fv.execute()


def test_update_fv_submission(fv_data):
    request = RequestFactory.create()
    user = UserFactory.create()
    updated_request = UpdateFinancialVerification(
        TrueValidator, TrueValidator, user, request, fv_data
    ).execute()
    assert updated_request


def test_save_empty_draft():
    request = RequestFactory.create()
    user = UserFactory.create()
    save_draft = SaveFinancialVerificationDraft(
        TrueValidator, TrueValidator, user, request, {}, is_extended=False
    )

    assert save_draft.execute()


def test_save_draft_with_ba_code():
    request = RequestFactory.create()
    user = UserFactory.create()
    data = {"ba_code": "02A"}
    save_draft = SaveFinancialVerificationDraft(
        TrueValidator, TrueValidator, user, request, data, is_extended=False
    )

    assert save_draft.execute()


def test_save_draft_allows_invalid_data():
    request = RequestFactory.create()
    user = UserFactory.create()
    data = {
        "task_order-number": MANUAL_TO_NUMBER,
        "request-pe_id": "123",
        "request-ba_code": "a",
    }

    assert SaveFinancialVerificationDraft(
        PENumberValidator(),
        TaskOrderNumberValidator(),
        user,
        request,
        data,
        is_extended=True,
    ).execute()


def test_save_draft_and_then_submit():
    request = RequestFactory.create()
    user = UserFactory.create()
    data = {"ba_code": "02A"}
    updated_request = SaveFinancialVerificationDraft(
        TrueValidator, TrueValidator, user, request, data, is_extended=False
    ).execute()

    with pytest.raises(FormValidationError):
        UpdateFinancialVerification(
            TrueValidator, TrueValidator, user, updated_request, data
        ).execute()


def test_updated_request_has_pdf(fv_data, e_fv_data):
    request = RequestFactory.create()
    user = UserFactory.create()
    data = {**fv_data, **e_fv_data, "task_order-number": MANUAL_TO_NUMBER}
    updated_request = UpdateFinancialVerification(
        TrueValidator, TrueValidator, user, request, data, is_extended=True
    ).execute()
    assert updated_request.task_order.pdf


def test_can_save_draft_with_just_pdf(e_fv_data):
    request = RequestFactory.create()
    user = UserFactory.create()
    data = {"task_order-pdf": e_fv_data["task_order-pdf"]}
    SaveFinancialVerificationDraft(
        TrueValidator, TrueValidator, user, request, data, is_extended=True
    ).execute()

    form = GetFinancialVerificationForm(user, request, is_extended=True).execute()
    assert form.task_order.pdf


def test_task_order_info_present_in_extended_form(fv_data, e_fv_data):
    request = RequestFactory.create()
    user = UserFactory.create()
    data = {
        "task_order-clin_0001": "1",
        "task_order-number": fv_data["task_order-number"],
    }
    SaveFinancialVerificationDraft(
        TrueValidator, TrueValidator, user, request, data, is_extended=True
    ).execute()

    form = GetFinancialVerificationForm(user, request, is_extended=True).execute()
    assert form.task_order.clin_0001.data


def test_update_ignores_empty_values(fv_data, e_fv_data):
    request = RequestFactory.create()
    user = UserFactory.create()
    data = {**fv_data, **e_fv_data, "task_order-funding_type": ""}
    SaveFinancialVerificationDraft(
        TrueValidator, TrueValidator, user, request, data, is_extended=True
    ).execute()


def test_can_save_draft_with_funding_type(fv_data, e_fv_data):
    request = RequestFactory.create()
    user = UserFactory.create()
    data = {
        "task_order-number": fv_data["task_order-number"],
        "task_order-funding_type": e_fv_data["task_order-funding_type"],
    }
    updated_request = SaveFinancialVerificationDraft(
        TrueValidator, TrueValidator, user, request, data, is_extended=False
    ).execute()

    assert updated_request.task_order.funding_type


def test_update_fv_route(client, user_session, fv_data):
    user = UserFactory.create()
    request = RequestFactory.create(creator=user)
    user_session(user)
    response = client.post(
        url_for("requests.financial_verification", request_id=request.id),
        data=fv_data,
        follow_redirects=False,
    )

    assert response.status_code == 200


def test_save_fv_draft_route(client, user_session, fv_data):
    user = UserFactory.create()
    request = RequestFactory.create(creator=user)
    user_session(user)
    response = client.post(
        url_for("requests.save_financial_verification_draft", request_id=request.id),
        data=fv_data,
        follow_redirects=True,
    )

    assert response.status_code == 200


def test_get_fv_form_route(client, user_session, fv_data):
    user = UserFactory.create()
    request = RequestFactory.create(creator=user)
    user_session(user)
    response = client.get(
        url_for("requests.financial_verification", request_id=request.id),
        data=fv_data,
        follow_redirects=False,
    )

    assert response.status_code == 200


def test_manual_task_order_triggers_extended_form(
    client, user_session, fv_data, e_fv_data
):
    user = UserFactory.create()
    request = RequestFactory.create(creator=user)

    data = {**fv_data, **e_fv_data, "task_order-number": MANUAL_TO_NUMBER}

    UpdateFinancialVerification(
        TrueValidator, TrueValidator, user, request, data, is_extended=True
    ).execute()

    user_session(user)
    response = client.get(
        url_for("requests.financial_verification", request_id=request.id),
        data=fv_data,
        follow_redirects=False,
    )
    assert "extended" in response.headers["Location"]


def test_manual_to_does_not_trigger_approval(client, user_session, fv_data, e_fv_data):
    user = UserFactory.create()
    request = RequestFactory.create(creator=user)
    data = {
        **fv_data,
        **e_fv_data,
        "task_order-number": MANUAL_TO_NUMBER,
        "request-pe_id": "0101228N",
    }
    user_session(user)
    client.post(
        url_for(
            "requests.financial_verification", request_id=request.id, extended=True
        ),
        data=data,
        follow_redirects=True,
    )

    updated_request = RequestsQuery.get(request.id)
    assert updated_request.status != RequestStatus.APPROVED


def test_eda_task_order_does_trigger_approval(client, user_session, fv_data, e_fv_data):
    user = UserFactory.create()
    request = RequestFactory.create(creator=user)
    data = {
        **fv_data,
        **e_fv_data,
        "task_order-number": MockEDAClient.MOCK_CONTRACT_NUMBER,
        "request-pe_id": "0101228N",
    }
    user_session(user)
    client.post(
        url_for(
            "requests.financial_verification", request_id=request.id, extended=True
        ),
        data=data,
        follow_redirects=True,
    )

    updated_request = RequestsQuery.get(request.id)
    assert updated_request.status == RequestStatus.APPROVED


def test_attachment_on_non_extended_form(client, user_session, fv_data, e_fv_data):
    user = UserFactory.create()
    request = RequestFactory.create(creator=user)
    data = {
        **fv_data,
        **e_fv_data,
        "task_order-number": MockEDAClient.MOCK_CONTRACT_NUMBER,
        "request-pe_id": "0101228N",
    }
    user_session(user)
    client.post(
        url_for(
            "requests.financial_verification", request_id=request.id, extended=True
        ),
        data=data,
        follow_redirects=True,
    )

    response = client.get(
        url_for("requests.financial_verification", request_id=request.id)
    )

    assert response.status_code == 200


def test_task_order_number_persists_in_form(fv_data, e_fv_data):
    user = UserFactory.create()
    request = RequestFactory.create(creator=user)
    data = {
        **fv_data,
        "task_order-number": MANUAL_TO_NUMBER,
        "request-pe_id": "0101228N",
    }

    try:
        UpdateFinancialVerification(
            TrueValidator, FalseValidator, user, request, data, is_extended=False
        ).execute()
    except FormValidationError:
        pass

    form = GetFinancialVerificationForm(user, request, is_extended=True).execute()
    assert form.task_order.number.data == MANUAL_TO_NUMBER


def test_can_submit_once_to_details_are_entered(fv_data, e_fv_data):
    user = UserFactory.create()
    request = RequestFactory.create(creator=user)
    data = {
        **fv_data,
        "task_order-number": MANUAL_TO_NUMBER,
        "request-pe_id": "0101228N",
    }

    try:
        UpdateFinancialVerification(
            TrueValidator, FalseValidator, user, request, data, is_extended=False
        ).execute()
    except FormValidationError:
        pass

    data = {
        **fv_data,
        **e_fv_data,
        "task_order-number": MANUAL_TO_NUMBER,
        "request-pe_id": "0101228N",
    }
    assert UpdateFinancialVerification(
        TrueValidator, TrueValidator, user, request, data, is_extended=True
    ).execute()


def test_existing_task_order_with_pdf(fv_data, e_fv_data, client, user_session):
    # Use finver route to create initial TO #1, complete with PDF
    user = UserFactory.create()
    request = RequestFactory.create(creator=user)
    data = {**fv_data, **e_fv_data, "task_order-number": MANUAL_TO_NUMBER}
    UpdateFinancialVerification(
        TrueValidator, TaskOrderNumberValidator(), user, request, data, is_extended=True
    ).execute()

    # Save draft on a new finver form, but with same number as TO #1
    user = UserFactory.create()
    request = RequestFactory.create(creator=user)
    data = {"task_order-number": MANUAL_TO_NUMBER}
    SaveFinancialVerificationDraft(
        TrueValidator,
        TaskOrderNumberValidator(),
        user,
        request,
        data,
        is_extended=False,
    ).execute()

    # Get finver form
    user_session(user)
    response = client.get(
        url_for("requests.financial_verification", request_id=request.id),
        follow_redirects=True,
    )

    assert response.status_code == 200


def test_pdf_clearing(fv_data, e_fv_data, pdf_upload, pdf_upload2):
    user = UserFactory.create()
    request = RequestFactory.create(creator=user)
    data = {**fv_data, **e_fv_data, "task_order-pdf": pdf_upload}

    SaveFinancialVerificationDraft(
        TrueValidator, TrueValidator, user, request, data, is_extended=True
    ).execute()

    data = {**data, "task_order-pdf": pdf_upload2}
    UpdateFinancialVerification(
        TrueValidator, TrueValidator, user, request, data, is_extended=True
    ).execute()

    form = GetFinancialVerificationForm(user, request, is_extended=True).execute()
    assert form.task_order.pdf.data == pdf_upload2.filename


# TODO: This test manages an edge case for our current non-unique handling of
# task orders. Because two requests can reference the same task order but we
# only record one request ID on the PDF attachment, multiple task
# orders/requests reference the same task order but only one of them is noted
# in the related attachment entity. I have changed the handling in
# FinancialVerificationBase#_get_form to be more generous in how it finds the
# PDF filename and prepopulates the form data with that name.
def test_always_derives_pdf_filename(fv_data, e_fv_data, pdf_upload):
    user = UserFactory.create()
    request_one = RequestFactory.create(creator=user)
    attachment = Attachment.attach(
        pdf_upload, resource="task_order", resource_id=request_one.id
    )
    task_order = LegacyTaskOrderFactory.create(pdf=attachment)
    request_two = RequestFactory.create(creator=user, task_order=task_order)

    form_one = GetFinancialVerificationForm(
        user, request_one, is_extended=True
    ).execute()
    form_two = GetFinancialVerificationForm(
        user, request_two, is_extended=True
    ).execute()

    assert form_one.task_order.pdf.data == attachment.filename
    assert form_two.task_order.pdf.data == attachment.filename
