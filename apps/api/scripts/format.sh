#!/usr/bin/env bash

set -e
set -x

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports .
autoflake --remove-all-unused-imports --remove-unused-variables --in-place . --exclude=__init__.py
black .
isort .
