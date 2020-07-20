# Workaround for packaging Monkey Island using PyInstaller. See https://github.com/oasis-open/cti-python-stix2/issues/218

import os

from PyInstaller.utils.hooks import get_module_file_attribute

stix2_dir = os.path.dirname(get_module_file_attribute('stix2'))
datas = [(stix2_dir, 'stix2')]
