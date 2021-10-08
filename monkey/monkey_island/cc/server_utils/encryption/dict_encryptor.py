from dataclasses import dataclass
from typing import Callable, List, Type

import dpath.util

from .field_encryptors import IFieldEncryptor


class FieldNotFoundError(Exception):
    pass


@dataclass
class SensitiveField:
    path: str
    path_separator = "."
    field_encryptor: Type[IFieldEncryptor]


def encrypt_dict(sensitive_fields: List[SensitiveField], document_dict: dict) -> dict:
    for sensitive_field in sensitive_fields:
        _apply_operation_to_document_field(
            document_dict, sensitive_field, sensitive_field.field_encryptor.encrypt
        )

    return document_dict


def decrypt_dict(sensitive_fields: List[SensitiveField], document_dict: dict) -> dict:
    for sensitive_field in sensitive_fields:
        _apply_operation_to_document_field(
            document_dict, sensitive_field, sensitive_field.field_encryptor.decrypt
        )
    return document_dict


def _apply_operation_to_document_field(
    report: dict, sensitive_field: SensitiveField, operation: Callable
):
    field_value = dpath.util.get(report, sensitive_field.path, sensitive_field.path_separator, None)
    if field_value is None:
        raise FieldNotFoundError(
            f"Can't encrypt object because the path {sensitive_field.path} doesn't exist."
        )

    modified_value = operation(field_value)

    dpath.util.set(report, sensitive_field.path, modified_value, sensitive_field.path_separator)
