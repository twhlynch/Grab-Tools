#!/usr/bin/env bash

set -euo pipefail

echo "Generating protobuf types (pnpm proto)..."
pnpm proto

read -r -p "Press enter to run helpers (Ctrl+C to abort)... "

echo "Generating helpers (pnpm helpers)..."
pnpm helpers

read -r -p "Press enter to run nodes (Ctrl+C to abort)... "

echo "Generating node builders (pnpm nodes)..."
pnpm nodes

echo "Done."
