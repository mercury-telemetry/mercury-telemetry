#!/usr/bin/env bash
set -e
cd "$(git rev-parse --show-toplevel)"
black --check mysite mercury
flake8 --exclude tests mysite/ mercury/
flake8 --ignore=E501 mercury/tests/
python3 manage.py test
