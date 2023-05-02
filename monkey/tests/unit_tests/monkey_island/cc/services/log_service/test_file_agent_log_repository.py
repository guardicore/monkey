import io
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from tests.monkey_island import InMemoryFileRepository, OpenErrorFileRepository

from monkey_island.cc.repositories import IFileRepository, RetrievalError, UnknownRecordError
from monkey_island.cc.services.log_service import IAgentLogRepository
from monkey_island.cc.services.log_service.file_agent_log_repository import FileAgentLogRepository

LOG_CONTENTS = "lots of useful information"
AGENT_ID_1 = UUID("6bfd8b64-43d8-4449-8c70-d898aca74ad8")
AGENT_ID_2 = UUID("789abcd4-20d7-abcd-ef7a-0123acaabcde")


@pytest.fixture
def repository() -> IAgentLogRepository:
    return FileAgentLogRepository(InMemoryFileRepository())


def test_store_agent_log(repository: IAgentLogRepository):
    repository.upsert_agent_log(AGENT_ID_1, LOG_CONTENTS)
    retrieved_log_contents = repository.get_agent_log(AGENT_ID_1)

    assert retrieved_log_contents == LOG_CONTENTS


def test_get_agent_log__unknown_record_error(repository: IAgentLogRepository):
    with pytest.raises(UnknownRecordError):
        repository.get_agent_log(AGENT_ID_1)


def test_get_agent_log__retrieval_error():
    repository = FileAgentLogRepository(OpenErrorFileRepository())
    with pytest.raises(RetrievalError):
        repository.get_agent_log(AGENT_ID_1)


def test_get_agent_log__corrupt_data():
    file_repository = MagicMock(spec=IFileRepository)
    # Return invalid unicode
    file_repository.open_file = MagicMock(return_value=io.BytesIO(b"\xff\xfe"))
    repository = FileAgentLogRepository(file_repository)

    with pytest.raises(RetrievalError):
        repository.get_agent_log(AGENT_ID_1)


def test_multiple_logs(repository: IAgentLogRepository):
    log_contents_1 = "hello"
    log_contents_2 = "world"

    repository.upsert_agent_log(AGENT_ID_1, log_contents_1)
    repository.upsert_agent_log(AGENT_ID_2, log_contents_2)

    assert repository.get_agent_log(AGENT_ID_1) == log_contents_1
    assert repository.get_agent_log(AGENT_ID_2) == log_contents_2


def test_reset_agent_logs(repository: IAgentLogRepository):
    repository.upsert_agent_log(AGENT_ID_1, LOG_CONTENTS)
    repository.reset()
    with pytest.raises(UnknownRecordError):
        repository.get_agent_log(AGENT_ID_1)
