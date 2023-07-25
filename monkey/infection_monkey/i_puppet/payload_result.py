from dataclasses import dataclass


@dataclass
class PayloadResult:
    run_success: bool = False
    error_message: str = ""
