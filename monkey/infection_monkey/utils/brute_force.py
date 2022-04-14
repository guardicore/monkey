from itertools import chain, product
from typing import Any, Iterable, List, Mapping, Sequence, Tuple


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


def generate_username_password_or_ntlm_hash_combinations(
    usernames: Iterable[str],
    passwords: Iterable[str],
    lm_hashes: Iterable[str],
    nt_hashes: Iterable[str],
) -> Iterable[Tuple[str, str, str, str]]:
    """
    Generates all possible combinations of the following: username/password, username/lm_hash,
    username/nt_hash.
    :param usernames: An iterable containing usernames
    :param passwords: An iterable containing passwords
    :param lm_hashes: An iterable containing lm_hashes
    :param nt_hashes: An iterable containing nt_hashes
    :return: An iterable containing tuples of all possible credentials combinations. Note that each
    tuple will contain a username and at most one secret component (i.e. password, lm_hash,
    nt_hash). If usernames is empty, an empty iterator is returned. If all secret component
    iterators are empty, an empty iterator is returned.
    """
    return chain(
        product(usernames, passwords, [""], [""]),
        product(usernames, [""], lm_hashes, [""]),
        product(usernames, [""], [""], nt_hashes),
    )


def generate_brute_force_combinations(credentials: Mapping[str, Sequence[str]]):
    return generate_username_password_or_ntlm_hash_combinations(
        usernames=credentials["exploit_user_list"],
        passwords=credentials["exploit_password_list"],
        lm_hashes=credentials["exploit_lm_hash_list"],
        nt_hashes=credentials["exploit_ntlm_hash_list"],
    )


# Expects a list of username, password, lm hash and nt hash in that order
def get_credential_string(creds: List) -> str:
    cred_strs = [
        (creds[0], "username"),
        (creds[1], "password"),
        (creds[2], "lm hash"),
        (creds[3], "nt hash"),
    ]

    present_creds = [cred[1] for cred in cred_strs if cred[0]]
    return ", ".join(present_creds)
