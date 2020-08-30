import json
import logging
from os import listdir, path
from typing import Dict, List

from tqdm import tqdm

TELEM_DIR_PATH = './tests/performance/telem_sample'
MAX_SAME_TYPE_TELEM_FILES = 10000
LOGGER = logging.getLogger(__name__)


class SampleFileParser:

    @staticmethod
    def save_teletries_to_files(telems: List[Dict]):
        for telem in (tqdm(telems, desc="Telemetries saved to files", position=3)):
            SampleFileParser.save_telemetry_to_file(telem)

    @staticmethod
    def save_telemetry_to_file(telem: Dict):
        telem_filename = telem['name'] + telem['method']
        for i in range(MAX_SAME_TYPE_TELEM_FILES):
            if not path.exists(path.join(TELEM_DIR_PATH, (str(i) + telem_filename))):
                telem_filename = str(i) + telem_filename
                break
        with open(path.join(TELEM_DIR_PATH, telem_filename), 'w') as file:
            file.write(json.dumps(telem))

    @staticmethod
    def read_telem_files() -> List[str]:
        telems = []
        try:
            file_paths = [path.join(TELEM_DIR_PATH, f) for f in listdir(TELEM_DIR_PATH)
                          if path.isfile(path.join(TELEM_DIR_PATH, f))]
        except FileNotFoundError:
            raise FileNotFoundError("Telemetries to send not found. "
                                    "Refer to readme to figure out how to generate telemetries and where to put them.")
        for file_path in file_paths:
            with open(file_path, 'r') as telem_file:
                telem_string = "".join(telem_file.readlines()).replace("\n", "")
                telems.append(telem_string)
        return telems

    @staticmethod
    def get_all_telemetries() -> List[Dict]:
        return [json.loads(t) for t in SampleFileParser.read_telem_files()]
