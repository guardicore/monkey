import inspect
from typing import Type

import monkeyevents


def _discover_builtin_agent_event_classes():
    discovered_agent_event_classes: list[Type[monkeyevents.AbstractAgentEvent]] = []

    for _, event_class in inspect.getmembers(monkeyevents, inspect.isclass):
        if event_class is monkeyevents.AbstractAgentEvent:
            continue

        if not issubclass(event_class, monkeyevents.AbstractAgentEvent):
            continue

        discovered_agent_event_classes.append(event_class)

    return discovered_agent_event_classes


BUILTIN_AGENT_EVENT_CLASSES = tuple(_discover_builtin_agent_event_classes())
