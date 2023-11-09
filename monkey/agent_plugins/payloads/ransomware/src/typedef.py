from pathlib import Path
from typing import Callable, Iterable, TypeAlias

FileEncryptorCallable: TypeAlias = Callable[[Path], None]
FileSelectorCallable: TypeAlias = Callable[[Path], Iterable[Path]]
ReadmeDropperCallable: TypeAlias = Callable[[Path, Path], None]
WallpaperChangerCallable: TypeAlias = Callable[[Path, Path], None]
