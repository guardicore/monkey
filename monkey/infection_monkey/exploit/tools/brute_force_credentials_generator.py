from itertools import chain
from typing import Dict, Iterable, List, Sequence, Set, Type

from common.credentials import Credentials, Identity, Secret


def generate_brute_force_credentials(
    input_credentials: Iterable[Credentials],
) -> Sequence[Credentials]:
    """
    Generates all possible combinations of identities and secrets from the inputs

    Given some Credentials objects, this function will generate all possible combinations of
    identities and secrets. The function will preserve "complete" credentials (i.e. both identity
    and secret are provided) and will put them first in the output sequence. This allows callers to
    prioritize using known identity/secret pairs before attempting to use random combinations.

    :param input_credentials: The credentials used to generate the brute force credentials
    :return: A Sequence of credentials
    """
    _input_credentials = set(input_credentials)
    brute_force_credentials = _generate_all_possible_combinations(_input_credentials)

    return _sort_known_identity_secret_pairs_first(brute_force_credentials, _input_credentials)


def _generate_all_possible_combinations(
    input_credentials: Set[Credentials],
) -> Iterable[Credentials]:
    brute_force_credentials: List[Credentials] = []
    identities: Dict[Type[Identity], Set[Identity]] = {}
    secrets: Dict[Type[Secret], Set[Secret]] = {}

    for credentials in input_credentials:
        if credentials.identity:
            identity_type = type(credentials.identity)
            identities.setdefault(identity_type, set()).add(credentials.identity)
        if credentials.secret:
            secret_type = type(credentials.secret)
            secrets.setdefault(secret_type, set()).add(credentials.secret)

    # Output will be grouped by secret type. This is not guaranteed by the interface, but if we can
    # arrange these in an orderly sequence, we might as well.
    for secret in chain.from_iterable(secrets.values()):
        for identity in chain.from_iterable(identities.values()):
            brute_force_credentials.append(Credentials(identity=identity, secret=secret))

    return brute_force_credentials


def _sort_known_identity_secret_pairs_first(
    brute_force_credentials: Iterable[Credentials], input_credentials: Set[Credentials]
) -> List[Credentials]:
    # If the credentials object constitutes a known complete identity/secret pair (i.e. it was
    # provided to us in the input), we want to put it first in the output sequence. This allows
    # known credentials to be prioritized over random combinations.
    return sorted(
        brute_force_credentials,
        key=lambda c: not (
            (c in input_credentials) and (c.identity is not None) and (c.secret is not None)
        ),
    )
