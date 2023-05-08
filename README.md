# concertina-helper
Python script to find good fingerings on bisonoric concertinas for tunes in
[ABC notation](https://abcnotation.com/), and a supporting API.

## CLI usage

See [`demo-cli.sh`](https://github.com/mccalluc/concertina-helper/blob/main/demo-cli.sh)
for examples of CLI usage.
```
usage: concertina-helper [-h] [--format {unicode,ascii,long}]
                         (--layout_path PATH | --layout_name {20_cg,30_jefferies_cg,30_wheatstone_cg})
                         [--layout_transpose SEMITONES]
                         [--bellows_change_cost N]
                         [--finger_in_same_column_cost N]
                         [--pull_at_start_of_measure_cost N] [--show_all]
                         abc_path

Given a file containing ABC notation, and a concertina type, prints possible
fingerings.

positional arguments:
  abc_path              Path of ABC file

options:
  -h, --help            show this help message and exit
  --format {unicode,ascii,long}
                        Output format. "unicode" uses "○" and "●" to represent
                        button state / "ascii" uses "." and "@" to represent
                        button state / "long" spells out the names of pressed
                        buttons (default: long)

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
  --show_all            Ignore cost options and just show all possible
                        fingerings (default: False)
```

## API usage

See [API documentation](https://mccalluc.github.io/concertina-helper) for details.

## Development

See [`demo-api.sh`](https://github.com/mccalluc/concertina-helper/blob/main/demo-cli.sh)
for for typical developer setup. The demo scripts are also used for CI.

## Related tools

### Generate fingerings for tunes

- [Anglo Concertina Fingering Generator](https://jvandonsel.github.io/fingering/fingering.html): Web page which takes ABC notation, and returns ABC notation, and renders it using [abcjs](https://www.abcjs.net/)
- [concertina-pbqp](https://github.com/resistor/concertina-pbqp): C++; Models it as an NP-hard problem, but uses a solver library for an approximate solution. 

### Notes and chords

- [Anglo Piano](https://anglopiano.com/): Web page with piano and a variety of concertina layouts. Shows all possible fingerings for notes and chords.
- [KonzertinaNetz](https://www.konzertinanetz.de/): Auf Deutsch. Includes windows `.exe` for download.
