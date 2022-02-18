from itertools import chain, product
from typing import Any, Iterable, Tuple


def generate_identity_secret_pairs(
    identities: Iterable, secrets: Iterable
) -> Iterable[Tuple[Any, Any]]:
    return product(identities, secrets)


def generate_username_password_or_ntlm_hash_combinations(
    usernames: Iterable[str],
    passwords: Iterable[str],
    lm_hashes: Iterable[str],
    nt_hashes: Iterable[str],
) -> Iterable[Tuple[str, str, str, str]]:
    """
    Returns all combinations of the configurations users and passwords or lm/ntlm hashes
    :return:
    """
    return chain(
        product(usernames, passwords, [""], [""]),
        product(usernames, [""], lm_hashes, [""]),
        product(usernames, [""], [""], nt_hashes),
    )
