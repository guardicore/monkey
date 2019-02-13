import re
import urllib2

__author__ = 'itay.mizeretz'


class AwsInstance(object):
    def __init__(self):
        try:
            self.instance_id = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id', timeout=2).read()
            self.region = self._parse_region(
                urllib2.urlopen('http://169.254.169.254/latest/meta-data/placement/availability-zone').read())
        except urllib2.URLError:
            self.instance_id = None
            self.region = None

    @staticmethod
    def _parse_region(region_url_response):
        # For a list of regions: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html
        # This regex will find any AWS region format string in the response.
        re_phrase = r'((?:us|eu|ap|ca|cn|sa)-[a-z]*-[0-9])'
        finding = re.findall(re_phrase, region_url_response, re.IGNORECASE)
        if finding:
            return finding[0]
        else:
            return None

    def get_instance_id(self):
        return self.instance_id

    def get_region(self):
        return self.region

    def is_aws_instance(self):
        return self.instance_id is not None
