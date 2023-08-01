from dataclasses import dataclass


@dataclass
class PayloadResult:
    success: bool = False
    error_message: str = ""
