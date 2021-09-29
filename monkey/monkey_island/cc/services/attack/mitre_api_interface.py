class MitreApiInterface:
    @staticmethod
    def get_stix2_external_reference_id(stix2_data) -> str:
        for reference in stix2_data["external_references"]:
            if reference["source_name"] == "mitre-attack" and "external_id" in reference:
                return reference["external_id"]
        return ""

    @staticmethod
    def get_stix2_external_reference_url(stix2_data) -> str:
        for reference in stix2_data["external_references"]:
            if "url" in reference:
                return reference["url"]
        return ""
