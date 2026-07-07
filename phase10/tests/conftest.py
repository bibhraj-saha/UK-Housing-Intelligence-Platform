from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PHASE10_SRC = (
    PROJECT_ROOT
    / "phase10"
    / "src"
)

if str(PHASE10_SRC) not in sys.path:
    sys.path.insert(
        0,
        str(PHASE10_SRC),
    )