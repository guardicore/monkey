class FailedExploitationError(Exception):
    """Raise when exploiter fails instead of returning False"""


class DomainControllerNameFetchError(FailedExploitationError):
    """Raise on failed attempt to extract domain controller's name"""
