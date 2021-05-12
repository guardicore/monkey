from monkey_island.cc.services.post_breach_files import PostBreachFilesService
from monkey_island.cc.services.run_local_monkey import RunLocalMonkeyService


def initialize_services(data_dir):
    PostBreachFilesService.initialize(data_dir)
    RunLocalMonkeyService.initialize(data_dir)
