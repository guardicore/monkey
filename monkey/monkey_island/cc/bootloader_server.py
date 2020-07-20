import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib import parse

import pymongo
import requests
import urllib3

from monkey_island.cc.environment import Environment

# Disable "unverified certificate" warnings when sending requests to island
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # noqa: DUO131
logger = logging.getLogger(__name__)


class BootloaderHttpServer(ThreadingMixIn, HTTPServer):

    def __init__(self, mongo_url):
        self.mongo_client = pymongo.MongoClient(mongo_url)
        server_address = ('', 5001)
        super().__init__(server_address, BootloaderHTTPRequestHandler)


class BootloaderHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        island_server_path = BootloaderHTTPRequestHandler.get_bootloader_resource_url(self.request.getsockname()[0])
        island_server_path = parse.urljoin(island_server_path, self.path[1:])
        # The island server doesn't always have a correct SSL cert installed
        # (By default it comes with a self signed one),
        # that's why we're not verifying the cert in this request.
        r = requests.post(url=island_server_path, data=post_data, verify=False)  # noqa: DUO123

        try:
            if r.status_code != 200:
                self.send_response(404)
            else:
                self.send_response(200)
            self.end_headers()
            self.wfile.write(r.content)
        except Exception as e:
            logger.error("Failed to respond to bootloader: {}".format(e))
        finally:
            self.connection.close()

    @staticmethod
    def get_bootloader_resource_url(server_ip):
        return "https://" + server_ip + ":" + str(Environment._ISLAND_PORT) + "/api/bootloader/"
