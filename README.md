# concertina-helper
Python script to find good fingerings for musical passages on the Anglo-German concertina.

## Getting started

```
git clone https://github.com/mccalluc/concertina-helper.git
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Other tools

### Fingerings over passages

- [Anglo Concertina Fingering Generator](https://jvandonsel.github.io/fingering/fingering.html): Web page which takes ABC notation, and returns ABC notation, and renders it using [abcjs](https://www.abcjs.net/)
- [concertina-pbqp](https://github.com/resistor/concertina-pbqp): C++; Models it as an NP-hard problem, but uses a solver library for an approximate solution. 
- [juliamullen/concertina](https://github.com/juliamullen/concertina): Python classes.

### Just notes and chords

- [Anglo Piano](https://anglopiano.com/): Web page with piano and a variety of concertina layouts. Shows all possible fingerings for notes and chords.
- [KonzertinaNetz](https://www.konzertinanetz.de/): Auf Deutsch. Includes windows `.exe` for download.
- [german-concertina-notes](https://github.com/daniel-leinweber/german-concertina-notes): HTML and JS, but not deployed to a site.
