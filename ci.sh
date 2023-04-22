#!/usr/bin/env bash
set -o errexit

# test end-user functions:
# TODO: find a better way to confirm that dev dependencies aren't necessary at runtime.

pip install flit
flit install --symlink
from-abc tests/cherrytree.abc --verbose # TODO: reenable pipe check

# test developer functions:

pip install -r requirements.txt
pip install -r requirements-dev.txt 

export PYTHONPATH="${PYTHONPATH}:concertina_helper"

pytest --verbose --doctest-modules \
       --cov=. --cov-fail-under=100 --cov-branch \
       --cov-report=html --cov-report=term-missing \
       --no-cov-on-fail

mypy concertina_helper

flake8

echo 'PASS!'

