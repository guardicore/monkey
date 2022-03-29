import enum
import json
from typing import Dict, Iterable

from common.common_consts.telem_categories import TelemCategoryEnum
from infection_monkey.i_puppet.credential_collection import Credentials, ICredentialComponent
from infection_monkey.telemetry.base_telem import BaseTelem


class CredentialsTelem(BaseTelem):
    telem_category = TelemCategoryEnum.CREDENTIALS

    def __init__(self, credentials: Iterable[Credentials]):
        """
        Used to send information about stolen or discovered credentials to the Island.
        :param credentials: An iterable containing credentials to be sent to the Island.
        """
        self._credentials = credentials

    @property
    def credentials(self) -> Iterable[Credentials]:
        return iter(self._credentials)

    def send(self, log_data=True):
        super().send(log_data=False)

    def get_data(self) -> Dict:
        # TODO: At a later time we can consider factoring this into a Serializer class or similar.
        return json.loads(json.dumps(self._credentials, default=_serialize))


def _serialize(obj):
    if isinstance(obj, enum.Enum):
        return obj.name

    if isinstance(obj, ICredentialComponent):
        # This is a workaround for ICredentialComponents that are implemented as dataclasses. If the
        # credential_type attribute is populated with `field(init=False, ...)`, then credential_type
        # is not added to the object's __dict__ attribute. The biggest risk of this workaround is
        # that we might change the name of the credential_type field in ICredentialComponents, but
        # automated refactoring tools would not detect that this string needs to change. This is
        # mittigated by the call to getattr() below, which will raise an AttributeException if the
        # attribute name changes and a unit test will fail under these conditions.
        credential_type = getattr(obj, "credential_type")
        return dict(obj.__dict__, **{"credential_type": credential_type})

    return getattr(obj, "__dict__", str(obj))
