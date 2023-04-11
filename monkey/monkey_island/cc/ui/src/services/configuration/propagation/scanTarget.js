const SCAN_TARGET_CONFIGURATION_SCHEMA = {
  'title': 'Network',
  'type': 'object',
  'description': 'If "Scan Agent\'s networks" is checked, the Monkey scans for machines on each ' +
    'of the network interfaces of the machine it is running on.\nAdditionally, the Monkey scans ' +
    'machines according to "Scan target list" and skips machines in "Blocked IPs".',
  'properties': {
    'blocked_ips': {
      'title': 'Blocked IPs',
      'type': 'array',
      'uniqueItems': true,
      'items': {
        'type': 'string',
        'format': 'ip'
      },
      'default': [],
      'description': 'List of IPs that the monkey will not scan.'
    },
    'scan_my_networks': {
      'title': 'Scan Agent\'s networks',
      'type': 'boolean',
      'default': false
    },
    'subnets': {
      'title': 'Scan target list',
      'type': 'array',
      'uniqueItems': true,
      'items': {
        'type': 'string',
        'format': 'ip-range'
      },
      'default': [],
      'description': 'List of targets the Monkey will try to scan. Targets can be ' +
        'IPs, subnets or hosts. ' +
        'Examples:\n' +
        '\tTarget a specific IP: "192.168.0.1"\n' +
        '\tTarget a subnet using a network range: ' +
        '"192.168.0.5-192.168.0.20"\n' +
        '\tTarget a subnet using an IP mask: "192.168.0.5/24"\n' +
        '\tTarget a specific host: "printer.example"'
    },
    'inaccessible_subnets': {
      'title': 'Network segmentation testing',
      'type': 'array',
      'uniqueItems': true,
      'items': {
        'type': 'string',
        'format': 'ip-range'
      },
      'default': [],
      'description': 'Test for network segmentation by providing a list of network segments that should not be accessible to each other.\n\n ' +
        'For example, if you configured the following three segments: ' +
        '"10.0.0.0/24", "11.0.0.2/32" and "12.2.3.0/24",' +
        'a Monkey running on 10.0.0.5 will try to access machines in ' +
        'the following subnets: ' +
        '11.0.0.2/32, 12.2.3.0/24. An alert on successful cross-segment connections ' +
        'will be shown in the reports. \n\n' +
        'Network segments can be IPs, subnets or hosts. Examples:\n' +
        '\tDefine a single-IP segment: "192.168.0.1"\n' +
        '\tDefine a segment using a network range: ' +
        '"192.168.0.5-192.168.0.20"\n' +
        '\tDefine a segment using an subnet IP mask: "192.168.0.5/24"\n' +
        '\tDefine a single-host segment: "printer.example"\n\n' +
        ' \u26A0 ' +
        'Note that the networks configured in this section will be scanned using ping sweep.'
    }
  }
}
export default SCAN_TARGET_CONFIGURATION_SCHEMA;
