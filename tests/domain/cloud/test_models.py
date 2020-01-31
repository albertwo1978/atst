import pytest

from pydantic import ValidationError

from atst.domain.csp.cloud.models import (
    AZURE_MGMNT_PATH,
    KeyVaultCredentials,
    ManagementGroupCSPPayload,
    ManagementGroupCSPResponse,
)


def test_ManagementGroupCSPPayload_management_group_name():
    # supplies management_group_name when absent
    payload = ManagementGroupCSPPayload(
        tenant_id="any-old-id",
        display_name="Council of Naboo",
        parent_id="Galactic_Senate",
    )
    assert payload.management_group_name
    # validates management_group_name
    with pytest.raises(ValidationError):
        payload = ManagementGroupCSPPayload(
            tenant_id="any-old-id",
            management_group_name="council of Naboo 1%^&",
            display_name="Council of Naboo",
            parent_id="Galactic_Senate",
        )
    # shortens management_group_name to fit
    name = "council_of_naboo".ljust(95, "1")

    assert len(name) > 90
    payload = ManagementGroupCSPPayload(
        tenant_id="any-old-id",
        management_group_name=name,
        display_name="Council of Naboo",
        parent_id="Galactic_Senate",
    )
    assert len(payload.management_group_name) == 90


def test_ManagementGroupCSPPayload_display_name():
    # shortens display_name to fit
    name = "Council of Naboo".ljust(95, "1")
    assert len(name) > 90
    payload = ManagementGroupCSPPayload(
        tenant_id="any-old-id", display_name=name, parent_id="Galactic_Senate"
    )
    assert len(payload.display_name) == 90


def test_ManagementGroupCSPPayload_parent_id():
    full_path = f"{AZURE_MGMNT_PATH}Galactic_Senate"
    # adds full path
    payload = ManagementGroupCSPPayload(
        tenant_id="any-old-id",
        display_name="Council of Naboo",
        parent_id="Galactic_Senate",
    )
    assert payload.parent_id == full_path
    # keeps full path
    payload = ManagementGroupCSPPayload(
        tenant_id="any-old-id", display_name="Council of Naboo", parent_id=full_path
    )
    assert payload.parent_id == full_path


def test_ManagementGroupCSPResponse_id():
    full_id = "/path/to/naboo-123"
    response = ManagementGroupCSPResponse(
        **{"id": "/path/to/naboo-123", "other": "stuff"}
    )
    assert response.id == full_id


def test_KeyVaultCredentials_enforce_admin_creds():
    with pytest.raises(ValidationError):
        KeyVaultCredentials(tenant_id="an id", tenant_admin_username="C3PO")
    assert KeyVaultCredentials(
        tenant_id="an id",
        tenant_admin_username="C3PO",
        tenant_admin_password="beep boop",
    )


def test_KeyVaultCredentials_enforce_sp_creds():
    with pytest.raises(ValidationError):
        KeyVaultCredentials(tenant_id="an id", tenant_sp_client_id="C3PO")
    assert KeyVaultCredentials(
        tenant_id="an id", tenant_sp_client_id="C3PO", tenant_sp_key="beep boop"
    )


def test_KeyVaultCredentials_enforce_root_creds():
    with pytest.raises(ValidationError):
        KeyVaultCredentials(root_tenant_id="an id", root_sp_client_id="C3PO")
    assert KeyVaultCredentials(
        root_tenant_id="an id", root_sp_client_id="C3PO", root_sp_key="beep boop"
    )
