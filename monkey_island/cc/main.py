from __future__ import print_function  # In python 2.7

import os
import sys

import time

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_PATH not in sys.path:
    sys.path.insert(0, BASE_PATH)

from cc.app import init_app
from cc.utils import local_ip_addresses
from cc.environment.environment import env
from cc.database import is_db_server_up

if __name__ == '__main__':
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    mongo_url = os.environ.get('MONGO_URL', env.get_mongo_url())

    while not is_db_server_up(mongo_url):
        print('Waiting for MongoDB server')
        time.sleep(1)

    app = init_app(mongo_url)
    if env.is_debug():
        app.run(host='0.0.0.0', debug=True, ssl_context=('server.crt', 'server.key'))
    else:
        http_server = HTTPServer(WSGIContainer(app),
                                 ssl_options={'certfile': os.environ.get('SERVER_CRT', 'server.crt'),
                                              'keyfile': os.environ.get('SERVER_KEY', 'server.key')})
        http_server.listen(env.get_island_port())
        print('Monkey Island C&C Server is running on https://{}:{}'.format(local_ip_addresses()[0], env.get_island_port()))
        IOLoop.instance().start()

