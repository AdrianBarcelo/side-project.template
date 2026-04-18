#!/usr/bin/env bash
set -ex
pytest --junit-xml=junit.xml --cov-report term-missing:skip-covered --cov-report xml:coverage.xml --cov .
