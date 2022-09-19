class IslandAPIError(Exception):
    """
    Raised when something goes wrong when calling the Island API
    """

    pass


class IslandAPITimeoutError(IslandAPIError):
    """
    Raised when the API request hits a timeout
    """

    pass


class IslandAPIConnectionError(IslandAPIError):
    """
    Raised when the API request can't find/connect to the Island
    """

    pass


class IslandAPIRequestFailedError(IslandAPIError):
    """
    Raised when the API request fails(malformed request or an error on the API side)
    """

    pass
