class FailedExploitationError(Exception):
    """Raise when exploiter fails instead of returning False"""


class InvalidRegistrationCredentialsError(Exception):
    """Raise when server config file changed and island needs to restart"""


class IncorrectCredentialsError(Exception):
    """Raise to indicate that authentication failed"""


class DomainControllerNameFetchError(FailedExploitationError):
    """Raise on failed attempt to extract domain controller's name"""
