import logging
from http import HTTPStatus

from flask import Response, make_response, request, send_file
from werkzeug.utils import secure_filename as sanitize_filename

from monkey_island.cc import repository
from monkey_island.cc.repository import IAgentConfigurationRepository, IFileRepository
from monkey_island.cc.resources.AbstractResource import AbstractResource
from monkey_island.cc.resources.request_authentication import jwt_required

logger = logging.getLogger(__file__)

# Front end uses these strings to identify which files to work with (linux or windows)
LINUX_PBA_TYPE = "PBAlinux"
WINDOWS_PBA_TYPE = "PBAwindows"


# NOTE: This resource will be reworked when the Custom PBA feature is rebuilt as a payload plugin.
class PBAFileUpload(AbstractResource):
    """
    File upload endpoint used to send/receive Custom PBA files
    """

    urls = [
        "/api/pba/upload/<string:target_os>",
        "/api/pba/upload/<string:target_os>?load=<string:filename>",
        "/api/pba/upload/<string:target_os>?restore=<string:filename>",
    ]

    def __init__(
        self,
        file_repository: IFileRepository,
        agent_configuration_repository: IAgentConfigurationRepository,
    ):
        self._file_repository = file_repository
        self._agent_configuration_repository = agent_configuration_repository

    # NOTE: None of these methods are thread-safe. Don't forget to fix that when this becomes a
    #       payload plugin.

    # This endpoint is basically a duplicate of PBAFileDownload.get(). They serve slightly different
    # purposes. This endpoint is authenticated, whereas the one in PBAFileDownload can not be (at
    # the present time). In the future, consider whether or not they should be merged, or if they
    # serve truly distinct purposes. After #2049, all endpoints that the agent uses will be
    # authenticated.
    @jwt_required
    def get(self, target_os):
        """
        Sends file to the requester
        :param target_os: Indicates which file to send, linux or windows
        :return: Returns file contents
        """
        if self._target_os_is_unsupported(target_os):
            return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY, mimetype="text/plain")

        agent_configuration = self._agent_configuration_repository.get_configuration()
        # Verify that file_name is indeed a file from config
        if target_os == LINUX_PBA_TYPE:
            filename = agent_configuration.custom_pbas.linux_filename
        else:
            filename = agent_configuration.custom_pbas.windows_filename

        try:
            file = self._file_repository.open_file(filename)

            # `send_file()` handles the closing of the open file.
            return send_file(file, mimetype="application/octet-stream")
        except repository.FileNotFoundError as err:
            logger.error(str(err))
            return make_response({"error": str(err)}, HTTPStatus.NOT_FOUND)

    # NOTE: Consider putting most of this functionality into a service when this is transformed into
    #       a payload plugin.
    @jwt_required
    def post(self, target_os):
        """
        Receives user's uploaded file
        :param target_os: Type indicates which file was received, linux or windows
        :return: Returns flask response object with uploaded file's filename
        """
        if self._target_os_is_unsupported(target_os):
            return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY, mimetype="text/plain")

        file_storage = next(request.files.values())  # For now, assume there's only one file
        safe_filename = sanitize_filename(file_storage.filename)

        self._file_repository.save_file(safe_filename, file_storage.stream)
        try:
            self._update_config(target_os, safe_filename)
        except Exception as err:
            # Roll back the entire transaction if part of it failed.
            self._file_storage.delete_file(safe_filename)
            raise err

        # API Spec: HTTP status code should be 201
        response = Response(response=safe_filename, status=HTTPStatus.OK, mimetype="text/plain")
        return response

    def _update_config(self, target_os: str, safe_filename: str):
        agent_configuration = self._agent_configuration_repository.get_configuration()

        if target_os == LINUX_PBA_TYPE:
            custom_pbas = agent_configuration.custom_pbas.copy(
                update={"linux_filename": safe_filename}
            )
        else:
            custom_pbas = agent_configuration.custom_pbas.copy(
                update={"windows_filename": safe_filename}
            )

        updated_agent_configuration = agent_configuration.copy(update={"custom_pbas": custom_pbas})
        self._agent_configuration_repository.store_configuration(updated_agent_configuration)

    @jwt_required
    def delete(self, target_os):
        """
        Deletes file that has been deleted on the front end
        :param target_os: Type indicates which file was deleted, linux of windows
        :return: Empty response
        """
        if self._target_os_is_unsupported(target_os):
            return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY, mimetype="text/plain")

        original_agent_configuration = self._agent_configuration_repository.get_configuration()
        self._update_config(target_os, "")

        if target_os == LINUX_PBA_TYPE:
            filename = original_agent_configuration.custom_pbas.linux_filename
        else:
            filename = original_agent_configuration.custom_pbas.windows_filename

        try:
            self._file_repository.delete_file(filename)
        except Exception as err:
            # Roll back the entire transaction if part of it failed.
            self._agent_configuration_repository.store_configuration(original_agent_configuration)
            raise err

        # API Spec: HTTP status code should be 204
        return make_response({}, HTTPStatus.OK)

    @staticmethod
    def _target_os_is_unsupported(target_os: str) -> bool:
        return target_os not in {LINUX_PBA_TYPE, WINDOWS_PBA_TYPE}
