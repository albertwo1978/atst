from flask import current_app as app, g, redirect, url_for

from . import index
from . import new
from . import settings
from . import invitations
from .blueprint import applications_bp
from atst.domain.environment_roles import EnvironmentRoles
from atst.domain.exceptions import UnauthorizedError
from atst.domain.authz.decorator import user_can_access_decorator as user_can
from atst.models.permissions import Permissions


def wrap_environment_role_lookup(user, environment_id=None, **kwargs):
    env_role = EnvironmentRoles.get_by_user_and_environment(user.id, environment_id)
    if not env_role:
        raise UnauthorizedError(user, "access environment {}".format(environment_id))

    return True


@applications_bp.route("/environments/<environment_id>/access")
@user_can(None, override=wrap_environment_role_lookup, message="access environment")
def access_environment(environment_id):
    return redirect("https://portal.azure.com")
