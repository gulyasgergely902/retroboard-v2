#!/bin/sh

cd backend || exit 1
ruff check .
ruff format --check .
