import io
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from tests.monkey_island import OpenErrorFileRepository, SingleFileRepository

from monkey_island.cc.repository import (
    FileAgentLogRepository,
    IAgentLogRepository,
    IFileRepository,
    RetrievalError,
    UnknownRecordError,
)

LOG_CONTENTS = "lots of useful information"
AGENT_ID = UUID("6bfd8b64-43d8-4449-8c70-d898aca74ad8")


@pytest.fixture
def repository() -> IAgentLogRepository:
    return FileAgentLogRepository(SingleFileRepository())


def test_store_agent_log(repository: IAgentLogRepository):
    repository.upsert_agent_log(AGENT_ID, LOG_CONTENTS)
    retrieved_log_contents = repository.get_agent_log(AGENT_ID)

    assert retrieved_log_contents == LOG_CONTENTS


def test_get_agent_log__unknown_record_error(repository: IAgentLogRepository):
    with pytest.raises(UnknownRecordError):
        repository.get_agent_log(AGENT_ID)


def test_get_agent_log__retrieval_error():
    repository = FileAgentLogRepository(OpenErrorFileRepository())
    with pytest.raises(RetrievalError):
        repository.get_agent_log(AGENT_ID)


def test_get_agent_log__corrupt_data():
    file_repository = MagicMock(spec=IFileRepository)
    # Return invalid unicode
    file_repository.open_file = MagicMock(return_value=io.BytesIO(b"\xff\xfe"))
    repository = FileAgentLogRepository(file_repository)

    with pytest.raises(RetrievalError):
        repository.get_agent_log(AGENT_ID)


def test_reset_agent_logs(repository: IAgentLogRepository):
    repository.upsert_agent_log(AGENT_ID, LOG_CONTENTS)
    repository.reset()
    with pytest.raises(UnknownRecordError):
        repository.get_agent_log(AGENT_ID)
