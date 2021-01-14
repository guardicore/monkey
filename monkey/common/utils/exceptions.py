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


class RulePathCreatorNotFound(Exception):
    """ Raise to indicate that ScoutSuite rule doesn't have a path creator"""


class InvalidAWSKeys(Exception):
    """ Raise to indicate that AWS API keys are invalid"""


class NoInternetError(Exception):
    """ Raise to indicate problems caused when no internet connection is present"""


class ScoutSuiteScanError(Exception):
    """ Raise to indicate problems ScoutSuite encountered during scanning"""
