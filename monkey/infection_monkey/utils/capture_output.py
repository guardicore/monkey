import io
import sys


class StdoutOutputCaptor:
    def __init__(self):
        _orig_stdout = None
        _new_stdout = None

    def capture_stdout_output(self) -> None:
        self._orig_stdout = sys.stdout
        self._new_stdout = io.StringIO()
        sys.stdout = self._new_stdout

    def get_captured_stdout_output(self) -> str:
        self._reset_stdout_to_original()
        self._new_stdout.seek(0)
        info = self._new_stdout.read()
        return info

    def _reset_stdout_to_original(self) -> None:
        sys.stdout = self._orig_stdout
