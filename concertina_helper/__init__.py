"""
**concertina_helper** is a python script that helps
find good fingerings on bisonoric concertinas for tunes provided in
[ABC notation](https://abcnotation.com/), and a supporting API.

This is the API documentation; For help with the CLI,
see the [README](https://github.com/mccalluc/concertina-helper#readme).

The CLI is a thin wrapper around
`concertina_helper.tune_on_layout.TuneOnLayout.get_best_fingerings`:

>>> from pathlib import Path
>>> from pyabc2 import Tune
>>> from concertina_helper.tune_on_layout import TuneOnLayout
>>> from concertina_helper.layouts.layout_loader import load_bisonoric_layout_by_name
>>> from concertina_helper.penalties import (
...     penalize_finger_in_same_column, penalize_bellows_change)
>>> tune = Tune(Path('tests/g-major.abc').read_text())
>>> layout = load_bisonoric_layout_by_name('30_wheatstone_cg')
>>> t_l = TuneOnLayout(tune, layout)
>>> best = t_l.get_best_fingerings(
...     penalize_finger_in_same_column(3),
...     penalize_bellows_change(2))
>>> len(best)
8
>>> print(best[0].fingering)
???
>>> print(best[-1].fingering)
???

**concertina_helper** models a tune as a graph,
with each possible fingering for a given note a node in that graph. It then uses an
[implementation of the A* algorithm](https://github.com/jrialland/python-astar/)
(wrapped in `concertina_helper.finger_finder`)
to find the best path through this graph.

Classes representing uni- and bisonoric layouts, fingerings on those layouts,
and utilities to create layouts, are in `concertina_helper.layouts`.

Functions that encapsulate heuristics about what makes a "good" fingering are in
`concertina_helper.penalties`, or you can provide your own penalty functions.
"""

__version__ = "0.0.1"
