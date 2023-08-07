from uuid import UUID

import pytest

from common.agent_events import CPUConsumptionEvent

AGENT_ID = UUID("012e7238-7b81-4108-8c7f-0787bc3f3c10")
TIMESTAMP = 1664371327.4067292
UTILIZATION = 77
CPU_NUMBER = 3


def test_constructor():
    event = CPUConsumptionEvent(
        source=AGENT_ID, timestamp=TIMESTAMP, utilization=UTILIZATION, cpu_number=CPU_NUMBER
    )

    assert event.source == AGENT_ID
    assert event.timestamp == TIMESTAMP
    assert event.target is None
    assert len(event.tags) == 0
    assert event.utilization == UTILIZATION
    assert event.cpu_number == CPU_NUMBER


@pytest.mark.parametrize("invalid_utilization", ("not-an-int", -1, -5.0, None))
def test_invalid_utilization(invalid_utilization):
    with pytest.raises((ValueError, TypeError)):
        CPUConsumptionEvent(
            source=AGENT_ID,
            timestamp=TIMESTAMP,
            utilization=invalid_utilization,
            cpu_number=CPU_NUMBER,
        )


@pytest.mark.parametrize("invalid_cpu_number", ("not-an-int", -1, 5.2, None))
def test_invalid_cpu_number(invalid_cpu_number):
    with pytest.raises((ValueError, TypeError)):
        CPUConsumptionEvent(
            source=AGENT_ID,
            timestamp=TIMESTAMP,
            utilization=UTILIZATION,
            cpu_number=invalid_cpu_number,
        )
