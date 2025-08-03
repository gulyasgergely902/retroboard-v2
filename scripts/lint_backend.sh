#!/bin/sh

cd backend || exit 1

if [ "$1" = "--fix" ]; then
    echo "Running linter with --fix!"
    ruff check . --fix
    ruff format .
else
    ruff check .
    ruff format --check .
fi
