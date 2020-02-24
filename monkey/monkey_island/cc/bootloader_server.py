from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib import parse
import urllib3

import requests
import pymongo

# Disable "unverified certificate" warnings when sending requests to island
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BootloaderHttpServer(ThreadingMixIn, HTTPServer):

    def __init__(self, mongo_url):
        self.mongo_client = pymongo.MongoClient(mongo_url)
        server_address = ('', 5001)
        super().__init__(server_address, BootloaderHTTPRequestHandler)


class BootloaderHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        conf = self.server.mongo_client['monkeyisland']['config'].find_one({'name': 'newconfig'})
        if not conf:
            conf = self.server.mongo_client['monkeyisland']['config'].find_one({'name': 'initial'})
        island_server_path = BootloaderHTTPRequestHandler.get_bootloader_resource_path_from_config(conf)
        island_server_path = parse.urljoin(island_server_path, self.path)
        r = requests.post(url=island_server_path, data=post_data, verify=False)

        if r.status_code != 200:
            self.send_response(404)
        else:
            self.send_response(200)
        self.end_headers()
        self.wfile.write(r.content)
        self.connection.close()

    @staticmethod
    def get_bootloader_resource_path_from_config(config):
        address = config['cnc']['servers']['current_server']
        return parse.urljoin("https://"+address, "api/bootloader")
