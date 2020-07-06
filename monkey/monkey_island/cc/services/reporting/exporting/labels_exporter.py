import binascii
import json
import logging
from pathlib import Path

from monkey_island.cc.services.reporting.exporting.exporter import Exporter

logger = logging.getLogger(__name__)


def create_machine_object(machine):
    ip_addrs = machine["ip_addresses"]
    ip_addrs_formatted = ["ip:" + binascii.hexlify(x.encode()).decode() for x in ip_addrs]
    return {
        "ip_addresses": ip_addrs,
        "ip_addresses_formatted": ip_addrs_formatted
    }


def create_seen_label(machine):
    return {
        "label_key": "Monkey Scan",
        "label_value": f"Seen be Monkeys {machine['accessible_from_nodes']}",
        "machine": create_machine_object(machine)
    }


def create_exploited_label(machine):
    exploit = "ssh"
    # exploit = machine["???"]
    logger.debug(f"Info: {machine}")
    return {
        "label_key": "Monkey Exploit",
        "label_value": f"{exploit} used by Monkey",
        "machine": {
            create_machine_object(machine)
        }
    }


def create_risk_assessment_label(machine):
    risk_assessment = "Medium" # TODO run a demo with a lot of info in the report
    return {
        "label_key": "Monkey Risk assessment",
        "label_value": f"Risk: {risk_assessment}",
        "machine": {
            create_machine_object(machine)
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
        # Might be the machine the Monkey started on
        if len(machine["accessible_from_nodes"]) > 0:
            labels.append(create_seen_label(machine))
    # Get Monkey Exploited
    for machine in report_json['glance']['exploited']:
        labels.append(create_exploited_label(machine))
    # Get Monkey risk assessment
    # TODO choose an assessment scheme with product
    return labels


def export_labels_to_file(machine_labels):
    labels_file_path = Path("monkey_labels.json")  # todo get from internal config
    logger.debug(f"Writing labels to {labels_file_path.absolute()}")
    with open(labels_file_path, "w") as labels_file:
        json.dump(machine_labels, labels_file, indent=2)


class LabelsExporter(Exporter):
    @staticmethod
    def handle_report(report_json):
        machine_labels = create_machine_labels_from_report(report_json)
        logger.info(f"Created {len(machine_labels)} labels")
        export_labels_to_file(machine_labels)
        # Save labels to X?
        # Export labels?
