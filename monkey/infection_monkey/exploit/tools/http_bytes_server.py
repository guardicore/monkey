import http.server
import logging
import threading
from http import HTTPStatus
from typing import Optional, Type

from monkeytoolbox import create_daemon_thread, insecure_generate_random_string
from monkeytypes import Event, SocketAddress

logger = logging.getLogger(__name__)


class HTTPBytesServer:
    """
    An HTTP server that serves some bytes. This server limits the number of requests to one. That
    is, after one victim has downloaded the bytes, the server will respond with a 429 error to all
    future requests.
    """

    def __init__(
        self, bind_address: SocketAddress, bytes_to_serve: bytes, poll_interval: float = 0.5
    ):
        """
        :param socket_address: The address that this server will listen on
        :param bytes_to_server: The data (bytes) that the server will serve
        :param poll_interval: Poll for shutdown every `poll_interval` seconds, defaults to 0.5.
        """
        logger.debug(f"The server will be accessible at http://{bind_address}")

        self._bind_address = bind_address
        self._bytes_downloaded = threading.Event()
        self._poll_interval = poll_interval

        HTTPHandler = _get_new_http_handler_class(bytes_to_serve, self._bytes_downloaded)

        server_ip = str(bind_address.ip)
        server_port = int(bind_address.port)
        self._server = http.server.HTTPServer((server_ip, server_port), HTTPHandler)

        server_thread_name = (
            f"{threading.current_thread().name}-HTTPBytesServer-"
            f"{insecure_generate_random_string(n=8)}"
        )
        self._server_thread = create_daemon_thread(
            target=self._server.serve_forever,
            name=server_thread_name,
            args=(self._poll_interval,),
        )

    def start(self):
        """
        Runs the HTTP server in the background and blocks until the server has successfully started
        """
        logger.info("Starting HTTPBytesServer")
        self._bytes_downloaded.clear()

        # NOTE: Unlike in LDAPExploitServer, we theoretically don't need to worry about a race
        # between when `serve_forever()` is ready to handle requests and when the victim machine
        # sends its requests. This could change if we switch from multithreading to multiprocessing.
        # See
        # https://stackoverflow.com/questions/22606480/how-can-i-test-if-python-http-server-httpserver-is-serving-forever
        # for more information.
        self._server_thread.start()

    def stop(self, timeout: Optional[float] = None):
        """
        Stops the HTTP server.

        :param timeout: A floating point number of seconds to wait for the server to stop. If this
                        argument is None (the default), the method blocks until the HTTP server
                        terminates. If `timeout` is a positive floating point number, this method
                        blocks for at most `timeout` seconds.
        """
        if self._server_thread.is_alive():
            logger.debug("Stopping the HTTP server")
            self._server.shutdown()
            self._server_thread.join(timeout)

        if self._server_thread.is_alive():
            logger.warning("Timed out while waiting for the HTTP server to stop")
        else:
            logger.debug("The HTTP server has stopped")

    @property
    def bytes_downloaded(self) -> Event:
        """
        Returns whether or not a victim has downloaded the bytes from the server.

        :return: True if the victim has downloaded the bytes from the server. False
                 otherwise.
        """
        return self._bytes_downloaded

    @property
    def download_url(self) -> str:
        """
        Returns the URL that should be used to download the bytes from the server

        :return: The URL that should be used to download the bytes from the server
        """
        return f"http://{self._bind_address}/"


def _get_new_http_handler_class(
    bytes_to_serve: bytes, bytes_downloaded: threading.Event
) -> Type[http.server.BaseHTTPRequestHandler]:
    """
    Dynamically create a new subclass of http.server.BaseHTTPRequestHandler and return it to the
    caller.

    Because Python's http.server.HTTPServer accepts a class and creates a new object to
    handle each request it receives, any state that needs to be shared between requests must be
    stored as class variables. Creating the request handler classes dynamically at runtime allows
    multiple HTTPBytesServers, each with it's own unique state, to run concurrently.
    """

    def do_GET(self):
        with self.download_lock:
            if self.bytes_downloaded.is_set():
                self.send_error(
                    HTTPStatus.TOO_MANY_REQUESTS,
                    "A download has already been requested",
                )
                return

            logger.info("Received a GET request!")

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "application/octet-stream")
            self.end_headers()

            logger.info("Sending the bytes to the requester")
            self.wfile.write(self.bytes_to_serve)
            self.bytes_downloaded.set()

    return type(
        "HTTPHandler",
        (http.server.BaseHTTPRequestHandler,),
        {
            "bytes_to_serve": bytes_to_serve,
            "bytes_downloaded": bytes_downloaded,
            "download_lock": threading.Lock(),
            "do_GET": do_GET,
        },
    )
