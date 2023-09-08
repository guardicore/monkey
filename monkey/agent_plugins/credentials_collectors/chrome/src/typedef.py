from typing import Callable, Collection, TypeAlias

from common.credentials import Credentials
from common.types import Event

from .utils import BrowserCredentialsDatabasePath

CredentialsDatabaseSelectorCallable: TypeAlias = Callable[
    [], Collection[BrowserCredentialsDatabasePath]
]
CredentialsDatabaseProcessorCallable: TypeAlias = Callable[
    [Event, Collection[BrowserCredentialsDatabasePath]], Collection[Credentials]
]
