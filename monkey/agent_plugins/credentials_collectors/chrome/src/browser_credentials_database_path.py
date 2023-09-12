from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class BrowserCredentialsDatabasePath:
    database_file_path: Path
    master_key: Optional[bytes]
