import json
from enum import Enum

from flask import make_response, request

from common.credentials import Credentials, LMHash, NTHash, Password, SSHKeypair, Username
from monkey_island.cc.repository import ICredentialsRepository
from monkey_island.cc.repository.errors import StorageError
from monkey_island.cc.resources.AbstractResource import AbstractResource


class UnknownCredentialTypeError(Exception):
    pass


class PropagationCredentialsType(Enum):
    STOLEN = "stolen"
    CONFIGURED = "configured"


class PropagationCredentials(AbstractResource):
    urls = ["/api/propagation-credentials"]

    def __init__(self, credentials_repository: ICredentialsRepository):
        self._credentials_repository = credentials_repository

    def get(self):
        propagation_credentials = self._credentials_repository.get_all_credentials()

        return make_response({"propagation_credentials": propagation_credentials})

    def post(self):
        body = json.loads(request.data)

        credentials = body.get("credentials")
        if credentials:
            try:
                credentials_object = PropagationCredentials._create_credentials_object(credentials)
            except Exception as exc:
                return make_response({"error": f"Couldn't create 'Credentials' object: {exc}"}, 400)

            try:
                if body.get("type") == PropagationCredentialsType.STOLEN:
                    self._credentials_repository.save_stolen_credentials(credentials_object)
                elif body.get("type") == PropagationCredentialsType.CONFIGURED:
                    self._credentials_repository.save_configured_credentials(credentials_object)
            except StorageError as err:
                return make_response(
                    {"error": f"Error encountered while storing credentials: {err}"}, 400
                )

        return make_response({}, 200)

    @staticmethod
    def _create_credentials_object(credentials: dict) -> Credentials:
        identities = []
        secrets = []

        usernames = credentials.get("usernames", [])
        for username in usernames:
            identities.append(Username(username))

        passwords = credentials.get("passwords", [])
        for password in passwords:
            secrets.append(Password(password))

        nt_hashes = credentials.get("nt_hashes", [])
        for nt_hash in nt_hashes:
            secrets.append(NTHash(nt_hash))

        lm_hashes = credentials.get("lm_hashes", [])
        for lm_hash in lm_hashes:
            secrets.append(LMHash(lm_hash))

        ssh_keypairs = credentials.get("ssh_keypairs", [])
        for ssh_keypair in ssh_keypairs:
            private_key = ssh_keypair.get("private_key", "")
            public_key = ssh_keypair.get("public_key", "")
            secrets.append(SSHKeypair(private_key, public_key))

        return Credentials(identities, secrets)
