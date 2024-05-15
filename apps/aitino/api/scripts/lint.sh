#!/usr/bin/env bash

set -e
set -x

mypy .
black . --check
isort --recursive --check-only .
flake8
