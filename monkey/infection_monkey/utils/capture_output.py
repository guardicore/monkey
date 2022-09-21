from __future__ import annotations

import io
import sys


class StdoutCapture:
    def __enter__(self) -> StdoutCapture:
        self._orig_stdout = sys.stdout
        self._new_stdout = io.StringIO()
        sys.stdout = self._new_stdout
        return self

    def get_captured_stdout_output(self) -> str:
        self._new_stdout.seek(0)
        output = self._new_stdout.read()
        return output

    def __exit__(self, _, __, ___) -> None:
        sys.stdout = self._orig_stdout
