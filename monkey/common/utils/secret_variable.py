from typing import Any

from pydantic.types import SecretStr

from common.utils.i_secret_variable import ISecretVariable


class SecretVariable(ISecretVariable):
    def __init__(self, secret_value: Any):
        if isinstance(secret_value, str):
            self._secret_value = SecretStr(secret_value)
        else:
            raise NotImplementedError("SecretVariable only supports string values.")

    def get_secret_value(self) -> Any:
        return self._secret_value.get_secret_value()
