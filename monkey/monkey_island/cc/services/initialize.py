from pathlib import Path
from threading import Thread

from common import DIContainer
from monkey_island.cc.services import DirectoryFileStorageService, IFileStorageService, aws_service
from monkey_island.cc.services.post_breach_files import PostBreachFilesService
from monkey_island.cc.services.run_local_monkey import LocalMonkeyRunService

from . import AuthenticationService, JsonFileUserDatastore


def initialize_services(data_dir: Path) -> DIContainer:
    container = DIContainer()
    container.register_instance(
        IFileStorageService, DirectoryFileStorageService(data_dir / "custom_pbas")
    )

    # Takes a while so it's best to start it in the background
    Thread(target=aws_service.initialize, name="AwsService initialization", daemon=True).start()

    # This is temporary until we get DI all worked out.
    PostBreachFilesService.initialize(container.resolve(IFileStorageService))
    LocalMonkeyRunService.initialize(data_dir)
    AuthenticationService.initialize(data_dir, JsonFileUserDatastore(data_dir))

    return container
