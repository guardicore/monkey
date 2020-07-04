import logging

from monkey_island.cc.services.reporting.exporting.exporter import Exporter

logger = logging.getLogger(__name__)


def create_seen_label(machine):
    return {
        "label": "Monkey Scan: Machine visible",
        "machine": {
            "ip_addresses": machine['ip_addresses']
        }
    }


def create_exploited_label(machine):
    exploit = machine["???"]  # TODO run a demo with a lot of info in the report
    return {
        "label": f"Monkey Exploit: {exploit}",
        "machine": {
            "ip_addresses": machine['ip_addresses']
        }
    }


def create_machine_labels_from_report(report_json):
    labels = []
    """
    Labels:
    Each label has: 
    the label itself, which can be:
    - Monkey Scan: Seen
    - Monkey Exploit: CVE-xxx
    - Monkey Risk Assessment: low/medium/high
    
    The Machine itself: Only IPs are required
    """
    # Get Monkey seen
    for machine in report_json['glance']['scanned']:
        labels.append(create_seen_label(machine))
    # Get Monkey Exploited
    for machine in report_json['glance']['exploited']:
        labels.append(create_exploited_label(machine))
    # Get Monkey risk assessment
    # TODO choose an assessment scheme with product
    return labels


class LabelsExporter(Exporter):
    @staticmethod
    def handle_report(report_json):
        machine_labels = create_machine_labels_from_report(report_json)
        logger.info(f"Created {len(machine_labels)} labels")
        # Save labels to X?
        # Export labels?
