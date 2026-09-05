import sys
from pathlib import Path

# Add backend/src to Python's path so `sih26155` package imports work
sys.path.insert(0, str(Path(__file__).parent / "backend" / "src"))