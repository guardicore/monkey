from threading import Thread

class TransportProxyBase(Thread):
    def __init__(self, local_port, dest_host=None, dest_port=None, local_host=''):
        self.local_host = local_host
        self.local_port = local_port
        self.dest_host = dest_host
        self.dest_port = dest_port
        self._stopped = False
        super(TransportProxyBase, self).__init__()
        self.daemon = True

    def stop(self):
        self._stopped = True        