import json

BAD_ENDPOINTS = {
    "tcp-80": "Open HTTP server."
}


def test_open_data_endpoints(telemetry_json):
    services = telemetry_json["data"]["machine"]["services"]
    for service_name, service_data in services.items():
        if service_name in BAD_ENDPOINTS:
            # TODO Create finding
            print("found open {} service on address {}, details: {}".format(
                service_data["display_name"],
                telemetry_json["data"]["machine"]["ip_addr"],
                json.dumps(service_data)))
