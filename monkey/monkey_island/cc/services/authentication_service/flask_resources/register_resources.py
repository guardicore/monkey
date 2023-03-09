from monkey_island.cc.flask_utils import FlaskDIWrapper

from .login import Login
from .logout import Logout
from .register import Register
from .registration_status import RegistrationStatus


def register_resources(api: FlaskDIWrapper):
    api.add_resource(Register)
    api.add_resource(RegistrationStatus)
    api.add_resource(Login)
    api.add_resource(Logout)
