from monkey_island.cc.repositories.utils import AgentConfigurationSchemaCompiler


class AgentConfigurationSchemaService:
    """
    A service for retrieving the agent configuration schema.
    """

    def __init__(self, parser: AgentConfigurationSchemaCompiler):
        self.parser = parser

    def get_schema(self):
        """
        Get the Agent configuration schema.

        :return: Agent configuration schema
        :raises RuntimeError: If the schema could not be retrieved
        """
        return self.parser.get_schema()
