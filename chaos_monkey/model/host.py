__author__ = 'itamar'


class VictimHost(object):
    def __init__(self, ip_addr):
        self.ip_addr = ip_addr
        self.cred = {}
        self.os = {}
        self.services = {}
        self.monkey_exe = None
        self.default_tunnel = None
        self.default_server = None

    def as_dict(self):
        return self.__dict__

    def __hash__(self):
        return hash(self.ip_addr)

    def __eq__(self, other):
        if not isinstance(other, VictimHost):
            return False

        return self.ip_addr.__eq__(other.ip_addr)

    def __cmp__(self, other):
        if not isinstance(other, VictimHost):
            return -1

        return self.ip_addr.__cmp__(other.ip_addr)

    def __repr__(self):
        return "<VictimHost %s>" % (self.ip_addr, )

    def __str__(self):
        victim = "Victim Host %s: " % self.ip_addr
        victim += "OS - ["
        for k, v in self.os.iteritems():
            victim += "%s-%s " % (k, v)
        victim += "] Services - ["
        for k, v in self.services.iteritems():
            victim += "%s-%s " % (k, v)
        victim += ']'
        return victim

    def learn_credentials(self, username, password):
        self.cred[username.lower()] = password

    def get_credentials(self, username):
        return self.cred.get(username.lower(), None)

    def set_default_server(self, default_server):
        self.default_server = default_server
