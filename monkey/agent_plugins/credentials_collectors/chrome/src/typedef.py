from pathlib import PurePath
from typing import Callable, Sequence, TypeAlias

from common.credentials import Credentials
from common.types import Event

CredentialsDatabaseSelectorCallable: TypeAlias = Callable[[None], Sequence[PurePath]]
CredentialsDatabaseProcessorCallable: TypeAlias = Callable[
    [Event, Sequence[PurePath]], Sequence[Credentials]
]
