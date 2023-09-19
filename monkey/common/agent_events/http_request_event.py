from http import HTTPMethod

from pydantic import AnyHttpUrl

from . import AbstractAgentEvent


class HTTPRequestEvent(AbstractAgentEvent):
    """
    An event that occurs when the Agent sends an HTTP request to any server other than the Island.

    Attributes:
        :param method: The HTTP method used to make the request
        :param url: The URL to which the request was sent
    """

    method: HTTPMethod
    url: AnyHttpUrl
