from typing import Dict, List, Optional

from pydantic import BaseModel, validator

from atst.utils import snake_to_camel


class AliasModel(BaseModel):
    """
    This provides automatic camel <-> snake conversion for serializing to/from json
    You can override the alias generation in subclasses by providing a Config that defines
    a fields property with a dict mapping variables to their cast names, for cases like:
    * some_url:someURL
    * user_object_id:objectId
    """

    class Config:
        alias_generator = snake_to_camel
        allow_population_by_field_name = True


class BaseCSPPayload(AliasModel):
    tenant_id: str


class TenantCSPPayload(AliasModel):
    user_id: str
    password: Optional[str]
    domain_name: str
    first_name: str
    last_name: str
    country_code: str
    password_recovery_email_address: str


class TenantCSPResult(AliasModel):
    user_id: str
    tenant_id: str
    user_object_id: str

    tenant_admin_username: Optional[str]
    tenant_admin_password: Optional[str]

    class Config:
        fields = {
            "user_object_id": "objectId",
        }

    def dict(self, *args, **kwargs):
        exclude = {"tenant_admin_username", "tenant_admin_password"}
        if "exclude" not in kwargs:
            kwargs["exclude"] = exclude
        else:
            kwargs["exclude"].update(exclude)

        return super().dict(*args, **kwargs)

    def get_creds(self):
        return {
            "tenant_admin_username": self.tenant_admin_username,
            "tenant_admin_password": self.tenant_admin_password,
            "tenant_id": self.tenant_id,
        }


class BillingProfileAddress(AliasModel):
    company_name: str
    address_line_1: str
    city: str
    region: str
    country: str
    postal_code: str


class BillingProfileCLINBudget(AliasModel):
    clin_budget: Dict
    """
        "clinBudget": {
            "amount": 0,
            "startDate": "2019-12-18T16:47:40.909Z",
            "endDate": "2019-12-18T16:47:40.909Z",
            "externalReferenceId": "string"
        }
    """


class BillingProfileCreationCSPPayload(BaseCSPPayload):
    tenant_id: str
    billing_profile_display_name: str
    billing_account_name: str
    enabled_azure_plans: Optional[List[str]]
    address: BillingProfileAddress

    @validator("enabled_azure_plans", pre=True, always=True)
    def default_enabled_azure_plans(cls, v):
        """
        Normally you'd implement this by setting the field with a value of:
            dataclasses.field(default_factory=list)
        but that prevents the object from being correctly pickled, so instead we need
        to rely on a validator to ensure this has an empty value when not specified
        """
        return v or []

    class Config:
        fields = {"billing_profile_display_name": "displayName"}


class BillingProfileCreationCSPResult(AliasModel):
    billing_profile_verify_url: str
    billing_profile_retry_after: int

    class Config:
        fields = {
            "billing_profile_verify_url": "Location",
            "billing_profile_retry_after": "Retry-After",
        }


class BillingProfileVerificationCSPPayload(BaseCSPPayload):
    billing_profile_verify_url: str


class BillingInvoiceSection(AliasModel):
    invoice_section_id: str
    invoice_section_name: str

    class Config:
        fields = {"invoice_section_id": "id", "invoice_section_name": "name"}


class BillingProfileProperties(AliasModel):
    address: BillingProfileAddress
    billing_profile_display_name: str
    invoice_sections: List[BillingInvoiceSection]

    class Config:
        fields = {"billing_profile_display_name": "displayName"}


class BillingProfileVerificationCSPResult(AliasModel):
    billing_profile_id: str
    billing_profile_name: str
    billing_profile_properties: BillingProfileProperties

    class Config:
        fields = {
            "billing_profile_id": "id",
            "billing_profile_name": "name",
            "billing_profile_properties": "properties",
        }


class BillingProfileTenantAccessCSPPayload(BaseCSPPayload):
    tenant_id: str
    user_object_id: str
    billing_account_name: str
    billing_profile_name: str


class BillingProfileTenantAccessCSPResult(AliasModel):
    billing_role_assignment_id: str
    billing_role_assignment_name: str

    class Config:
        fields = {
            "billing_role_assignment_id": "id",
            "billing_role_assignment_name": "name",
        }


class TaskOrderBillingCreationCSPPayload(BaseCSPPayload):
    billing_account_name: str
    billing_profile_name: str


class TaskOrderBillingCreationCSPResult(AliasModel):
    task_order_billing_verify_url: str
    task_order_retry_after: int

    class Config:
        fields = {
            "task_order_billing_verify_url": "Location",
            "task_order_retry_after": "Retry-After",
        }


class TaskOrderBillingVerificationCSPPayload(BaseCSPPayload):
    task_order_billing_verify_url: str


class BillingProfileEnabledPlanDetails(AliasModel):
    enabled_azure_plans: List[Dict]


class TaskOrderBillingVerificationCSPResult(AliasModel):
    billing_profile_id: str
    billing_profile_name: str
    billing_profile_enabled_plan_details: BillingProfileEnabledPlanDetails

    class Config:
        fields = {
            "billing_profile_id": "id",
            "billing_profile_name": "name",
            "billing_profile_enabled_plan_details": "properties",
        }


class BillingInstructionCSPPayload(BaseCSPPayload):
    initial_clin_amount: float
    initial_clin_start_date: str
    initial_clin_end_date: str
    initial_clin_type: str
    initial_task_order_id: str
    billing_account_name: str
    billing_profile_name: str


class BillingInstructionCSPResult(AliasModel):
    reported_clin_name: str

    class Config:
        fields = {
            "reported_clin_name": "name",
        }

