class FailedExploitationError(Exception):
    """Raise when exploiter fails instead of returning False"""


class IncorrectCredentialsError(Exception):
    """Raise to indicate that authentication failed"""


class DomainControllerNameFetchError(FailedExploitationError):
    """Raise on failed attempt to extract domain controller's name"""
