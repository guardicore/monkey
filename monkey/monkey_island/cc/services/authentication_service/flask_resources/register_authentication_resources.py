import flask_restful
from flask_limiter import Limiter

from ..authentication_facade import AuthenticationFacade
from ..i_otp_generator import IOTPGenerator
from .agent_otp import AgentOTP
from .agent_otp_login import AgentOTPLogin
from .login import Login
from .logout import Logout
from .refresh_authentication_token import RefreshAuthenticationToken
from .register import Register
from .registration_status import RegistrationStatus


def register_resources(
    api: flask_restful.Api,
    authentication_facade: AuthenticationFacade,
    otp_generator: IOTPGenerator,
    limiter: Limiter,
):
    api.add_resource(Register, *Register.urls, resource_class_args=(authentication_facade,))
    api.add_resource(
        RegistrationStatus, *RegistrationStatus.urls, resource_class_args=(authentication_facade,)
    )
    api.add_resource(Login, *Login.urls, resource_class_args=(authentication_facade, limiter))
    api.add_resource(Logout, *Logout.urls, resource_class_args=(authentication_facade,))

    api.add_resource(AgentOTP, *AgentOTP.urls, resource_class_args=(otp_generator, limiter))
    api.add_resource(
        AgentOTPLogin,
        *AgentOTPLogin.urls,
        resource_class_args=(authentication_facade, limiter),
    )
    api.add_resource(
        RefreshAuthenticationToken,
        *RefreshAuthenticationToken.urls,
        resource_class_args=(authentication_facade, limiter),
    )
