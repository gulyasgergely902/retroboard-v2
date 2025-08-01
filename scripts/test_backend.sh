#!/bin/sh

cd backend || exit 1
python3 -m unittest discover -s tests -p "test_*.py"