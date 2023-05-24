import re

FILE_EXTENSION_REGEX = re.compile(r"^\.[^\\/]+$")


class FileExtension(str):
    def __init__(self, _):
        if not FILE_EXTENSION_REGEX.match(self):
            raise ValueError("Invalid file extension")
