def should_propagate(config: dict, current_depth: int) -> bool:
    return config["config"]["depth"] > current_depth
