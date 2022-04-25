from monkey_island.cc.services import DirectoryFileStorageService
from monkey_island.cc.services.post_breach_files import PostBreachFilesService
from monkey_island.cc.services.run_local_monkey import LocalMonkeyRunService

from . import AuthenticationService, JsonFileUserDatastore


def initialize_services(data_dir):
    # This is temporary until we get DI all worked out.
    PostBreachFilesService.initialize(DirectoryFileStorageService(data_dir / "custom_pbas"))

    LocalMonkeyRunService.initialize(data_dir)
    AuthenticationService.initialize(data_dir, JsonFileUserDatastore(data_dir))
