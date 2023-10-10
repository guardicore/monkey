from typing import Callable, Iterable

from monkeytypes import Credentials

from infection_monkey.propagation_credentials_repository import IPropagationCredentialsRepository


class BruteForceCredentialsProvider:
    """
    Provides credentials for brute-forcing propagation

    :param credentials_repository: A repository that provides credentials for propagation
    :param generate_brute_force_credentials: A function that generates credentials combinations
        for brute-forcing
    """

    def __init__(
        self,
        credentials_repository: IPropagationCredentialsRepository,
        generate_brute_force_credentials: Callable[[Iterable[Credentials]], Iterable[Credentials]],
    ) -> None:
        self._credentials_repository = credentials_repository
        self._generate_brute_force_credentials = generate_brute_force_credentials

    def __call__(self) -> Iterable[Credentials]:
        propagation_credentials = self._credentials_repository.get_credentials()
        for credentials in self._generate_brute_force_credentials(propagation_credentials):
            yield credentials
