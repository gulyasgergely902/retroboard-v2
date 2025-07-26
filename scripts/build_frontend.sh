#!/bin/sh

cd ../frontend || exit 1
pnpm install --force
pnpm format:check
pnpm build
