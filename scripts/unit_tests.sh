#!/bin/bash
set -euo pipefail

python3 -m pip install -e .[dev]
black --check .
pytest -v
