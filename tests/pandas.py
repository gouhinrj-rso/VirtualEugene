import importlib.util
from pathlib import Path

# Load the project-level pandas stub so tests that run from the tests
# directory can still import ``pandas`` before modifying ``sys.path``.
_spec = importlib.util.spec_from_file_location(
    "pandas", Path(__file__).resolve().parents[1] / "pandas.py"
)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)

globals().update(_module.__dict__)
