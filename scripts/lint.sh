#!/usr/bin/env bash

set -e
set -x

mypy app
black app --check
isort --recursive --check-only app
flake8
