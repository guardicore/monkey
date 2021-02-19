from mongoengine import Document, DynamicField


class ScoutSuiteRawDataJson(Document):
    """
    This model is a container for ScoutSuite report data dump.
    """

    # SCHEMA
    scoutsuite_data = DynamicField(required=True)

    # LOGIC
    @staticmethod
    def add_scoutsuite_data(scoutsuite_data: str) -> None:
        try:
            current_data = ScoutSuiteRawDataJson.objects()[0]
        except IndexError:
            current_data = ScoutSuiteRawDataJson()
        current_data.scoutsuite_data = scoutsuite_data
        current_data.save()
