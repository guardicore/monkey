from common.configuration import PluginConfigurationSchema


def test_build_plugin_configuration():
    name = "bond"
    options = {"gun": "Walther PPK", "car": "Aston Martin DB5"}
    pcs = PluginConfigurationSchema()

    pc = pcs.load({"name": name, "options": options})

    assert pc.name == name
    assert pc.options == options
