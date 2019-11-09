from infection_monkey.utils.plugins.plugin import Plugin


class PluginShouldRun(Plugin):

    def __init__(self):
        raise ValueError("Some Error")

    @staticmethod
    def should_run(class_name: str) -> bool:
        return True
