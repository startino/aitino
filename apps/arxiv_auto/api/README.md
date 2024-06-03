# Installation
1. (nix-only) `nix-shell` into the shell.nix file
2. `poetry shell` to activate the virtual environment


# Use
- `poetry run python src/__init__.py` to run the stream script
- `poetry run uvicorn src:app` to run the API server
