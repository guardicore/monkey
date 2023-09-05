from pathlib import PurePath
from typing import Callable, Sequence, TypeAlias

from common.credentials import Credentials

CredentialsDatabaseSelectorCallable: TypeAlias = Callable[[None], Sequence[PurePath]]
CredentialsDatabaseProcessorCallable: TypeAlias = Callable[
    [Sequence[PurePath]], Sequence[Credentials]
]
