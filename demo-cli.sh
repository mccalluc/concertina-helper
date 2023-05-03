#!/usr/bin/env bash
set -o errexit

die() { set +v; echo "$*" 1>&2 ; exit 1; }

pip install flit
flit install --symlink
concertina-helper tests/g-major.abc --layout_name 30_wheatstone_cg --layout_transpose -2 --verbose

perl -ne 'print if /usage:/../```/ and ! /```/' README.md > /tmp/expected.txt
concertina-helper --help > /tmp/actual.txt
diff /tmp/expected.txt /tmp/actual.txt || die "Update CLI usage in README.md"

echo 'PASS!'

