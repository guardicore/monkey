class ExploitingVulnerableMachineError(Exception):
    """ Raise when exploiter failed, but machine is vulnerable """


class FailedExploitationError(Exception):
    """ Raise when exploiter fails instead of returning False """


class InvalidRegistrationCredentialsError(Exception):
    """ Raise when server config file changed and island needs to restart """


class RegistrationNotNeededError(Exception):
    """ Raise to indicate the reason why registration is not required """


class CredentialsNotRequiredError(RegistrationNotNeededError):
    """ Raise to indicate the reason why registration is not required """


class AlreadyRegisteredError(RegistrationNotNeededError):
    """ Raise to indicate the reason why registration is not required """
