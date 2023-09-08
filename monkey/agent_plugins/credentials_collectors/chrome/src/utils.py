from dataclasses import dataclass
from pathlib import PurePath
from typing import Optional


@dataclass
class BrowserCredentialsDatabasePath:
    database_file_path: PurePath
    master_key: Optional[bytes]
