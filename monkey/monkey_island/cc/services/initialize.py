from monkey_island.cc.services.authentication import AuthenticationService
from monkey_island.cc.services.post_breach_files import PostBreachFilesService
from monkey_island.cc.services.run_local_monkey import LocalMonkeyRunService


def initialize_services(data_dir):
    PostBreachFilesService.initialize(data_dir)
    LocalMonkeyRunService.initialize(data_dir)
    AuthenticationService.initialize(data_dir)
