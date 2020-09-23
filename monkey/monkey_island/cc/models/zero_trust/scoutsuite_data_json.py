from mongoengine import Document, DynamicField


class ScoutSuiteDataJson(Document):
    """
    This model is a container for ScoutSuite report data dump.
    """

    # SCHEMA
    scoutsuite_data = DynamicField(required=True)

    # LOGIC
    @staticmethod
    def add_scoutsuite_data(scoutsuite_data: str) -> None:
        try:
            current_data = ScoutSuiteDataJson.objects()[0]
        except IndexError:
            current_data = ScoutSuiteDataJson()
        current_data.scoutsuite_data = scoutsuite_data
        current_data.save()
