#!/usr/bin/env bash
set -o errexit

export PYTHONPATH="${PYTHONPATH}:concertina_helper"

pytest --verbose --doctest-modules \
       --cov=. --cov-report=html --cov-fail-under=100 --cov-branch

mypy concertina_helper

flake8

flit install --symlink

from-abc tests/cherrytree.abc --verbose | head

echo 'PASS!'

