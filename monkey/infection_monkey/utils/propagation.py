from common.configuration import AgentConfiguration


def should_propagate(config: AgentConfiguration, current_depth: int) -> bool:
    return config.propagation.maximum_depth > current_depth
