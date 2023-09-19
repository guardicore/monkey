from uuid import UUID

import pytest

from common.agent_events import RAMConsumptionEvent

AGENT_ID = UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10")
TIMESTAMP = 1664371327.4067292
UTILIZATION = 77
BYTES_CONSUMED = 42 * (1024**3)  # 42 Gigabytes


def test_constructor():
    event = RAMConsumptionEvent(
        source=AGENT_ID, timestamp=TIMESTAMP, utilization=UTILIZATION, bytes=BYTES_CONSUMED
    )

    assert event.source == AGENT_ID
    assert event.timestamp == TIMESTAMP
    assert event.target is None
    assert len(event.tags) == 0
    assert event.utilization == UTILIZATION
    assert event.bytes == BYTES_CONSUMED


@pytest.mark.parametrize("invalid_utilization", ("not-an-int", -1, -5.0, None))
def test_invalid_utilization(invalid_utilization):
    with pytest.raises((ValueError, TypeError)):
        RAMConsumptionEvent(
            source=AGENT_ID,
            timestamp=TIMESTAMP,
            utilization=invalid_utilization,
            bytes=BYTES_CONSUMED,
        )


@pytest.mark.parametrize("invalid_bytes_consumed", ("not-an-int", -1, 5.2, None))
def test_invalid_ram_consumption(invalid_bytes_consumed):
    with pytest.raises((ValueError, TypeError)):
        RAMConsumptionEvent(
            source=AGENT_ID,
            timestamp=TIMESTAMP,
            utilization=UTILIZATION,
            bytes=invalid_bytes_consumed,
        )
