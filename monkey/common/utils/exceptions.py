class ExploitingVulnerableMachineError(Exception):
    """ Raise when exploiter failed, but machine is vulnerable """


class FailedExploitationError(Exception):
    """ Raise when exploiter fails instead of returning False """


class InvalidRegistrationCredentialsError(Exception):
    """ Raise when server config file changed and island needs to restart """


class RegistrationNotNeededError(Exception):
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


class UnknownFindingError(Exception):
    """ Raise when provided finding is of unknown type"""


class VersionServerConnectionError(Exception):
    """ Raise to indicate that connection to version update server failed """


class FindingWithoutDetailsError(Exception):
    """ Raise when pulling events for a finding, but get none """


class DomainControllerNameFetchError(FailedExploitationError):
    """ Raise on failed attempt to extract domain controller's name """


class InvalidConfigurationError(Exception):
    """ Raise when configuration is invalid """
