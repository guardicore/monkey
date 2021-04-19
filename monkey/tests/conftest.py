import sys
from pathlib import Path

MONKEY_BASE_PATH = str(Path(__file__).parent.parent)
sys.path.insert(0, MONKEY_BASE_PATH)
