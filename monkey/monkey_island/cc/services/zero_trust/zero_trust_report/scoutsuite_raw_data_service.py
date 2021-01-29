from monkey_island.cc.models.zero_trust.scoutsuite_data_json import ScoutSuiteRawDataJson


class ScoutSuiteRawDataService:

    # Return unparsed json of ScoutSuite results,
    # so that UI can pick out values it needs for report
    @staticmethod
    def get_scoutsuite_data_json() -> str:
        try:
            return ScoutSuiteRawDataJson.objects.get().scoutsuite_data
        except Exception:
            return "{}"
