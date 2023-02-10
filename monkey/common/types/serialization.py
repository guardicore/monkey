from typing import Dict, List, Union

JSONSerializable = Union[  # type: ignore[misc]
    Dict[str, "JSONSerializable"],  # type: ignore[misc]
    List["JSONSerializable"],  # type: ignore[misc]
    int,
    str,
    float,
    bool,
    None,
]
