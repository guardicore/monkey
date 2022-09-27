from itertools import count
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from common.agent_events import PingScanEvent
from common.types import PingScanData
from monkey_island.cc.agent_event_handlers import handle_scan_data
from monkey_island.cc.repository import (
    IAgentRepository,
    IMachineRepository,
    INodeRepository,
    RetrievalError,
    StorageError,
    UnknownRecordError,
)

SEED_ID = 99


@pytest.fixture
def agent_repository() -> IAgentRepository:
    agent_repository = MagicMock(spec=IAgentRepository)
    agent_repository.upsert_agent = MagicMock()
    return agent_repository


@pytest.fixture
def machine_repository() -> IMachineRepository:
    machine_repository = MagicMock(spec=IMachineRepository)
    machine_repository.get_new_id = MagicMock(side_effect=count(SEED_ID))
    machine_repository.upsert_machine = MagicMock()
    return machine_repository


@pytest.fixture
def node_repository() -> INodeRepository:
    node_repository = MagicMock(spec=INodeRepository)
    node_repository.upsert_communication = MagicMock()
    return node_repository


@pytest.fixture
def handler() -> handle_scan_data:
    return handle_scan_data(agent_repository, machine_repository, node_repository)


def test_handle_scan_data__upserts_machine(handler: handle_scan_data):
    pass


def test_handle_scan_data__upserts_node(handler: handle_scan_data):
    pass


def test_handle_scan_data__node_not_upserted_if_no_matching_agent(handler: handle_scan_data):
    pass


def test_handle_scan_data__node_not_upserted_if_no_matching_machine(handler: handle_scan_data):
    pass


def test_handle_scan_data__upserts_machine_if_did_not_exist(handler: handle_scan_data):
    pass
