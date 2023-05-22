#!/usr/bin/env bash
set -o errexit

die() { set +v; echo "$*" 1>&2 ; exit 1; }

pip install flit
flit install --symlink
concertina-helper tests/g-major.abc \
  --layout_name 30_wheatstone_cg \
  --layout_transpose -2 \
  --output_format LONG \
  --input_format ABC

perl -ne 'print if /usage:/../```/ and ! /```/' README.md > /tmp/expected.txt
ACTUAL=/tmp/actual.txt
concertina-helper --help > $ACTUAL
diff /tmp/expected.txt $ACTUAL || die "Update CLI usage in README.md with $ACTUAL"

echo 'PASS!'

