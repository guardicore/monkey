from itertools import product
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
    cred_list = []
    for cred in product(usernames, passwords, [""], [""]):
        cred_list.append(cred)
    for cred in product(usernames, [""], lm_hashes, [""]):
        cred_list.append(cred)
    for cred in product(usernames, [""], [""], nt_hashes):
        cred_list.append(cred)
    return cred_list
