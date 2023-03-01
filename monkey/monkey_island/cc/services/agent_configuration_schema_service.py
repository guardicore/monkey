from monkey_island.cc.repositories.utils import AgentConfigurationSchemaCompiler


class AgentConfigurationSchemaService:
    """
    A service for retrieving the agent configuration schema.
    """

    def __init__(self, schema_compiler: AgentConfigurationSchemaCompiler):
        self._schema_compiler = schema_compiler

    def get_schema(self):
        """
        Get the Agent configuration schema.

        :return: Agent configuration schema
        :raises RuntimeError: If the schema could not be retrieved
        """
        return self._schema_compiler.get_schema()
