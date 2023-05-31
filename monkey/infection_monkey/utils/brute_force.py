from itertools import product
from typing import Any, Iterable, Tuple


def generate_identity_secret_pairs(
    identities: Iterable, secrets: Iterable
) -> Iterable[Tuple[Any, Any]]:
    """
    Generates all possible combinations of identities and secrets (e.g. usernames and passwords).
    :param identities: An iterable containing identity components of a credential pair
    :param secrets: An iterable containing secret components of a credential pair
    :return: An iterable of all combinations of identity/secret pairs. If either identities or
             secrets is empty, an empty iterator is returned.
    """
    return product(identities, secrets)
