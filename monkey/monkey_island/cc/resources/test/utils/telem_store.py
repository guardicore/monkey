import logging
import shutil
from datetime import datetime
from functools import wraps
from os import mkdir, path

from flask import request

from monkey_island.cc.models.test_telem import TestTelem
from monkey_island.cc.services.config import ConfigService

TELEM_SAMPLE_DIR = "./telem_sample"
MAX_SAME_CATEGORY_TELEMS = 10000


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestTelemStore:

    TELEMS_EXPORTED = False

    @staticmethod
    def store_test_telem(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if ConfigService.is_test_telem_export_enabled():
                time = datetime.now()
                method = request.method
                content = request.data.decode()
                endpoint = request.path
                name = str(request.url_rule).replace('/', '_').replace('<', '_').replace('>', '_').replace(':', '_')
                TestTelem(name=name, method=method, endpoint=endpoint, content=content, time=time).save()
            return f(*args, **kwargs)

        return decorated_function

    @staticmethod
    def export_test_telems():
        logger.info(f"Exporting all telemetries to {TELEM_SAMPLE_DIR}")
        try:
            mkdir(TELEM_SAMPLE_DIR)
        except FileExistsError:
            logger.info("Deleting all previous telemetries.")
            shutil.rmtree(TELEM_SAMPLE_DIR)
            mkdir(TELEM_SAMPLE_DIR)
        for test_telem in TestTelem.objects():
            with open(TestTelemStore.get_unique_file_path_for_test_telem(TELEM_SAMPLE_DIR, test_telem), 'w') as file:
                file.write(test_telem.to_json(indent=2))
        TestTelemStore.TELEMS_EXPORTED = True
        logger.info("Telemetries exported!")

    @staticmethod
    def get_unique_file_path_for_test_telem(target_dir: str, test_telem: TestTelem):
        telem_filename = TestTelemStore._get_filename_by_test_telem(test_telem)
        for i in range(MAX_SAME_CATEGORY_TELEMS):
            potential_filepath = path.join(target_dir, (telem_filename + str(i)))
            if path.exists(potential_filepath):
                continue
            return potential_filepath
        raise Exception(f"Too many telemetries of the same category. Max amount {MAX_SAME_CATEGORY_TELEMS}")

    @staticmethod
    def _get_filename_by_test_telem(test_telem: TestTelem):
        endpoint_part = test_telem.name
        return endpoint_part + '_' + test_telem.method


if __name__ == '__main__':
    TestTelemStore.export_test_telems()
