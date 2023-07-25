from dataclasses import dataclass


@dataclass
class PayloadResultData:
    run_success: bool = False
    error_message: str = ""
