import io

from monkeytypes import OperatingSystem

from monkey_island.cc.services.agent_binary_service.i_agent_binary_repository import (
    IAgentBinaryRepository,
)

LINUX_AGENT_BINARY = b"linux_binary"
WINDOWS_AGENT_BINARY = b"windows_binary"


class InMemoryAgentBinaryRepository(IAgentBinaryRepository):
    def __init__(self):
        self.agent_binaries = {
            OperatingSystem.LINUX: LINUX_AGENT_BINARY,
            OperatingSystem.WINDOWS: WINDOWS_AGENT_BINARY,
        }

    def get_agent_binary(self, operating_system: OperatingSystem):
        return io.BytesIO(self.agent_binaries[operating_system])
