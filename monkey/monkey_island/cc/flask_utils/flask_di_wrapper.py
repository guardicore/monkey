import re
from typing import Iterable, Set, Type

import flask_restful
from ophidian import DIContainer

from . import AbstractResource


class FlaskDIWrapper:
    class DuplicateURLError(Exception):
        pass

    url_parameter_regex = re.compile(r"<.*?:.*?>")

    def __init__(self, api: flask_restful.Api, container: DIContainer):
        self._api = api
        self._container = container
        self._reserved_urls: Set[str] = set()

    def add_resource(self, resource: Type[AbstractResource]):
        if len(resource.urls) == 0:
            raise ValueError(f"Resource {resource.__name__} has no defined URLs")

        self._reserve_urls(resource.urls)

        # enforce our rule that URLs should not contain a trailing slash
        for url in resource.urls:
            if url.endswith("/"):
                raise ValueError(
                    f"Resource {resource.__name__} has an invalid URL: A URL "
                    "should not have a trailing slash."
                )
        dependencies = self._container.resolve_dependencies(resource)
        self._api.add_resource(resource, *resource.urls, resource_class_args=dependencies)

    def _reserve_urls(self, urls: Iterable[str]):
        for url in map(FlaskDIWrapper._format_url, urls):
            if url in self._reserved_urls:
                raise FlaskDIWrapper.DuplicateURLError(f"URL {url} has already been registered!")

            self._reserved_urls.add(url)

    @staticmethod
    def _format_url(url: str):
        new_url = url.strip("/")
        return FlaskDIWrapper.url_parameter_regex.sub("<PARAMETER_PLACEHOLDER>", new_url)
