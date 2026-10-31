
import sys
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Add src folder to Python import path
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))
