#!/usr/bin/env bash
set -o errexit

die() { set +v; echo "$*" 1>&2 ; exit 1; }

expect_equal() {
  MESSAGE="$1"
  shift
  diff -c $@ || die "Expected $MESSAGE to be equal!"
}

# pip install flit
# flit install --symlink

expect_equal 'documentation' \
<( perl -ne 'print if /usage:/../```/ and ! /```/' README.md ) \
<( concertina-helper --help )

# TODO: Non deterministic!

# expect_equal 'defaults' \
# <( concertina-helper tests/g-major.abc --layout_name 30_wheatstone_cg | head ) \
# <( echo "Measure 1 - G4
# PUSH:
# --- --- --- --- ---    --- --- --- --- ---
# --- --- --- --- ---    --- --- --- --- ---
# --- --- G4  --- ---    --- --- --- --- ---
# Measure 1 - A4
# PUSH:
# --- --- --- A4  ---    --- --- --- --- ---
# --- --- --- --- ---    --- --- --- --- ---
# --- --- --- --- ---    --- --- --- --- ---" )

# expect_equal 'options' \
# <( concertina-helper tests/g-major.abc \
#    --layout_path concertina_helper/layouts/30_jefferies_cg.yaml \
#    --layout_transpose 2 \
#    --format ascii \
#    --bellows_change_cost 3 \
#    --finger_in_same_column_cost 6 | head ) \
# <( echo "Measure 1 - G4
# PULL:
# .....   .....
# ...@.   .....
# .....   .....
# Measure 1 - A4
# PUSH:
# .....   .....
# .....   .....
# ..@..   ....." )


echo 'PASS!'

