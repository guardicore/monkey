import threading
from logging import getLogger
from typing import Any

from serpentarium import MultiUsePlugin, PluginLoader

logger = getLogger(__name__)


# NOTE: This should probably get moved to serpentarium.
class MultiprocessingPluginWrapper(MultiUsePlugin):
    """
    Wraps a MultiprocessingPlugin so it can be used like a MultiUsePlugin
    """

    process_start_lock = threading.Lock()

    def __init__(self, *, plugin_loader: PluginLoader, plugin_name: str, **kwargs):
        self._plugin_loader = plugin_loader
        self._name = plugin_name
        self._constructor_kwargs = kwargs

    def run(self, **kwargs) -> Any:
        logger.debug(f"Constructing a new instance of {self._name}")
        plugin = self._plugin_loader.load_multiprocessing_plugin(
            plugin_name=self._name, **self._constructor_kwargs
        )

        # HERE BE DRAGONS! multiprocessing.Process.start() is not thread-safe on Linux when used
        # with the "spawn" method. See https://github.com/pyinstaller/pyinstaller/issues/7410 for
        # more details.
        # UPDATE: This has been resolved in PyInstaller 5.8.0. Consider removing this lock, but
        # leaving a comment here for future reference.
        with MultiprocessingPluginWrapper.process_start_lock:
            logger.debug("Invoking plugin.start()")
            plugin.start(**kwargs)

        plugin.join()
        return plugin.return_value

    @property
    def name(self) -> str:
        return self._name
