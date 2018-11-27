import urllib2

__author__ = 'itay.mizeretz'


class AWS:
    def __init__(self):
        try:
            self.instance_id = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read()
        except urllib2.URLError:
            self.instance_id = None

    def get_instance_id(self):
        return self.instance_id

    def is_aws_instance(self):
        return self.instance_id is not None
