import flask_restful
from flask_security import MongoEngineUserDatastore

from common import DIContainer
from monkey_island.cc.event_queue import IIslandEventQueue
from monkey_island.cc.server_utils.encryption import ILockableEncryptor

from ..authentication_facade import AuthenticationFacade
from .agent_otp import AgentOTP
from .agent_otp_login import AgentOTPLogin
from .login import Login
from .logout import Logout
from .register import Register
from .registration_status import RegistrationStatus


def register_resources(
    api: flask_restful.Api, container: DIContainer, user_datastore: MongoEngineUserDatastore
):
    repository_encryptor = container.resolve(ILockableEncryptor)
    island_event_queue = container.resolve(IIslandEventQueue)
    authentication_facade = AuthenticationFacade(
        repository_encryptor, island_event_queue, user_datastore
    )

    api.add_resource(Register, *Register.urls, resource_class_args=(authentication_facade,))
    api.add_resource(
        RegistrationStatus, *RegistrationStatus.urls, resource_class_args=(authentication_facade,)
    )
    api.add_resource(Login, *Login.urls, resource_class_args=(authentication_facade,))
    api.add_resource(Logout, *Logout.urls, resource_class_args=(authentication_facade,))
    api.add_resource(AgentOTP, *AgentOTP.urls)
    api.add_resource(AgentOTPLogin, *AgentOTPLogin.urls)
