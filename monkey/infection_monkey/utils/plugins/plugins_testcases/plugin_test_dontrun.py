from infection_monkey.utils.plugins.plugin import Plugin


class PluginDontRun(Plugin):
    @staticmethod
    def should_run(class_name: str) -> bool:
        return False
