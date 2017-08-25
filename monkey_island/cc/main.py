from __future__ import print_function  # In python 2.7

import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_PATH not in sys.path:
    sys.path.insert(0, BASE_PATH)

from cc.app import init_app
from cc.utils import init_collections

ISLAND_PORT = 5000
DEFAULT_MONGO_URL = "mongodb://localhost:27017/monkeyisland"

INITIAL_USERNAMES = ['Administrator', 'root', 'user']
INITIAL_PASSWORDS = ["Password1!", "1234", "password", "12345678"]


if __name__ == '__main__':
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    app = init_app(os.environ.get('MONGO_URL', DEFAULT_MONGO_URL))
    with app.app_context():
        init_collections(INITIAL_USERNAMES, INITIAL_PASSWORDS)
    http_server = HTTPServer(WSGIContainer(app),
                             ssl_options={'certfile': os.environ.get('SERVER_CRT', 'server.crt'),
                                          'keyfile': os.environ.get('SERVER_KEY', 'server.key')})
    http_server.listen(ISLAND_PORT)
    IOLoop.instance().start()
    # app.run(host='0.0.0.0', debug=True, ssl_context=('server.crt', 'server.key'))
