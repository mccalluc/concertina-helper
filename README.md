# concertina-helper

[![PyPI version](https://badge.fury.io/py/concertina_helper.svg)](https://pypi.org/project/concertina_helper/)

**concertina_helper** is a python script and supporting API
to find good fingerings on bisonoric concertinas for
tunes in [ABC notation](https://abcnotation.com/).

## CLI usage

```
pip install concertina-helper
concertina-helper --help
```
```
usage: concertina-helper [-h] [--output_format {UNICODE,ASCII,LONG,COMPACT}]
                         (--layout_path PATH | --layout_name {20_cg,30_jefferies_cg,30_wheatstone_cg})
                         [--layout_transpose SEMITONES]
                         [--bellows_change_cost N]
                         [--finger_in_same_column_cost N]
                         [--pull_at_start_of_measure_cost N]
                         [--outer_fingers_cost N] [--show_all]
                         input

Given a file containing ABC notation, and a concertina type, prints possible
fingerings.

positional arguments:
  input                 Input file: Parsed either as a list of pitches, one
                        per line, or as ABC, if the first lines starts with
                        "X:".

options:
  -h, --help            show this help message and exit
  --output_format {UNICODE,ASCII,LONG,COMPACT}
                        Output format. "UNICODE" uses "○" and "●" to represent
                        button state / "ASCII" uses "." and "@" to represent
                        button state / "LONG" spells out the names of pressed
                        buttons / "COMPACT" multiple fingerings represented in
                        single grid (default: LONG)

Layout options:
  Supply your own layout, or use a predefined one, optionally transposed

  --layout_path PATH    Path of YAML file with concertina layout (default:
                        None)
  --layout_name {20_cg,30_jefferies_cg,30_wheatstone_cg}
                        Name of concertina layout (default: None)
  --layout_transpose SEMITONES
                        Semitones to transpose the layout; Negative transposes
                        down (default: 0)

Cost options:
  Configure the relative costs of different transitions between fingerings

  --bellows_change_cost N
                        Penalize fingerings where the bellows changes
                        direction between notes (default: 1)
  --finger_in_same_column_cost N
                        Penalize fingerings where one finger changes rows
                        between notes (default: 1)
  --pull_at_start_of_measure_cost N
                        Penalize fingerings where a pull begins a measure;
                        Hitting the downbeat with a push can be more musical.
                        (default: 1)
  --outer_fingers_cost N
                        Penalize fingerings that use outer fingers of either
                        hand instead of inner. This is useful as a tiebreaker.
                        (default: 1)
  --show_all            Ignore cost options and just show all possible
                        fingerings (default: False)
```

See [`EXAMPLES.md`](https://github.com/mccalluc/concertina-helper/blob/main/EXAMPLES.md)
for examples of CLI usage.

## API usage

See [API documentation](https://mccalluc.github.io/concertina-helper) for details.

## Development

See [`demo-api.sh`](https://github.com/mccalluc/concertina-helper/blob/main/demo-cli.sh)
for typical developer setup. Code has full type annotations, and 100% test coverage.

To release a new version:
- Make a feature branch
- Update `__version__` in `__init__.py`
- Run `flit publish`
- Make a PR with the updated version and merge.

## Related tools

### Generate fingerings for tunes

- [Anglo Concertina Fingering Generator](https://jvandonsel.github.io/fingering/fingering.html): Web page which takes ABC notation, and returns ABC notation, and renders it using [abcjs](https://www.abcjs.net/)
- [concertina-pbqp](https://github.com/resistor/concertina-pbqp): C++; Models it as an NP-hard problem, but uses a solver library for an approximate solution. 

### Notes and chords

- [Anglo Piano](https://anglopiano.com/): Web page with piano and a variety of concertina layouts. Shows all possible fingerings for notes and chords.
- [KonzertinaNetz](https://www.konzertinanetz.de/): In German. Includes windows `.exe` for download.
