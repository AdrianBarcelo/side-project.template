#!/usr/bin/env bash
set -x
pytest --junit-xml=junit.xml --cov-report term-missing:skip-covered --cov-report xml:coverage.xml --cov .
EXIT=$?
[ $EXIT -eq 0 ] || [ $EXIT -eq 5 ]  # exit 5 = no tests collected (valid for template)
