from monkey_island.cc.services.reporting.exporting.exporter_factory import ExporterFactory
from monkey_island.cc.services.reporting.exporting.exporter_names import LABELS_EXPORTER
from monkey_island.cc.services.reporting.exporting.labels_exporter import LabelsExporter
from monkey_island.cc.testing.IslandTestCase import IslandTestCase


class TestExporterFactory(IslandTestCase):
    def test_exporter_factory(self):
        self.fail_if_not_testing_env()

        assert ExporterFactory.get_exporter(LABELS_EXPORTER) == LabelsExporter
        with self.assertRaises(NotImplementedError):
            ExporterFactory.get_exporter("THIS IS A BAD EXPORTER NAME")
