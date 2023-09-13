import logging
import os
import shutil
import sqlite3
import tempfile
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path

logger = logging.getLogger(__name__)

DB_SQL_STATEMENT = "SELECT username_value,password_value FROM logins"

ExtractedCredentialPair = tuple[str, bytes]
DatabaseReader = Callable[[Path], Iterator[ExtractedCredentialPair]]


def get_credentials_from_database(
    database_path: Path,
) -> Iterator[ExtractedCredentialPair]:
    if database_path.is_file():
        with temporary_file() as temporary_database_path:
            shutil.copy(database_path, temporary_database_path)
            yield from _extract_login_data(temporary_database_path)


@contextmanager
def temporary_file() -> Iterator[Path]:
    file, path = tempfile.mkstemp()
    os.close(file)
    try:
        yield Path(path)
    finally:
        os.remove(path)


def _extract_login_data(database_path: Path) -> Iterator[ExtractedCredentialPair]:
    try:
        conn = sqlite3.connect(database_path)
        for user, password in conn.execute(DB_SQL_STATEMENT):
            yield user, password
    except Exception:
        logger.exception("Error encounter while connecting to " f"database: {database_path}")
    finally:
        conn.close()
