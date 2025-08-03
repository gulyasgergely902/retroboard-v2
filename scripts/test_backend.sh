#!/bin/sh

cd backend || exit 1
PYTHONPATH=. python3 -m coverage run --omit="tests/*" -m unittest discover -s tests -p "test_*.py"
python3 -m coverage report -m --fail-under 90
