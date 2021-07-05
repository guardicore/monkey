import traceback

import gevent.hub


class GeventHubErrorHandler:
    """
    Wraps gevent.hub.Hub's handle_error() method so that the exception can be
    logged but the traceback can be stored in a separate file. This preserves
    the default gevent functionality and adds a useful, concise log message to
    the Monkey Island logs.

    For more information, see
        https://github.com/guardicore/monkey/issues/859,
        https://www.gevent.org/api/gevent.hub.html#gevent.hub.Hub.handle_error
        https://github.com/gevent/gevent/issues/1482
    """

    def __init__(self, hub: gevent.hub.Hub, logger):
        self._original_handle_error = hub.handle_error
        self._logger = logger

    def __call__(self, context, type_, value, tb):
        exception_msg = traceback.format_exception_only(type_, value)
        self._logger.warning(f"gevent caught an exception: {exception_msg}")
        self._original_handle_error(context, type_, value, tb)
