from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, List, Type

import dpath.util

from monkey_island.cc.models.utils.field_types.field_type_abc import FieldTypeABC


@dataclass
class SensitiveField:
    path: str
    path_separator = "."
    field_type: Type[FieldTypeABC]


class DocumentEncryptor(ABC):
    @property
    @abstractmethod
    def sensitive_fields(self) -> List[SensitiveField]:
        pass

    @classmethod
    def encrypt(cls, document_dict: dict) -> dict:
        for sensitive_field in cls.sensitive_fields:
            DocumentEncryptor._apply_operation_to_document_field(
                document_dict, sensitive_field, sensitive_field.field_type.encrypt
            )

        return document_dict

    @classmethod
    def decrypt(cls, document_dict: dict) -> dict:
        for sensitive_field in cls.sensitive_fields:
            DocumentEncryptor._apply_operation_to_document_field(
                document_dict, sensitive_field, sensitive_field.field_type.decrypt
            )
        return document_dict

    @staticmethod
    def _apply_operation_to_document_field(
        report: dict, sensitive_field: SensitiveField, operation: Callable
    ):
        field_value = dpath.util.get(
            report, sensitive_field.path, sensitive_field.path_separator, None
        )
        if field_value is None:
            raise Exception(
                f"Can't encrypt object because the path {sensitive_field.path} doesn't exist."
            )

        modified_value = operation(field_value)

        dpath.util.set(report, sensitive_field.path, modified_value, sensitive_field.path_separator)
