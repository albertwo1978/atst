import os
import click
import logging
import subprocess

from utils.keyvault.secrets import SecretsClient

logger = logging.getLogger(__name__)


def _run_cmd(command):
    try:
        env = os.environ.copy()
        with subprocess.Popen(
            command, env=env, stdout=subprocess.PIPE, shell=True
        ) as proc:
            for line in proc.stdout:
                logging.info(line.decode("utf-8"))
    except Exception as e:
        print(e)


@click.group()
@click.option("--keyvault", required=True, help="Specify the keyvault to operate on")
@click.pass_context
def database(ctx, keyvault):
    ctx.ensure_object(dict)
    ctx.obj["keyvault"] = keyvault


# root password, root username
@click.command("provision")
@click.option(
    "--app-keyvault",
    "app_keyvault",
    required=True,
    help="The username for the new Postgres user.",
)
@click.option(
    "--user-username",
    "user_username",
    default="atat",
    required=True,
    help="The username for the new Postgres user.",
)
@click.option(
    "--user-password-key",
    "user_password_key",
    default="PGPASSWORD",
    required=True,
    help="The name of the user's password key in the specified vault.",
)
@click.option(
    "--root-username-key",
    "root_username_key",
    default="postgres-root-user",
    required=True,
    help="The name of the user's password key in the specified vault.",
)
@click.option(
    "--root-password-key",
    "root_password_key",
    default="postgres-root-password",
    required=True,
    help="The name of the user's password key in the specified vault.",
)
@click.option(
    "--dbname",
    "dbname",
    required=True,
    help="The name of the database the user will be given full access to.",
)
@click.option(
    "--dbhost",
    "dbhost",
    required=True,
    help="The name of the database the user will be given full access to.",
)
@click.option(
    "--container",
    "container",
    default="atat:latest",
    required=True,
    help="The container to run the provisioning command in.",
)
@click.option(
    "--ccpo-users",
    "ccpo_users",
    required=True,
    help="The full path to a YAML file listing CCPO users to be seeded to the database.",
)
@click.pass_context
def provision(
    ctx,
    app_keyvault,
    user_username,
    user_password_key,
    root_username_key,
    root_password_key,
    dbname,
    dbhost,
    container,
    ccpo_users,
):
    """
    Set up the initial ATAT database.
    """
    logger.info("obtaining postgres root user credentials")
    operator_keyvault = SecretsClient(vault_url=ctx.obj["keyvault"])
    root_password = operator_keyvault.get_secret(root_password_key)
    root_name = operator_keyvault.get_secret(root_username_key)

    logger.info("obtaining postgres database user password")
    app_keyvault = SecretsClient(vault_url=app_keyvault)
    user_password = app_keyvault.get_secret(user_password_key)

    logger.info("starting docker process")

    create_database_cmd = (
        f"docker run -e PGHOST='{dbhost}'"
        f" -e PGPASSWORD='{root_password}'"
        f" -e PGUSER='{root_name}@{dbhost}'"
        f" -e PGDATABASE='{dbname}'"
        f" -e PGSSLMODE=require"
        f" {container}"
        f" .venv/bin/python script/create_database.py {dbname}"
    )
    _run_cmd(create_database_cmd)

    seed_database_cmd = (
        f"docker run -e PGHOST='{dbhost}'"
        f" -e PGPASSWORD='{root_password}'"
        f" -e PGUSER='{root_name}@{dbhost}'"
        f" -e PGDATABASE='{dbname}'"
        f" -e PGSSLMODE=require"
        f" -v {ccpo_users}:/opt/atat/atst/users.yml"
        f" {container}"
        f" .venv/bin/python script/database_setup.py {user_username} '{user_password}' users.yml"
    )
    _run_cmd(seed_database_cmd)


database.add_command(provision)
