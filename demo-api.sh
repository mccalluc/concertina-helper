#!/usr/bin/env bash
set -o errexit

die() { set +v; echo "$*" 1>&2 ; exit 1; }

pip install -r requirements.txt
pip install -r requirements-dev.txt 

pytest --verbose --doctest-modules \
       --cov=. --cov-fail-under=100 --cov-branch \
       --cov-report=html --cov-report=term-missing \
       --no-cov-on-fail

mypy concertina_helper --disallow-untyped-defs

flake8

echo 'PASS!'
