#!/usr/bin/env bash
set -o errexit

# end-user tests:
# TODO: find a better way to confirm that dev dependencies aren't necessary at runtime.
# https://github.com/mccalluc/concertina-helper/issues/23

pip install flit
flit install --symlink
from-abc tests/g-major.abc --layout_name wheatstone_cg --verbose
# TODO: reenable pipe check
# https://github.com/mccalluc/concertina-helper/issues/24

# developer tests:

pip install -r requirements.txt
pip install -r requirements-dev.txt 

pytest --verbose --doctest-modules \
       --cov=. --cov-fail-under=100 --cov-branch \
       --cov-report=html --cov-report=term-missing \
       --no-cov-on-fail

mypy concertina_helper --disallow-untyped-defs

flake8

echo 'PASS!'

