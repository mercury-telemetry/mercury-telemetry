#!/usr/bin/env bash

cd "$(git rev-parse --show-toplevel)"
black --check mysite mercury
flake8 mysite mercury
