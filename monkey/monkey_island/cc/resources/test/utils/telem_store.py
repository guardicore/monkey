from functools import wraps
from os import mkdir, path
import shutil
from datetime import datetime

from flask import request

from monkey_island.cc.models.test_telem import TestTelem
from monkey_island.cc.services.config import ConfigService

TEST_TELEM_DIR = "./test_telems"


class TestTelemStore:

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
        try:
            mkdir(TEST_TELEM_DIR)
        except FileExistsError:
            shutil.rmtree(TEST_TELEM_DIR)
            mkdir(TEST_TELEM_DIR)
        for test_telem in TestTelem.objects():
            with open(TestTelemStore.get_unique_file_path_for_test_telem(TEST_TELEM_DIR, test_telem), 'w') as file:
                file.write(test_telem.to_json())

    @staticmethod
    def get_unique_file_path_for_test_telem(target_dir: str, test_telem: TestTelem):
        telem_filename = TestTelemStore._get_filename_by_test_telem(test_telem)
        for i in range(100):
            potential_filepath = path.join(target_dir, (telem_filename + str(i)))
            if path.exists(potential_filepath):
                continue
            return potential_filepath

    @staticmethod
    def _get_filename_by_test_telem(test_telem: TestTelem):
        endpoint_part = test_telem.name
        return endpoint_part + '_' + test_telem.method


if __name__ == '__main__':
    TestTelemStore.export_test_telems()
