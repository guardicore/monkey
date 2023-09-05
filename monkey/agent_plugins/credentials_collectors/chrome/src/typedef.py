from typing import Callable, TypeAlias

CredentialsDatabaseSelectorCallable: TypeAlias = Callable[[None], None]
CredentialsDatabaseProcessorCallable: TypeAlias = Callable[[None], None]
