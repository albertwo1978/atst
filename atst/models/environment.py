from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum

from atst.models.base import Base
import atst.models.mixins as mixins
import atst.models.types as types


class Environment(
    Base, mixins.TimestampsMixin, mixins.AuditableMixin, mixins.DeletableMixin
):
    __tablename__ = "environments"

    id = types.Id()
    name = Column(String, nullable=False)

    application_id = Column(ForeignKey("applications.id"), nullable=False)
    application = relationship("Application")

    # User user.id as the foreign key here beacuse the Environment creator may
    # not have an application role. We may need to revisit this if we receive any
    # requirements around tracking an environment's custodian.
    creator_id = Column(ForeignKey("users.id"), nullable=False)
    creator = relationship("User")

    cloud_id = Column(String)
    root_user_info = Column(JSONB(none_as_null=True))

    claimed_until = Column(TIMESTAMP(timezone=True))

    roles = relationship(
        "EnvironmentRole",
        back_populates="environment",
        primaryjoin="and_(EnvironmentRole.environment_id == Environment.id, EnvironmentRole.deleted == False)",
    )

    __table_args__ = (
        UniqueConstraint(
            "name", "application_id", name="environments_name_application_id_key"
        ),
    )

    class ProvisioningStatus(Enum):
        PENDING = "pending"
        COMPLETED = "completed"

    @property
    def users(self):
        return {r.application_role.user for r in self.roles}

    @property
    def num_users(self):
        return len(self.users)

    @property
    def displayname(self):
        return self.name

    @property
    def portfolio(self):
        return self.application.portfolio

    @property
    def portfolio_id(self):
        return self.application.portfolio_id

    @property
    def provisioning_status(self) -> ProvisioningStatus:
        if self.cloud_id is None or self.root_user_info is None:
            return self.ProvisioningStatus.PENDING
        else:
            return self.ProvisioningStatus.COMPLETED

    @property
    def is_pending(self):
        return self.provisioning_status == self.ProvisioningStatus.PENDING

    def __repr__(self):
        return "<Environment(name='{}', num_users='{}', application='{}', portfolio='{}', id='{}')>".format(
            self.name,
            self.num_users,
            self.application.name,
            self.application.portfolio.name,
            self.id,
        )

    @property
    def history(self):
        return self.get_changes()

    @property
    def csp_credentials(self):
        return (
            self.root_user_info.get("credentials")
            if self.root_user_info is not None
            else None
        )
