from monkey_island.cc.services.post_breach_files import PostBreachFilesService


def initialize_services(data_dir):
    initialize_post_breach_file_service(data_dir)


def initialize_post_breach_file_service(data_dir):
    PostBreachFilesService.initialize(data_dir)
