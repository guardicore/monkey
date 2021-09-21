from dataclasses import dataclass
from typing import Callable, Type

import dpath.util

from monkey_island.cc.models.utils.field_types.field_type_abc import FieldTypeABC
from monkey_island.cc.models.utils.field_types.string_list import StringList


@dataclass
class SensitiveField:
    path: str
    path_separator = "."
    field_type: Type[FieldTypeABC]


sensitive_fields = [SensitiveField(path="overview.config_passwords", field_type=StringList)]


def encrypt(report: dict) -> dict:
    for sensitive_field in sensitive_fields:
        _apply_operation_to_report_field(
            report, sensitive_field, sensitive_field.field_type.encrypt
        )

    return report


def decrypt(report: dict) -> dict:
    for sensitive_field in sensitive_fields:
        _apply_operation_to_report_field(
            report, sensitive_field, sensitive_field.field_type.decrypt
        )
    return report


def _apply_operation_to_report_field(
    report: dict, sensitive_field: SensitiveField, operation: Callable
):
    field_value = dpath.util.get(report, sensitive_field.path, sensitive_field.path_separator, None)
    if field_value is None:
        raise Exception(
            f"Can't encrypt object because the path {sensitive_field.path} doesn't exist."
        )

    modified_value = operation(field_value)

    dpath.util.set(report, sensitive_field.path, modified_value, sensitive_field.path_separator)
