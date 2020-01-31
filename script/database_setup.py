# Add root application dir to the python path
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

import sqlalchemy
import yaml

from atst.app import make_config, make_app
from atst.database import db
from atst.domain.users import Users
from atst.models import User
from reset_database import reset_database


def database_setup(username, password, dbname, ccpo_users):
    print(
        f"Creating Postgres user role for '{username}' and granting all privileges to database '{dbname}'."
    )
    try:
        _create_database_user(username, password, dbname)
    except sqlalchemy.exc.ProgrammingError as err:
        print(f"Postgres user role '{username}' already exists.")

    print("Applying schema and seeding roles and permissions.")
    reset_database()
    print("Creating initial set of CCPO users.")
    _add_ccpo_users(ccpo_users)


def _create_database_user(username, password, dbname):
    conn = db.engine.connect()

    meta = sqlalchemy.MetaData(bind=conn)
    meta.reflect()

    trans = conn.begin()
    engine = trans.connection.engine

    engine.execute(
        f"CREATE ROLE {username} WITH LOGIN NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION PASSWORD '{password}';\n"
        f"GRANT ALL PRIVILEGES ON DATABASE {dbname} TO {username};\n"
        f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO {username}; \n"
        f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO {username}; \n"
        f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON FUNCTIONS TO {username}; \n"
    )

    trans.commit()


def _add_ccpo_users(ccpo_users):
    for user_data in ccpo_users:
        user = User(**user_data)
        Users.give_ccpo_perms(user, commit=False)
        db.session.add(user)

    db.session.commit()


def _load_yaml(file_):
    with open(file_) as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    config = make_config({"DISABLE_CRL_CHECK": True, "DEBUG": False})
    app = make_app(config)
    with app.app_context():
        dbname = config.get("PGDATABASE", "atat")
        username = sys.argv[1]
        password = sys.argv[2]
        ccpo_user_file = sys.argv[3]
        ccpo_users = _load_yaml(ccpo_user_file)
        database_setup(username, password, dbname, ccpo_users)
