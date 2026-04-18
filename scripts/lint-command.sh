#!/usr/bin/env bash
set -e

echo "Checking typing..."
mypy .

echo "Checking ruff..."
ruff check .

echo "Checking black..."
black --check .
