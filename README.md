# concertina-helper
Python script to find good fingerings on bisonoric concertinas for tunes in
[ABC notation](https://abcnotation.com/), and a supporting API.

## CLI usage

(Plan to push to PyPi eventually: [Issue](https://github.com/mccalluc/concertina-helper/issues/2))
```
git clone https://github.com/mccalluc/concertina-helper.git
cd concertina-helper
pip install flit
flit install --symlink
from-abc --help
```
```
usage: from-abc [-h] [--verbose] [--layout_transpose SEMITONES]
                (--layout_path PATH | --layout_name {20_cg,30_wheatstone_cg,30_jefferies_cg})
                abc_path

Given a file containing ABC notation, and a concertina type, prints possible
fingerings.

positional arguments:
  abc_path              Path of ABC file

options:
  -h, --help            show this help message and exit
  --verbose
  --layout_transpose SEMITONES
                        Semitones to transpose the layout; Negative transposes
                        down
  --layout_path PATH    Path of YAML file with concertina layout
  --layout_name {20_cg,30_wheatstone_cg,30_jefferies_cg}
                        Name of concertina layout
```

## API usage

See [API documentation](https://mccalluc.github.io/concertina-helper).

## Development


```
pip install -r requirements.txt
pip install -r requirements-dev.txt
./ci.sh
```

## Related tools

### Generate fingerings for tunes

- [Anglo Concertina Fingering Generator](https://jvandonsel.github.io/fingering/fingering.html): Web page which takes ABC notation, and returns ABC notation, and renders it using [abcjs](https://www.abcjs.net/)
- [concertina-pbqp](https://github.com/resistor/concertina-pbqp): C++; Models it as an NP-hard problem, but uses a solver library for an approximate solution. 

### Notes and chords

- [Anglo Piano](https://anglopiano.com/): Web page with piano and a variety of concertina layouts. Shows all possible fingerings for notes and chords.
- [KonzertinaNetz](https://www.konzertinanetz.de/): Auf Deutsch. Includes windows `.exe` for download.
