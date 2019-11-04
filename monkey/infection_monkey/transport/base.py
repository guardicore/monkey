import time
from threading import Thread

g_last_served = None


class TransportProxyBase(Thread):
    def __init__(self, local_port, dest_host=None, dest_port=None, local_host=''):
        global g_last_served

        self.local_host = local_host
        self.local_port = local_port
        self.dest_host = dest_host
        self.dest_port = dest_port
        self._stopped = False
        super(TransportProxyBase, self).__init__()
        self.daemon = True

    def stop(self):
        self._stopped = True


def update_last_serve_time():
    global g_last_served
    g_last_served = time.time()


def get_last_serve_time():
    global g_last_served
    return g_last_served
