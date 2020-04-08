#!/usr/bin/env bash
set -e
cd "$(git rev-parse --show-toplevel)"
black . --check
flake8 .
python manage.py test
