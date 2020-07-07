import binascii
import json
import logging
from pathlib import Path

from monkey_island.cc.services.reporting.exporting.exporter import Exporter

LABEL_KEY_MONKEY_SCAN = "Monkey Scan"
LABEL_KEY_MONKEY_EXPLOIT = "Monkey Exploit"

logger = logging.getLogger(__name__)


def format_ip(ip_addr):
    return "ip:" + binascii.hexlify(ip_addr.encode()).decode()


def create_machine_object(report_glance_machine_info: dict) -> dict:
    ip_addrs = report_glance_machine_info["ip_addresses"]
    ip_addrs_formatted = [format_ip(x) for x in ip_addrs]
    return {
        "ip_addresses": ip_addrs,
        "ip_addresses_formatted": ip_addrs_formatted
    }


def create_seen_label(report_glance_scan_info):
    return {
        "label_key": LABEL_KEY_MONKEY_SCAN,
        "label_value": f"Seen from {len(report_glance_scan_info['accessible_from_nodes'])} machines by Monkey",
        "machine": create_machine_object(report_glance_scan_info)
    }


def create_exploited_label(report_glance_exploit_info):
    exploits = report_glance_exploit_info['exploits']
    logger.debug(f"Info: {report_glance_exploit_info}")
    return {
        "label_key": LABEL_KEY_MONKEY_EXPLOIT,
        "label_value": f"Breached using {', '.join(exploits)} by Monkey",
        "machine": create_machine_object(report_glance_exploit_info)
    }


def create_risk_assessment_label(machine):
    risk_assessment = "Medium"
    return {
        "label_key": "Monkey Risk assessment",
        "label_value": f"Risk: {risk_assessment}",
        "machine": create_machine_object(machine)
    }


def create_machine_labels_from_report(report_json):
    labels = []

    for machine in report_json['glance']['scanned']:
        # Might be the machine the Monkey started on
        if len(machine["accessible_from_nodes"]) > 0:
            labels.append(create_seen_label(machine))

    for machine in report_json['glance']['exploited']:
        labels.append(create_exploited_label(machine))

    # Get Monkey risk assessment
    # TODO choose an assessment scheme with product

    return labels


def export_labels_to_file(machine_labels, output_file_path):
    logger.debug(f"Writing labels to {output_file_path.absolute()}")
    with open(output_file_path, "w") as labels_file:
        json.dump(machine_labels, labels_file, indent=2)


class LabelsExporter(Exporter):
    @staticmethod
    def handle_report(report_json):
        machine_labels = create_machine_labels_from_report(report_json)
        logger.info(f"Created {len(machine_labels)} labels")
        labels_file_path = Path("monkey_labels.json")  # todo get from internal config
        export_labels_to_file(machine_labels, labels_file_path)
        return f"Exported labels to {labels_file_path.absolute()}."
