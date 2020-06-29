import logging

from monkey_island.cc.services.reporting.exporting.exporter import Exporter

logger = logging.getLogger(__name__)


def create_machine_labels_from_report(report_json):
    labels = []
    # TODO Create labels from exporters
    return labels


class LabelsExporter(Exporter):
    @staticmethod
    def handle_report(report_json):
        breakpoint()
        machine_labels = create_machine_labels_from_report(report_json)
        logger.info(f"Created {len(machine_labels)} labels")
        # Save labels to X?
        # Export labels?
