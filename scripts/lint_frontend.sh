#!/bin/sh

cd frontend || exit 1

pnpm install --force

if [ "$1" = "--fix" ]; then
    echo "Running linter with --fix!"
    pnpm format
else
    pnpm format:check
fi
