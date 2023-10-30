from typing import Callable
from unittest.mock import MagicMock

import pytest
from agent_plugins.payloads.cryptojacker.src.memory_utilizer import (
    MEMORY_CONSUMPTION_SAFETY_LIMIT,
    MemoryUtilizer,
)
from monkeytypes import PercentLimited

from common.event_queue import IAgentEventPublisher
from common.types import AgentID

AGENT_ID = AgentID("9614480d-471b-4568-86b5-cb922a34ed8a")
TARGET_UTILIZATION = PercentLimited(50)
TARGET_UTILIZATION_BYTES = 4 * 1024 * 1024  # 4 MB


class MockMemoryInfo:
    def __init__(self, vms: int):
        self.vms = vms


class MockProcess:
    def __init__(self, memory_info: MockMemoryInfo):
        self._memory_info = memory_info

    def memory_info(self):
        return self._memory_info


class MockSystemVirtualMemory:
    def __init__(self, total: int, available: int):
        self.total = total
        self.available = available


@pytest.fixture
def mock_agent_event_publisher() -> IAgentEventPublisher:
    return MagicMock(spec=IAgentEventPublisher)


@pytest.fixture
def memory_utilizer(mock_agent_event_publisher) -> MemoryUtilizer:
    return MemoryUtilizer(TARGET_UTILIZATION, AGENT_ID, mock_agent_event_publisher)


def set_system_virtual_memory(
    monkeypatch, total_virtual_memory: int, available_virtual_memory: int
):
    monkeypatch.setattr(
        "agent_plugins.payloads.cryptojacker.src.memory_utilizer.psutil.virtual_memory",
        lambda: MockSystemVirtualMemory(total_virtual_memory, available_virtual_memory),
    )


def set_consumed_virtual_memory(monkeypatch, vms: int):
    monkeypatch.setattr(
        "agent_plugins.payloads.cryptojacker.src.memory_utilizer.psutil.Process",
        lambda: MockProcess(MockMemoryInfo(vms)),
    )


@pytest.mark.parametrize(
    "parent_process_consumed_virtual_memory",
    (
        0,
        int(TARGET_UTILIZATION_BYTES / 1),
        int(TARGET_UTILIZATION_BYTES / 2),
        int(TARGET_UTILIZATION_BYTES / 4),
    ),
)
def test_adjust_memory_utilization__raise_to_target(
    monkeypatch: Callable,
    memory_utilizer: MemoryUtilizer,
    parent_process_consumed_virtual_memory: int,
):
    set_consumed_virtual_memory(monkeypatch, parent_process_consumed_virtual_memory)

    total_virtual_memory = int(TARGET_UTILIZATION_BYTES / TARGET_UTILIZATION.as_decimal_fraction())
    set_system_virtual_memory(monkeypatch, total_virtual_memory, total_virtual_memory)

    memory_utilizer.adjust_memory_utilization()
    assert memory_utilizer.consumed_bytes_size == (
        TARGET_UTILIZATION_BYTES - parent_process_consumed_virtual_memory
    )


@pytest.mark.parametrize(
    "parent_process_consumed_virtual_memory",
    (
        0,
        int(TARGET_UTILIZATION_BYTES / 2),
        int(TARGET_UTILIZATION_BYTES / 4),
    ),
)
def test_adjust_memory_utilization__drop_to_target(
    monkeypatch: Callable,
    memory_utilizer: MemoryUtilizer,
    mock_agent_event_publisher: IAgentEventPublisher,
    parent_process_consumed_virtual_memory: int,
):
    consumed_bytes = int(TARGET_UTILIZATION_BYTES * 1.5)
    set_consumed_virtual_memory(
        monkeypatch, parent_process_consumed_virtual_memory + consumed_bytes
    )

    total_virtual_memory = int(TARGET_UTILIZATION_BYTES / TARGET_UTILIZATION.as_decimal_fraction())
    set_system_virtual_memory(monkeypatch, total_virtual_memory, total_virtual_memory)

    # Instruct the memory utilizer to use more than the target so we can test its ability to reduce
    # its memory consumption
    memory_utilizer.consume_bytes(consumed_bytes)

    # Adjust memory utilization so that the memory utilizer is consuming the appropriate amount of
    # memory
    memory_utilizer.adjust_memory_utilization()

    assert memory_utilizer.consumed_bytes_size == (
        TARGET_UTILIZATION_BYTES - parent_process_consumed_virtual_memory
    )
    assert mock_agent_event_publisher.publish.called


def test_adjust_memory_utilization__parent_process_over_limit(
    monkeypatch: Callable,
    memory_utilizer: MemoryUtilizer,
):
    parent_process_consumed_virtual_memory = int(TARGET_UTILIZATION_BYTES * 1.25)
    set_consumed_virtual_memory(monkeypatch, parent_process_consumed_virtual_memory)

    total_virtual_memory = int(TARGET_UTILIZATION_BYTES / TARGET_UTILIZATION.as_decimal_fraction())
    set_system_virtual_memory(monkeypatch, total_virtual_memory, total_virtual_memory)

    # Adjust memory utilization so that the memory utilizer is consuming some memory
    memory_utilizer.adjust_memory_utilization()

    assert memory_utilizer.consumed_bytes_size == 0


def test_adjust_memory_utilization__used_gt_total(
    monkeypatch: Callable,
    memory_utilizer: MemoryUtilizer,
    mock_agent_event_publisher: IAgentEventPublisher,
):
    total_virtual_memory = 1024
    set_system_virtual_memory(monkeypatch, total_virtual_memory, total_virtual_memory)
    set_consumed_virtual_memory(monkeypatch, total_virtual_memory * 2)

    memory_utilizer.adjust_memory_utilization()

    assert memory_utilizer.consumed_bytes_size == 0
    assert not mock_agent_event_publisher.publish.called


@pytest.mark.parametrize(
    "parent_process_consumed_virtual_memory,expected_consumed_bytes_size",
    (
        (0, 1509949),
        (int(TARGET_UTILIZATION_BYTES / 2), 1300234),
        (int(TARGET_UTILIZATION_BYTES / 4), 1405091),
    ),
)
def test_adjust_memory_utilization__limits(
    monkeypatch: Callable,
    memory_utilizer: MemoryUtilizer,
    mock_agent_event_publisher: IAgentEventPublisher,
    parent_process_consumed_virtual_memory: int,
    expected_consumed_bytes_size: int,
):
    set_consumed_virtual_memory(monkeypatch, parent_process_consumed_virtual_memory)

    total_virtual_memory = int(TARGET_UTILIZATION_BYTES / TARGET_UTILIZATION.as_decimal_fraction())
    available_virtual_memory = total_virtual_memory * 0.2
    set_system_virtual_memory(monkeypatch, total_virtual_memory, available_virtual_memory)

    memory_utilizer.adjust_memory_utilization()

    assert memory_utilizer.consumed_bytes_size == expected_consumed_bytes_size
    assert mock_agent_event_publisher.publish.called, MEMORY_CONSUMPTION_SAFETY_LIMIT


def test_consume_bytes__publishes_event(
    memory_utilizer: MemoryUtilizer,
    mock_agent_event_publisher: IAgentEventPublisher,
):
    memory_utilizer.consume_bytes(1)
    assert mock_agent_event_publisher.publish.call_count == 1


@pytest.mark.parametrize(
    "bytes_to_consume_1,bytes_to_consume_2,expected_publish_count",
    ((0, 0, 0), (1024, 1025, 1), (1024, 1023, 1)),
)
def test_consume_bytes__no_change_publishes_no_event(
    memory_utilizer: MemoryUtilizer,
    mock_agent_event_publisher: IAgentEventPublisher,
    bytes_to_consume_1: int,
    bytes_to_consume_2: int,
    expected_publish_count: int,
):
    memory_utilizer.consume_bytes(bytes_to_consume_1)
    memory_utilizer.consume_bytes(bytes_to_consume_2)

    assert mock_agent_event_publisher.publish.call_count == expected_publish_count


@pytest.mark.parametrize(
    "bytes_to_consume_1,bytes_to_consume_2,expected_publish_count",
    ((0, 1, 1), (1, 0, 2), (0, 1025, 1), (1024, 2048, 2)),
)
def test_consume_bytes__change_publishes_event(
    memory_utilizer: MemoryUtilizer,
    mock_agent_event_publisher: IAgentEventPublisher,
    bytes_to_consume_1: int,
    bytes_to_consume_2: int,
    expected_publish_count: int,
):
    memory_utilizer.consume_bytes(bytes_to_consume_1)
    memory_utilizer.consume_bytes(bytes_to_consume_2)

    assert mock_agent_event_publisher.publish.call_count == expected_publish_count
