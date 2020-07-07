from monkey_island.cc.services.reporting.exporting.labels_exporter import create_machine_labels_from_report, \
    LABEL_KEY_MONKEY_SCAN, LABEL_KEY_MONKEY_EXPLOIT, create_machine_object, format_ip
from monkey_island.cc.testing.IslandTestCase import IslandTestCase


class TestLabelsExporter(IslandTestCase):
    def test_format_ip(self):
        assert format_ip('172.18.42.90') == 'ip:3137322e31382e34322e3930'

    def test_create_machine_object(self):
        machine_object = create_machine_object({
                    'label': 'unknown',
                    'ip_addresses': ['172.18.42.90'],
                    'accessible_from_nodes': ['gc-pc-169.gc.guardicore.com'],
                    'services': [],
                    'domain_name': '',
                    'pba_results': 'None'
                })

        assert machine_object['ip_addresses'] == ['172.18.42.90']
        assert machine_object['ip_addresses_formatted'] == ['ip:3137322e31382e34322e3930']

    def test_handle_report(self):
        self.fail_if_not_testing_env()
        # only has the relevant sub-sections
        fake_report = {
            'glance': {
                'scanned': [{
                    'label': 'unknown',
                    'ip_addresses': ['172.18.42.90'],
                    'accessible_from_nodes': ['gc-pc-169.gc.guardicore.com'],
                    'services': [],
                    'domain_name': '',
                    'pba_results': 'None'
                }, {
                    'label': 'unknown',
                    'ip_addresses': ['172.18.37.210'],
                    'accessible_from_nodes': ['gc-pc-169.gc.guardicore.com'],
                    'services': [],
                    'domain_name': '',
                    'pba_results': 'None'
                }],
                'exploited': [{
                    'label': 'unknown',
                    'ip_addresses': ['172.18.37.210'],
                    'accessible_from_nodes': ['gc-pc-169.gc.guardicore.com'],
                    'exploits': ["SSH Exploiter"],
                    'domain_name': '',
                    'pba_results': 'None'
                }],
                'stolen_creds': [],
                'azure_passwords': [],
                'ssh_keys': [],
                'strong_users': []
            },
        }

        labels = create_machine_labels_from_report(fake_report)
        assert len(labels) == 3
        assert len(list(filter(lambda x: LABEL_KEY_MONKEY_SCAN == x["label_key"], labels))) == 2
        assert len(list(filter(lambda x: LABEL_KEY_MONKEY_EXPLOIT == x["label_key"], labels))) == 1
