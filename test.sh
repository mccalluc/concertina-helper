#!/usr/bin/env bash
set -o errexit
set -o pipefail

export PYTHONPATH="${PYTHONPATH}:concertina_helper"

pytest --verbose --doctest-modules

mypy concertina_helper

flake8 && echo 'flake8 passes'

