import json
import secrets
from pathlib import Path
from typing import Any, Dict

from flask.sessions import SecureCookieSessionInterface
from flask_mongoengine import MongoEngine
from flask_security import ConfirmRegisterForm, MongoEngineUserDatastore, Security, UserDatastore
from monkeytoolbox import open_new_securely_permissioned_file
from wtforms import StringField

from monkey_island.cc.mongo_consts import MONGO_DB_HOST, MONGO_DB_NAME, MONGO_DB_PORT, MONGO_URL

from . import AccountRole
from .role import Role
from .user import User

SECRET_FILE_NAME = ".flask_security_configuration.json"
ACCESS_TOKEN_TTL = 15 * 60  # 15 minutes


def configure_flask_security(app, data_dir: Path) -> Security:
    _setup_flask_mongo(app)

    flask_security_config = _generate_flask_security_configuration(data_dir)
    app.config["SECRET_KEY"] = flask_security_config["secret_key"]
    app.config["SECURITY_PASSWORD_SALT"] = flask_security_config["password_salt"]
    app.config["SECURITY_USERNAME_ENABLE"] = True
    app.config["SECURITY_USERNAME_REQUIRED"] = True
    app.config["SECURITY_REGISTERABLE"] = True
    app.config["SECURITY_SEND_REGISTER_EMAIL"] = False

    app.config["SECURITY_TOKEN_MAX_AGE"] = ACCESS_TOKEN_TTL
    app.config["SECURITY_RETURN_GENERIC_RESPONSES"] = True
    # Ignore CSRF, because we don't store tokens in cookies
    app.config["WTF_CSRF_CHECK_DEFAULT"] = False
    app.config["SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS"] = True
    # Forbid sending authentication token in URL parameters
    app.config["SECURITY_TOKEN_AUTHENTICATION_KEY"] = None

    # The database object needs to be created after we configure the flask application
    db = MongoEngine(app)
    user_datastore = MongoEngineUserDatastore(db, User, Role)

    _create_roles(user_datastore)

    class CustomConfirmRegisterForm(ConfirmRegisterForm):
        # We don't use the email, but the field is required by ConfirmRegisterForm.
        # Email validators need to be overriden, otherwise an error about invalid email is raised.
        email = StringField("Email", default="dummy@dummy.com", validators=[])

        def to_dict(self, only_user):
            registration_dict = super().to_dict(only_user)
            registration_dict.update({"roles": [AccountRole.ISLAND_INTERFACE.name]})
            return registration_dict

    app.security = Security(
        app,
        user_datastore,
        confirm_register_form=CustomConfirmRegisterForm,
        register_blueprint=False,
    )
    # Force Security to always respond as an API rather than HTTP server
    # This will cause 401 response instead of 301 for unauthorized requests for example
    app.security._want_json = lambda _request: True

    app.session_interface = _disable_session_cookies()

    return app.security


def _setup_flask_mongo(app):
    app.config["MONGO_URI"] = MONGO_URL
    app.config["MONGODB_SETTINGS"] = [
        {
            "db": MONGO_DB_NAME,
            "host": MONGO_DB_HOST,
            "port": MONGO_DB_PORT,
        }
    ]


def _generate_flask_security_configuration(data_dir: Path) -> Dict[str, Any]:
    secret_file_path = str(data_dir / SECRET_FILE_NAME)
    try:
        with open(secret_file_path, "r") as secret_file:
            return json.load(secret_file)
    except FileNotFoundError:
        with open_new_securely_permissioned_file(secret_file_path, "w") as secret_file:
            secret_key = secrets.token_urlsafe(32)
            password_salt = str(secrets.SystemRandom().getrandbits(128))

            security_options = {"secret_key": secret_key, "password_salt": password_salt}
            json.dump(security_options, secret_file)

            return security_options


def _create_roles(user_datastore: UserDatastore):
    user_datastore.find_or_create_role(name=AccountRole.ISLAND_INTERFACE.name)
    user_datastore.find_or_create_role(name=AccountRole.AGENT.name)


def _disable_session_cookies() -> SecureCookieSessionInterface:
    class CustomSessionInterface(SecureCookieSessionInterface):
        """Prevent creating session from API requests."""

        def should_set_cookie(self, *args, **kwargs):
            return False

        def save_session(self, *args, **kwargs):
            return

    return CustomSessionInterface()
