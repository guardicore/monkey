from typing import Callable, Collection, TypeAlias

from common.credentials import Credentials
from common.types import Event

from .browser_credentials_database_path import BrowserCredentialsDatabasePath

CredentialsDatabaseSelectorCallable: TypeAlias = Callable[
    [], Collection[BrowserCredentialsDatabasePath]
]
CredentialsDatabaseProcessorCallable: TypeAlias = Callable[
    [Event, Collection[BrowserCredentialsDatabasePath]], Collection[Credentials]
]
