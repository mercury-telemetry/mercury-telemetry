#!/usr/bin/env bash
set -e
cd "$(git rev-parse --show-toplevel)"
black --check mysite mercury
flake8 mysite mercury
python3 manage.py test
