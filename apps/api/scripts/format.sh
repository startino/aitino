#!/usr/bin/env bash

set -e
set -x

# Sort imports one per line, so autoflake can remove unused imports
poetry run isort --force-single-line-imports .
poetry run autoflake --remove-all-unused-imports --remove-unused-variables --in-place . --exclude=__init__.py
poetry run black .
poetry run isort .
