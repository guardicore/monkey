import logging

from monkey_island.cc.services import IFileStorageService

logger = logging.getLogger(__name__)


# TODO: This service wraps an IFileStorageService for the sole purpose of making the
#       `remove_PBA_files()` method available to the ConfigService. This whole service can be
#       removed once ConfigService is refactored to be stateful (it already is but everything is
#       still statically/globally scoped) and use dependency injection.
class PostBreachFilesService:
    _file_storage_service = None

    # TODO: A number of these services should be instance objects instead of
    # static/singleton hybrids. At the moment, this requires invasive refactoring that's
    # not a priority.
    @classmethod
    def initialize(cls, file_storage_service: IFileStorageService):
        cls._file_storage_service = file_storage_service

    @classmethod
    def remove_PBA_files(cls):
        cls._file_storage_service.delete_all_files()
