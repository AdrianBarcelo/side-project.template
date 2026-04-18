#!/usr/bin/env bash
set -e

echo "Running black formatter..."
black .

echo "Running ruff linter..."
ruff check . --fix
