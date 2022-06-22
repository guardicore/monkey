def should_propagate(config: dict, depth: int) -> bool:
    return config["config"]["depth"] > depth
