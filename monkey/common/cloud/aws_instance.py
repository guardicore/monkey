import urllib2

__author__ = 'itay.mizeretz'


class AwsInstance(object):
    def __init__(self):
        try:
            self.instance_id = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read()
            self.region = urllib2.urlopen('http://169.254.169.254/latest/meta-data/placement/availability-zone').read()[:-1]
        except urllib2.URLError:
            self.instance_id = None
            self.region = None

    def get_instance_id(self):
        return self.instance_id

    def get_region(self):
        return self.region

    def is_aws_instance(self):
        return self.instance_id is not None
