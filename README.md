# concertina-helper
Python script to find good fingerings for musical passages on the Anglo-German concertina.

## Getting started

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
                (--layout_path PATH | --layout_name {wheatstone_cg})
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
  --layout_name {wheatstone_cg}
                        Name of concertina layout
```


## Other tools

### Fingerings over passages

- [Anglo Concertina Fingering Generator](https://jvandonsel.github.io/fingering/fingering.html): Web page which takes ABC notation, and returns ABC notation, and renders it using [abcjs](https://www.abcjs.net/)
- [concertina-pbqp](https://github.com/resistor/concertina-pbqp): C++; Models it as an NP-hard problem, but uses a solver library for an approximate solution. 

### Notes and chords

- [Anglo Piano](https://anglopiano.com/): Web page with piano and a variety of concertina layouts. Shows all possible fingerings for notes and chords.
- [KonzertinaNetz](https://www.konzertinanetz.de/): Auf Deutsch. Includes windows `.exe` for download.

### Incomplete projects

- [juliamullen/concertina](https://github.com/juliamullen/concertina): Some Python classes.
- [german-concertina-notes](https://github.com/daniel-leinweber/german-concertina-notes): HTML and JS, but not deployed to a site.
