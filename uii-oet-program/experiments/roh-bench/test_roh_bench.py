from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from run_experiment import run_world

def test_reproducibility():
    assert run_world(1, 12345) == run_world(1, 12345)

def test_schema():
    result = run_world(0, 1).__dict__
    required = {
        "world_id", "seed", "hidden_rule", "fixed_success",
        "adaptive_success", "developmental_success",
        "fixed_classes", "adaptive_classes", "developmental_classes",
    }
    assert required.issubset(result)
