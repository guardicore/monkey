class PluginInstallationError(ValueError):
    """
    Raised when a service encounters an error while attempting to install a plugin
    """


class PluginUninstallationError(Exception):
    """
    Raised when a service encounters an error while attempting to uninstall a plugin
    """
