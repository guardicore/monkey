class ExploitingVulnerableMachineError(Exception):
    """ Raise when exploiter failed, but machine is vulnerable """


class FailedExploitationError(Exception):
    """ Raise when exploiter fails instead of returning False """


class InvalidRegistrationCredentials(Exception):
    """ Raise when server config file changed and island needs to restart """
