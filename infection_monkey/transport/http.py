import BaseHTTPServer
import os.path
import select
import socket
import threading
import urllib
from logging import getLogger
from urlparse import urlsplit
from threading import Lock

import monkeyfs
from base import TransportProxyBase, update_last_serve_time

__author__ = 'hoffer'

LOG = getLogger(__name__)


class FileServHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    filename = ""

    def version_string(self):
        return "Microsoft-IIS/7.5."

    @staticmethod
    def report_download(dest=None):
        pass

    def do_POST(self):
        self.send_error(501, "Unsupported method (POST)")
        return

    def do_GET(self):
        """Serve a GET request."""
        f, start_range, end_range = self.send_head()
        if f:
            f.seek(start_range, 0)
            chunk = 0x1000
            total = 0
            while chunk > 0:
                if start_range + chunk > end_range:
                    chunk = end_range - start_range
                try:
                    self.wfile.write(f.read(chunk))
                except:
                    break
                total += chunk
                start_range += chunk

            if f.tell() == monkeyfs.getsize(self.filename):
                self.report_download(self.client_address)

            f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        f, start_range, end_range = self.send_head()
        if f:
            f.close()

    def send_head(self):
        if self.path != '/' + urllib.quote(os.path.basename(self.filename)):
            self.send_error(500, "")
            return None, 0, 0
        f = None
        try:
            f = monkeyfs.open(self.filename, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None, 0, 0
        size = monkeyfs.getsize(self.filename)
        start_range = 0
        end_range = size

        if "Range" in self.headers:
            s, e = self.headers['range'][6:].split('-', 1)
            sl = len(s)
            el = len(e)
            if sl > 0:
                start_range = int(s)
                if el > 0:
                    end_range = int(e) + 1
            elif el > 0:
                ei = int(e)
                if ei < size:
                    start_range = size - ei

            if start_range == 0 and end_range - start_range >= size:
                self.send_response(200)
            else:
                self.send_response(206)
        else:
            self.send_response(200)

        self.send_header("Content-type", "application/octet-stream")
        self.send_header("Content-Range", 'bytes ' + str(start_range) + '-' + str(end_range - 1) + '/' + str(size))
        self.send_header("Content-Length", min(end_range - start_range, size))
        self.end_headers()
        return f, start_range, end_range

    def log_message(self, format, *args):
        LOG.debug("FileServHTTPRequestHandler: %s - - [%s] %s" % (self.address_string(),
                                                                  self.log_date_time_string(),
                                                                  format % args))


class HTTPConnectProxyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    timeout = 30  # timeout with clients, set to None not to make persistent connection
    proxy_via = None  # pseudonym of the proxy in Via header, set to None not to modify original Via header
    protocol_version = "HTTP/1.1"

    def version_string(self):
        return ""

    def do_CONNECT(self):
        # just provide a tunnel, transfer the data with no modification
        req = self
        reqbody = None
        req.path = "https://%s/" % req.path.replace(':443', '')

        u = urlsplit(req.path)
        address = (u.hostname, u.port or 443)
        try:
            conn = socket.create_connection(address)
        except socket.error as e:
            LOG.debug("HTTPConnectProxyHandler: Got exception while trying to connect to %s: %s" % (repr(address), e))
            self.send_error(504)  # 504 Gateway Timeout
            return
        self.send_response(200, 'Connection Established')
        self.send_header('Connection', 'close')
        self.end_headers()

        conns = [self.connection, conn]
        keep_connection = True
        while keep_connection:
            keep_connection = False
            rlist, wlist, xlist = select.select(conns, [], conns, self.timeout)
            if xlist:
                break
            for r in rlist:
                other = conns[1] if r is conns[0] else conns[0]
                data = r.recv(8192)
                if data:
                    other.sendall(data)
                    keep_connection = True
                    update_last_serve_time()
        conn.close()

    def log_message(self, format, *args):
        LOG.debug("HTTPConnectProxyHandler: %s - [%s] %s" %
                  (self.address_string(), self.log_date_time_string(), format % args))


class HTTPServer(threading.Thread):
    def __init__(self, local_ip, local_port, filename, max_downloads=1):
        self._local_ip = local_ip
        self._local_port = local_port
        self._filename = filename
        self.max_downloads = max_downloads
        self.downloads = 0
        self._stopped = False
        threading.Thread.__init__(self)

    def run(self):
        class TempHandler(FileServHTTPRequestHandler):
            filename = self._filename

            @staticmethod
            def report_download(dest=None):
                LOG.info('File downloaded from (%s,%s)' % (dest[0], dest[1]))
                self.downloads += 1

        httpd = BaseHTTPServer.HTTPServer((self._local_ip, self._local_port), TempHandler)
        httpd.timeout = 0.5  # this is irrelevant?

        while not self._stopped and self.downloads < self.max_downloads:
            httpd.handle_request()

        self._stopped = True

    def stop(self, timeout=60):
        self._stopped = True
        self.join(timeout)

class LockedHTTPServer(threading.Thread):
    def __init__(self, local_ip, local_port, filename, lock, max_downloads=1):
        self._local_ip = local_ip
        self._local_port = local_port
        self._filename = filename
        self.max_downloads = max_downloads
        self.downloads = 0
        self._stopped = False
        self.lock = lock
        threading.Thread.__init__(self)

    def run(self):
        class TempHandler(FileServHTTPRequestHandler):
            filename = self._filename

            @staticmethod
            def report_download(dest=None):
                LOG.info('File downloaded from (%s,%s)' % (dest[0], dest[1]))
                self.downloads += 1

        httpd = BaseHTTPServer.HTTPServer((self._local_ip, self._local_port), TempHandler)
        self.lock.release()
        while not self._stopped and self.downloads < self.max_downloads:
            httpd.handle_request()

        self._stopped = True

    def stop(self, timeout=5):
        self._stopped = True
        self.join(timeout)

class HTTPConnectProxy(TransportProxyBase):
    def run(self):
        httpd = BaseHTTPServer.HTTPServer((self.local_host, self.local_port), HTTPConnectProxyHandler)
        httpd.timeout = 30
        while not self._stopped:
            httpd.handle_request()
