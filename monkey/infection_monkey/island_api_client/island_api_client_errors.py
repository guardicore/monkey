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


class IslandAPIRequestError(IslandAPIError):
    """
    Raised when the API request fails due to an error in the request sent from the client
    """

    pass


class IslandAPIAuthenticationError(IslandAPIError):
    """
    Raised when the authentication to the API failed
    """

    pass


class IslandAPIRequestFailedError(IslandAPIError):
    """
    Raised when the API request fails due to an error on the server
    """

    pass


class IslandAPIResponseParsingError(IslandAPIError):
    """
    Raised when IslandAPIClient fails to parse the response
    """

    pass


class IslandAPIRequestLimitExceededError(IslandAPIError):
    """
    Raised when the API request fails due to rate limiting
    """

    pass
