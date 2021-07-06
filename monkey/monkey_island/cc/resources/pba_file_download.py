import flask_restful
from flask import send_from_directory

from monkey_island.cc.services.post_breach_files import PostBreachFilesService


class PBAFileDownload(flask_restful.Resource):
    """
    File download endpoint used by monkey to download user's PBA file
    """

    # Used by monkey. can't secure.
    def get(self, filename):
        custom_pba_dir = PostBreachFilesService.get_custom_pba_directory()
        return send_from_directory(custom_pba_dir, filename)
